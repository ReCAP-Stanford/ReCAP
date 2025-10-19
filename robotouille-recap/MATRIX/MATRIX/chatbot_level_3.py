import os
import json
import openai
import tiktoken

from typing import List

import time

import re
_quad_fence = re.compile(r'`+(?:json)?', re.IGNORECASE)
#from prompts import get_few_shot

def remove_json_fence(text: str) -> str:
    """
    Remove the JSON fence from the text.
    """
    # Remove the JSON fence
    text = _quad_fence.sub('', text)
    return text

# 1) Define model pricing (per 1 000 tokens)
MODEL_PRICING = {
    "gpt-4o": {
        "prompt": 0.0025,     # $0.03 per 1 000 prompt tokens
        "completion": 0.01  # $0.06 per 1 000 completion tokens
    },
    "gpt-4.1": {
        "prompt": 0.002,
        "completion": 0.008
    },
    # add other models/prices here…
}

def count_chat_tokens(messages, model):
    """Count tokens in a list of chat messages for the given model."""
    enc = tiktoken.encoding_for_model(model)
    # per OpenAI chat-token guidelines:
    tokens_per_message = 3
    tokens_per_name    = 1
    total = 0
    for msg in messages:
        total += tokens_per_message
        for k, v in msg.items():
            total += len(enc.encode(v))
            if k == "name":
                total += tokens_per_name
    total += 3  # assistant priming
    return total

def call_llm(user_prompt, history, client, model, ctx_len):
    """Prompts the LLM with messages and parameters.
    
    Parameters:
        user_prompt (str)
            The user prompt to query the LLM with.
        params (dict)
            The parameters to prompt the LLM with.
        history (list)
            The history of the conversation.
    
    Returns:
        response (str)
            The response from the LLM.
        truncated_history (list)
            The truncated history that fits within the context length.
    """
    success = False
    truncated_history = history
    while not success:
        try:
            # if model != "gpt-4o" and len(truncated_history) > 32:
            if len(truncated_history) > ctx_len:
                del truncated_history[2:4]
            truncated_history.append({'role': 'user', 'content': user_prompt})
            # 2) Count prompt tokens
            if model == "gpt-4o":
                prompt_tokens = count_chat_tokens(history, model)
            response = client.chat.completions.create(
                model=model,
                messages=history,
                response_format={ "type": "json_object" }
            )
            response = response.choices[0].message.content
            truncated_history.append({'role': 'assistant', 'content': response})
            success = True
        except openai.BadRequestError as e:
            error_code = e.code
            if error_code == 'context_length_exceeded':
                assert len(truncated_history) > 3, "The starter prompt is too long."
                # Remove the first and second element
                del truncated_history[2:34]
                if len(truncated_history) > 2:
                    # remove last element (the input prompt), because the same prompt will be added in the next iteration
                    del truncated_history[-1]

            else:
                raise e # Raise other errors for user to handle
        if model == "gpt-4o":
            # 4) Count completion tokens
            enc = tiktoken.encoding_for_model(model)
            completion_tokens = len(enc.encode(response))
            total_tokens = prompt_tokens + completion_tokens
            
            # 5) Compute cost
            pricing = MODEL_PRICING.get(model, {})
            prompt_cost = prompt_tokens/1_000 * pricing.get("prompt", 0)
            completion_cost = completion_tokens/1_000 * pricing.get("completion", 0)
            cost = prompt_cost + completion_cost
        
            usage = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "prompt_cost": prompt_cost,
                "completion_cost": completion_cost,
                "cost_usd": cost
            }
    return response, truncated_history, None if model != "gpt-4o" else usage


