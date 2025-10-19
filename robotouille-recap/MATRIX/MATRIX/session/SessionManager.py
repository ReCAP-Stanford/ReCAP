from langchain_openai import ChatOpenAI
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re

import os

from rich.console import Console

import toml
from pathlib import Path

config_path = Path(__file__).parent.parent / "task_description.toml"
conf = toml.load(config_path.resolve())
expected_final_states = conf['original_task_description']


def create_llm(model_name: str = "gpt-4o", temperature: float = 0.5, is_json: bool = False):
    if is_json:
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            streaming=False,  # set True if you want real‐time tokens，
            api_key=os.environ.get("OPENAI_API_KEY"),
            # format='json' if is_json else None,
        ).bind(response_format={"type": "json_object"})
    else:
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            streaming=False,  # set True if you want real‐time tokens，
            api_key=os.environ.get("OPENAI_API_KEY"),
            # format='json' if is_json else None,
        )

def build_tree_graph(node, graph=None, parent=None, parent_name=None):
    if graph is None:
        graph = nx.DiGraph()
    name = f"id:{node.id}: {node.name}"
    graph.add_node(name)
    if parent:
        graph.add_edge(parent_name, name)
    for child in node.children:
        build_tree_graph(child, graph, node, parent_name=name)
    return graph

def draw_tree_image(root_node):
    graph = build_tree_graph(root_node)
    pos = nx.spring_layout(graph)    
    plt.figure(figsize=(10, 5))
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


class SessionManager:
    def __init__(self, system_description=None, rule_description=None, environment_name=None, ablation="original", ctx_len=64):

        self.reset_session()
        self.system_description = system_description
        self.rule_description = rule_description
        print("Rule Description: ", self.rule_description)
        self.expected_final_state = expected_final_states[environment_name]

        if ablation == "nothink":
            from ..chatbot_no_think import chatbot
            from ..prompts import get_few_shot_no_think
            self.few_shot_list = get_few_shot_no_think()
        elif ablation == "nameonly":
            from ..chatbot_name_only import chatbot
            from ..prompts import get_few_shot_name_only
            self.few_shot_list = get_few_shot_name_only()
        elif ablation == "thinkmany":
            from ..chatbot_think_many import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()
        elif ablation == "level2":
            from ..chatbot_level_2 import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()
        elif ablation == "level3":
            from ..chatbot_level_3 import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()
        elif ablation == "level4":
            from ..chatbot_level_4 import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()
        elif ablation == "level5":
            from ..chatbot_level_5 import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()
        else:
            from ..chatbot import chatbot
            from ..prompts import get_few_shot
            self.few_shot_list = get_few_shot()

        self.chatbot = chatbot
        self.ctx_len = ctx_len

    def reset_session(self):
        self.context = None
        self.task = None
        self.generator = None
        self.last_action = None
        self.run_cnt = 0
        self.ended = False
        self.action_list = []

    def step_with_obs(self, obs, str_valid_actions):
        if self.ended:
            return None
        try:

            if self.run_cnt == 0:
                self.generator = self.chatbot(
                    system_prompt=self.system_description,
                    few_shot_list=self.few_shot_list,
                    task_name=self.expected_final_state,
                    init_obs=obs,
                    rule=self.rule_description,
                    valid_actions = str_valid_actions,
                    ctx_len=self.ctx_len
                )

                action = next(self.generator)
                self.last_action = action
                self.action_list.append(action)
            else:
                action = self.generator.send((obs, str_valid_actions))
                self.last_action = action
                self.action_list.append(action)
        except StopIteration as e:
            try:
                self.last_action = f"{e.value}"
                self.action_list.append(self.last_action)
                self.ended = True
                print(f"ALL Actions: {self.action_list}")
            except:
                pass
        self.run_cnt += 1
        console = Console()
        console.print(f'[yellow]Action: {self.last_action}[/yellow]')
        return self.last_action

    def get_context_image(self):
        if self.context.root is None:
            return ""
        return draw_tree_image(self.context.root)
    
    def is_ended(self):
        return self.ended
