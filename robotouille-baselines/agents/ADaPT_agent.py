import os
import re
import copy
from typing import List, Tuple

from .agent import Agent
from .ReAct_agent import ReActAgent
from .prompt_builder.prompt_llm import prompt_llm


class ADaPTAgent(Agent):
    _STEP_REGEX = re.compile(r"^Step\s*(\d+):\s*(.+)$", re.M)
    _EXEC_REGEX = re.compile(r"Execution\s*order\s*:\s*(.+)", re.I)

    def __init__(self, kwargs):

        super().__init__(kwargs)

        # Planner configuration.  If unspecified fall back to sensible
        self.planner_model = kwargs.get('planner_model', 'gpt-4o')
        self.planner_temperature = kwargs.get('planner_temperature', 0.0)
        # Allow users to override retry behaviour for planner queries
        self.planner_max_attempts = kwargs.get('planner_max_attempts', 10)
        self.planner_sleep_time = kwargs.get('planner_sleep_time', 5)
        self.executor_example_dir_path = kwargs.get("example_dir_path", None)

        # Cache of planner system messages and few‑shot examples.  Read once
        # during initialisation.  If the prompt files are missing a
        # RuntimeError will be raised.
        adapt_dir = os.path.join(os.path.dirname(__file__), 'prompt_builder', 'prompts', 'Adapt')
        planner_sys_path = os.path.join(adapt_dir, 'planner_system.txt')
        if not os.path.exists(planner_sys_path):
            raise RuntimeError(f"Planner system prompt not found at {planner_sys_path}")
        with open(planner_sys_path, 'r', encoding='utf-8') as f:
            planner_system = f.read().strip()
        # Start building the planner messages with the system prompt.
        self.planner_messages: List[dict] = [
            {"role": "system", "content": planner_system}
        ]

        planner_fewshot_path = os.path.join(adapt_dir, 'planner_fewshot.txt')
        if os.path.exists(planner_fewshot_path):
            try:
                with open(planner_fewshot_path, 'r', encoding='utf-8') as f:
                    fewshot_text = f.read()
                # Split the text into blocks separated by Interaction labels
                interactions = re.split(r'(?i)\bInteraction\s*\d+\s*\n+[-]+\n+', fewshot_text)
                for block in interactions:
                    block = block.strip()
                    if not block:
                        continue
                    # Extract the user segment (Observation and Goal) and assistant segment
                    user_match = re.search(r'Observation:(.*?)Reasoning:', block, re.S)
                    assist_match = re.search(r'Reasoning:(.*)', block, re.S)
                    if not user_match or not assist_match:
                        continue
                    user_content = user_match.group(1).strip()
                    user_content = f"Observation:{user_content}"
                    assistant_content = assist_match.group(1).strip()
                    self.planner_messages.append({"role": "user", "content": user_content})
                    self.planner_messages.append({"role": "assistant", "content": assistant_content})
            except Exception:
                # Ignore parsing failures and fall back to system message only
                pass


        self._base_executor_kwargs = copy.deepcopy(kwargs)
        self._executor_prompt_params = {
            'experiment_name': 'Adapt',
            'prompt_description': 'executor',
            'prompt_version': 'custom',
            'model': kwargs.get('model', 'gpt-4o'),
            'temperature': kwargs.get('temperature', 0.0),
        }


        self._info_prop: str = ''
        self._last_action: object = None

        # Internal plan state
        self._plan_steps: List[str] = []
        self._current_step_idx: int = 0
        self._executor_agent: ReActAgent = None  # Active ReActAgent
        self._done: bool = False  # Whether all subtasks are complete

        self._error_feedback: str = ''

    def is_done(self) -> bool:
        return self._done

    def is_retry(self, steps_left: int) -> bool:
        return False

    # ------------------------------------------------------------------
    # Planning utilities
    # ------------------------------------------------------------------
    def _plan(self, obs: str, env) -> List[str]:
        """Generate a list of abstract subtasks from the current observation.

        This method calls the planner LLM via ``prompt_llm``.  It
        constructs a user prompt containing the observation and the list
        of valid low‑level actions available in the environment.  The
        planner system prompt (loaded at initialisation) instructs the
        model to return a numbered set of steps and a final execution
        order.  Only the step descriptions are extracted – the logical
        execution order is ignored for simplicity.

        Parameters
        ----------
        obs : str
            Natural language observation describing the current state and
            goal.
        env : object
            The environment object.  Must support
            ``current_state.get_valid_actions_and_str()`` which returns a
            tuple ``(valid_actions, str_valid_actions)`` where
            ``str_valid_actions`` is a list of string representations of
            valid low‑level actions.

        Returns
        -------
        List[str]
            A list of high‑level subtask descriptions extracted from the
            planner's response.  If no steps are found an empty list is
            returned.
        """
        try:
            _, str_valid_actions = env.current_state.get_valid_actions_and_str()
        except AttributeError:
            str_valid_actions = []


        user_prompt_lines: List[str] = []
        if self._error_feedback:
            user_prompt_lines.append(f"Error Feedback: {self._error_feedback}")
            self._error_feedback = ''
        user_prompt_lines.append(f"Observation: {obs}")
        user_prompt = '\n'.join(user_prompt_lines)


        planner_params = {
            'messages': self.planner_messages,
            'model': self.planner_model,
            'temperature': self.planner_temperature,
            'max_attempts': self.planner_max_attempts,
            'sleep_time': self.planner_sleep_time,
        }

        # Invoke the planner.
        try:
            plan_str = prompt_llm(user_prompt, **planner_params)
        except Exception:
            # If the planner fails entirely return an empty plan.  This
            # causes the agent to terminate immediately.
            return []

        # Parse the planner output into a list of subtasks.  This will
        # honour the logical execution order expression where possible.
        return self._parse_plan(plan_str)

    def _parse_plan(self, plan_str: str) -> List[str]:
        step_lookup: dict[int, str] = {}
        for match in self._STEP_REGEX.finditer(plan_str):
            try:
                step_num = int(match.group(1))
                desc = match.group(2).strip()
                step_lookup[step_num] = desc
            except Exception:
                continue
        if not step_lookup:
            return []

        # Attempt to extract the execution order expression.  If it is
        # missing simply return the descriptions in step number order.
        exec_match = self._EXEC_REGEX.search(plan_str)
        if not exec_match:
            return [step_lookup[n] for n in sorted(step_lookup.keys())]
        expr = exec_match.group(1).strip()
        try:
            logic_exp = self._parse_expression(expr)
            structured = self._fetch_args(step_lookup, logic_exp)
            return self._flatten_structure(structured)
        except Exception:
            # Fall back to numeric order if parsing fails
            return [step_lookup[n] for n in sorted(step_lookup.keys())]

    def _parse_expression(self, expression: str) -> dict:
        stack: list[dict] = []
        current: dict = {}
        # Tokenise the expression.  Regex finds Step N, AND, OR, '(' and ')'
        for token in re.findall(r'Step\s+\d+|AND|OR|\(|\)', expression):
            if token.startswith('Step'):
                # Extract the step number
                num = int(token.split()[1])
                current.setdefault('steps', []).append(num)
            elif token in ('AND', 'OR'):
                current['logic'] = token
            elif token == '(':  # Start a new nested group
                stack.append(current)
                current = {}
            elif token == ')':  # Close the current group
                closed = current
                current = stack.pop() if stack else {}
                current.setdefault('steps', []).append(closed)
        return current

    def _fetch_args(self, lookup: dict, logic_exp: dict) -> dict:
        out = copy.deepcopy(logic_exp)
        steps = out.get('steps', [])
        for idx, step in enumerate(steps):
            if isinstance(step, int):
                out['steps'][idx] = lookup.get(step, f'Step {step}')
            elif isinstance(step, dict):
                out['steps'][idx] = self._fetch_args(lookup, step)
        return out

    def _flatten_structure(self, structure: dict) -> List[str]:
        tasks: List[str] = []
        steps = structure.get('steps', [])
        # Honour OR logic by taking only the first branch.  If logic is
        # unspecified or AND, traverse all branches.
        logic = structure.get('logic', '').upper() if isinstance(structure.get('logic', ''), str) else ''
        if logic == 'OR' and steps:
            step = steps[0]
            if isinstance(step, str):
                tasks.append(step)
            elif isinstance(step, dict):
                tasks.extend(self._flatten_structure(step))
            return tasks
        for step in steps:
            if isinstance(step, str):
                tasks.append(step)
            elif isinstance(step, dict):
                tasks.extend(self._flatten_structure(step))
        return tasks

    def _init_executor(self, subtask: str) -> None:
        exec_kwargs = copy.deepcopy(self._base_executor_kwargs)
        exec_kwargs['prior'] = f"Subtask: {subtask}"
        exec_kwargs.setdefault('prompts', {})
        exec_kwargs['prompts']['action_proposal_prompt'] = self._executor_prompt_params
        exec_kwargs['example_dir_path'] = self.executor_example_dir_path
        self._executor_agent = ReActAgent(exec_kwargs)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def propose_actions(self, obs: str, env) -> List[object]:
        """Propose one or more low‑level actions for the current state.

        This method orchestrates planning and execution.  On the first
        call it plans a sequence of abstract subtasks using the
        observation and valid actions.  It then instantiates a new
        ``ReActAgent`` for the first subtask and delegates action
        proposals to it.  When the current executor signals that the
        subtask has finished (by returning an empty list) this method
        advances to the next subtask.  Once all subtasks have been
        exhausted it marks the agent as done and returns an empty list on
        subsequent calls.

        Parameters
        ----------
        obs : str
            Natural language observation of the environment state.
        env : object
            The environment object passed through to the executor.

        Returns
        -------
        List[object]
            A (possibly empty) list of low‑level actions to take.  If the
            list is empty the agent has either finished the current
            subtask or completed its entire plan.
        """
        if self._done:
            return []


        if not self._plan_steps:
            self._plan_steps = self._plan(obs, env)
            self._current_step_idx = 0
            # If planning produced no steps treat this as completion
            if not self._plan_steps:
                self._done = True
                return []

        if self._executor_agent is None and self._current_step_idx < len(self._plan_steps):
            current_subtask = self._plan_steps[self._current_step_idx]
            self._init_executor(current_subtask)


        if self._executor_agent is not None:
            proposed = self._executor_agent.propose_actions(obs, env)
            if proposed:
                return proposed

            self._executor_agent = None
            self._current_step_idx += 1
            if self._current_step_idx >= len(self._plan_steps):
                self._done = True
                return []
            return self.propose_actions(obs, env)

        self._done = True
        return []