class ChatGPTWithMemory:
    def __init__(self, fixed_prompt, ctx_len):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
        self.fixed_prompt = fixed_prompt
        self.truncated_chat_history = [fixed_prompt]
        self.ctx_len = ctx_len
        self.usage_history = []
        self.total_prompt_cost = 0
        self.total_completion_cost = 0
        self.total_cost = 0

    def invoke(self, user_prompt: str) -> str:
        response, self.truncated_chat_history, usage = call_llm(user_prompt, self.truncated_chat_history, self.client, self.model, self.ctx_len)
        if self.model == "gpt-4o":
            self.total_prompt_cost += usage["prompt_cost"]
            self.total_completion_cost += usage["completion_cost"]
            self.total_cost += usage["cost_usd"]
            usage["cumulated_prompt_cost"] = self.total_prompt_cost
            usage["cumulated_completion_cost"] = self.total_completion_cost
            usage["cumulated_cost"] = self.total_cost
            self.usage_history.append(usage)
        return response

    def reset(self):
        """重置对话历史"""
        self.truncated_chat_history = [self.fixed_prompt]
    
    def save_history_to_json(self, file_path: str = "history.json"):
        """
        将历史记录保存到json文件
        """
        with open(file_path, "w") as f:
            json.dump(self.truncated_chat_history, f, ensure_ascii=False, indent=4)
    
    def save_cost_to_json(self, file_path: str = "cost.json"):
        """
        将历史花费保存到json文件
        """
        if self.model == "gpt-4o":
            with open(file_path, "w") as f:
                json.dump(self.usage_history, f, ensure_ascii=False, indent=4)


class Node:
    def __init__(self, task_name, parent=None):
        self.children = []
        self.parent = None
        self.info_list = []
        self.task_name = task_name
        self.obs_list = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def set_info(self, info):
        self.info_list.append(info)
    
    def get_latest_info(self):
        if len(self.info_list) == 0:
            return None
        return self.info_list[-1]
    
    def set_obs(self, obs):
        self.obs_list.append(obs)
    
    def get_latest_obs(self):
        if len(self.obs_list) == 0:
            return None
        return self.obs_list[-1]


def tree_to_dict(node: Node):
    """
    将树结构转换为字典结构
    """
    if node is None:
        return None
    return {
        "task_name": node.task_name,
        "children": [tree_to_dict(child) for child in node.children],
        "info_list": node.info_list,
        "obs_list": node.obs_list
    }


def save_tree_to_json(node: Node, file_path: str):
    """
    将树结构保存为json文件
    """
    tree_dict = tree_to_dict(node)
    with open(file_path, "w") as f:
        json.dump(tree_dict, f, ensure_ascii=False, indent=4)


def print_tree(node:Node, level=0):
    """
    打印树结构
    """
    if node is None:
        return
    indent = "    " * level
    print(indent + f"Task: {node.task_name}")
    print(indent + f"Info: {node.info_list}")
    print(indent + f"Obs: {node.obs_list}")
    for child in node.children:
        print_tree(child, level + 1)



class Prompt:
    def __init__(self, ):
        pass
    
      
    def generate_init_prompt(self, task_name: str, init_obs: str, rule: str, system_prompt: str):

        return f"""
{system_prompt}

Here's the rule of the environment:
{rule}

{init_obs}

Now you need to make a new meal. Here is the goal description:
{task_name}

Now, start the task.
"""
    
      
    def generate_down_prompt(self, task_name: str):
        return f"""OK.

Your current task: {task_name}

We wish you to generate a list of subtasks for the current task.
"""

      
    def generate_leaf_down_prompt(self, task_name: str):
        return f"""OK.

Your current task: {task_name}

You are reaching the maximum depth of task decomposition. We wish you to generate a single valid action for the current task.
"""


      
    def generate_leaf_up_prompt(self,
                           obs = None,
                           done_task_name: str = None,
                           previous_stage_task_name: str = None,
                           previous_stage_think: str = None,
                           remaining_subtask: List[str] = [],
                           ):

        if remaining_subtask:
            remaining_subtask_str = '\n'.join(remaining_subtask)
        else:
            remaining_subtask_str = "No remaining subtasks."
        return f"""You have successfully completed the task: {done_task_name}

{obs}

Now, you return to the parent task.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

Your remaining subtasks:
{remaining_subtask_str}

We wish you to refine your list of subtasks. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.
"""
    
    def generate_nonleaf_judge_done_prompt(self, 
                            done_task_name,
                            previous_stage_task_name: str,
                            previous_stage_think: str):
        return f"""You have successfully completed the task: {done_task_name}

Now, you return to the parent task.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

There are no remaining subtasks for the current task. Please determine whether the task has been completed. If it has, set the subtasks to an empty list; if not, generate the necessary subtasks required to complete the current task.
"""
    def generate_leaf_judge_done_prompt(self,
                            obs,
                            done_task_name,
                            previous_stage_task_name: str,
                            previous_stage_think: str):
        return f"""You have successfully completed the task: {done_task_name}

{obs}

Now, you return to the parent task.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

There are no remaining subtasks for the current task. Please determine whether the task has been completed. If it has, set the subtasks to an empty list; if not, generate the necessary subtasks required to complete the current task.
"""
    
    def generate_leaf_up_fail_prompt(self,
                           obs = None,
                           fail_task_name: str = None,
                           previous_stage_task_name: str = None,
                           previous_stage_think: str = None,
                           remaining_subtask: List[str] = [],
                           ):
        remaining_subtask_str = '\n'.join(remaining_subtask)
        return f"""You fail to complete the task: {fail_task_name}
Because the task name is not included in the valid actions provided in the observation. Your assumptions may not be valid.
Potential cause of the problem might be:
1. The action name is not the EXACT match of the valid action name.
2. You can't place an object directly on a Station when it's occupied by another object. Otherwise you will stack on it.
3. You can't cut an object that is stacked on another object. It must be directly on the board. You should remove the object underneath first.
4. You can't pick up an item that is being stacked under another item. It must be on the top.

{obs}

Now, you return to the parent task.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

Your remaining subtasks:
{remaining_subtask_str}

We wish you to modify your subtasks in order to fix the error.
"""
    
    def generate_nonleaf_up_prompt(self,
                           done_task_name: str = None,
                           previous_stage_task_name: str = None,
                           previous_stage_think: str = None,
                           remaining_subtask: List[str] = [],
                           ):
        if remaining_subtask:
            remaining_subtask_str = '\n'.join(remaining_subtask)
        else:
            remaining_subtask_str = "No remaining subtasks."
        return f"""You have successfully completed the task: {done_task_name}

Now, you return to the parent task.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

Your remaining subtasks:
{remaining_subtask_str}

We wish you to refine your list of subtasks. Do not generate any subtasks beyond the scope of the current task.
"""


def check_valid_action(action: str, valid_actions: List[str]) -> bool:
    return action in valid_actions


def chatbot(system_prompt: str, few_shot_list: str, task_name: str, init_obs: str, rule: str, valid_actions: List[str], ctx_len: int):

    cur_time = time.strftime('%Y%m%d_%H%M%S')
    # log_dir = f"logs_level_3_ctx_{ctx_len}_{task_name}"
    log_dir = f"logs_level_3_ctx_{ctx_len}"
    os.makedirs(log_dir, exist_ok=True)
    log_tree_json_file_path = f"{log_dir}/tree_{cur_time}.json"
    log_history_json_file_path = f"{log_dir}/history_{cur_time}.json"
    log_cost_json_file_path = f"{log_dir}/cost_{cur_time}.json"
    
    # Start
    few_shot_str = '\n'.join(f"{d['role']}: {d['content']}" for d in few_shot_list)
    few_shot_str = f"""Here is a demo of making an onion cheese sandwich:
{few_shot_str}

END OF DEMO.
    """
    llm = ChatGPTWithMemory(fixed_prompt={'role': 'user', 'content': few_shot_str}, ctx_len=ctx_len)
    prompt_obj = Prompt()
      
    prompt = prompt_obj.generate_init_prompt(
        task_name=task_name,
        init_obs=init_obs,
        rule=rule,
        system_prompt=system_prompt
    )


    # 创建根节点
    root = Node(task_name=task_name, parent=None)
    # 初始化状态变量
    node_ptr = root # 指向当前节点
    cur_obs = init_obs # 当前观察
    during_down = True # 当前是否是递归（反之则是回溯）
    level = 0
    max_level = 2
    invoke_cnt = 0 # LLM被call的次数
    while node_ptr:
        # 生成回答
        invoke_cnt += 1
        # Rule提醒
        if invoke_cnt % 10 == 0:
            rule_str = f"""Since we’ve gone through many rounds of dialogue, here’s a reminder to prevent you from forgetting the operation rules. The rules are as follows:

{rule}

END OF RULE

"""
            prompt = rule_str + prompt
        
        response = llm.invoke(prompt)
        
        # 解析回答
        # response结构: {
        #     "think": str
        #     "subtasks": [str]
        # }

        try:
            response = json.loads(remove_json_fence(response))
            # 处理回答
            # 1. 外部context tree设置
            node_ptr.set_info(response)
            node_ptr.set_obs(cur_obs)
            # 2. 判断是否是叶子结点
            if during_down and len(response['subtasks']) == 1 or level == max_level:
                level -= 1
                action = response["subtasks"][0]
                if check_valid_action(action, valid_actions):
                    # yield之前先log
                    save_tree_to_json(root, log_tree_json_file_path)
                    llm.save_history_to_json(log_history_json_file_path)
                    llm.save_cost_to_json(log_cost_json_file_path)
                    # 如果当前动作是valid action, 则执行
                    cur_obs, valid_actions = yield action
                    # 更新状态
                    during_down = False
                    
                    # 如果没有remaining_subtask, 则直接回溯
                    done_task_name = node_ptr.task_name
                    node_ptr = node_ptr.parent
                    if not node_ptr:
                        break
                    
                    # 生成下一轮的Prompt
                    if node_ptr.get_latest_info()['subtasks'][1:]:
                        prompt = prompt_obj.generate_leaf_up_prompt(
                            obs=cur_obs,
                            done_task_name=done_task_name,
                            previous_stage_task_name=node_ptr.task_name,
                            previous_stage_think=node_ptr.get_latest_info()['think'],
                            remaining_subtask=node_ptr.get_latest_info()['subtasks'][1:], # 这里去掉第一个子任务
                        )
                    else:
                        prompt = prompt_obj.generate_leaf_judge_done_prompt(
                            obs=cur_obs,
                            done_task_name=done_task_name,
                            previous_stage_task_name=node_ptr.task_name,
                            previous_stage_think=node_ptr.get_latest_info()['think'],
                        )
                else:
                    # 如果当前动作不是valid action, 则回溯错误信息
                    node_ptr = node_ptr.parent
                    during_down = False
                    # 生成下一轮的Prompt
                    prompt = prompt_obj.generate_leaf_up_fail_prompt(
                        obs=cur_obs,
                        fail_task_name=action,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_info()['think'],
                        remaining_subtask=node_ptr.get_latest_info()['subtasks'], # 这里不需要去掉第一个子任务，因为当前任务失败了
                    )
                    print('Fail to execute action:', action)
                    
            # 3. 判断是否非叶子结点已经完成(subtasks为空)
            elif not response['subtasks']:
                level -= 1
                if node_ptr.parent is None:
                    break
                # 更新状态
                during_down = False
                # 如果没有remaining_subtask, 则直接回溯
                done_task_name = node_ptr.task_name
                node_ptr = node_ptr.parent
                # while node_ptr and not node_ptr.get_latest_info()['subtasks'][1:]:
                #     done_task_list.append(node_ptr.task_name)
                #     node_ptr = node_ptr.parent
                if not node_ptr:
                    break
                # 生成下一轮的Prompt
                if node_ptr.get_latest_info()['subtasks'][1:]:
                    prompt = prompt_obj.generate_nonleaf_up_prompt(
                        done_task_name=done_task_name,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_info()['think'],
                        remaining_subtask=node_ptr.get_latest_info()['subtasks'][1:], # 这里去掉第一个子任务
                    )
                else:
                    prompt = prompt_obj.generate_nonleaf_judge_done_prompt(
                        done_task_name=done_task_name,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_info()['think'],
                    )
            # 4. 如果当前子任务没有完成，执行第一个子任务
            else:
                level += 1
                child = Node(task_name=response["subtasks"][0], parent=node_ptr)
                node_ptr.add_child(child)
                node_ptr = child
                during_down = True
                if level == max_level:
                    prompt = prompt_obj.generate_leaf_down_prompt(task_name=response["subtasks"][0])
                else:
                    prompt = prompt_obj.generate_down_prompt(task_name=response["subtasks"][0])
        except Exception as e:
            if type(e) == json.JSONDecodeError:
                #llm.batch_add([{"role": "system", "content": "Error occurred in parsing json, please check the format of your response."}])
                llm.truncated_chat_history.append({"role": "user", "content": "Error occurred in parsing json, please check the format of your response."})
            print("Error: ", e)
            pass

    save_tree_to_json(root, log_tree_json_file_path)
    llm.save_history_to_json(log_history_json_file_path)
    llm.save_cost_to_json(log_cost_json_file_path)