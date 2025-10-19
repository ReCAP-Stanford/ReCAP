import os
import json
import openai
from typing import List

from .prompt_llm import *

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


def call_llm(user_prompt, history, client, model):
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
            if len(truncated_history) > 32:
                # Remove the first and second element
                del truncated_history[1:3]
            truncated_history.append({'role': 'user', 'content': user_prompt})
            response = client.chat.completions.create(
                model=model,
                messages=history,
                # temperature=0.5,
                # top_p=0.9,
                # n=1,
                response_format={"type": "json_object"},
            )
            response = response.choices[0].message.content
            truncated_history.append({'role': 'assistant', 'content': response})
            success = True
        except openai.BadRequestError as e:
            error_code = e.code
            if error_code == 'context_length_exceeded':
                assert len(truncated_history) > 3, "The starter prompt is too long."
                # Remove the first and second element
                del truncated_history[1:33]
                if len(truncated_history) > 2:
                    # remove last element (the input prompt), because the same prompt will be added in the next iteration
                    del truncated_history[-1]

            else:
                raise e # Raise other errors for user to handle
    return response, truncated_history


class ChatGPTWithMemory:
    def __init__(self, fixed_prompt):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.fixed_prompt = fixed_prompt
        self.truncated_chat_history = [fixed_prompt]

    def invoke(self, user_prompt: str) -> str:
        response, self.truncated_chat_history = call_llm(user_prompt, self.truncated_chat_history, self.client, "gpt-4o")
        return response

    def reset(self):
        """重置对话历史"""
        self.truncated_chat_history = [self.fixed_prompt]
    
    def save_history_to_json(self, file_path: str = "history.json"):
        """
        将历史记录保存到json文件
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.truncated_chat_history, f, ensure_ascii=False, indent=4)


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
    
    def get_latest_obs(self, size=1):
        if len(self.obs_list) == 0:
            return None
        return self.obs_list[-1]
    
    def get_latest_think(self, size=100):
        if len(self.info_list) == 0:
            return None
        size = min(size, len(self.info_list))
        return '\n'.join(f"{i+1}. {info['think']}" for i, info in enumerate(self.info_list[-size:]))


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
    with open(file_path, "w", encoding="utf-8") as f:
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

Now you need to find the answer for the following question using the actions I provide. Here is the description:
{task_name}

Now, start the task. Please firstly generate a list of general subtasks to accomplish the task.
"""
    
     
    def generate_down_prompt(self, task_name: str):
        return f"""OK.

Your current task: {task_name}

We wish you to generate a list of subtasks for the current task.
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
        return f"""You have completed the task: {done_task_name}

Here is the result:
{obs}

Now, you return to the parent task:
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

Your remaining subtasks:
{remaining_subtask_str}

We wish you to refine your list of subtasks based on the latest observation to achieve your goal. If there are no remaining subtasks, you need to check whether the current goal has been achieved. If yes, simply return an empty list of subtasks. If not, return the subtasks required to accomplish the current goal. Do not generate any subtasks beyond the scope of the current task.
"""
    
    def generate_nonleaf_judge_done_prompt(self, 
                            done_task_name,
                            previous_stage_task_name: str,
                            previous_stage_think: str):
        return f"""You have successfully completed the task: {done_task_name}

Now, you return to the previous stage.
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

There are no remaining subtasks for the current task. Please determine whether the task has been completed. If it has, set the subtasks to an empty list; if not, generate the necessary subtasks required to complete the current task.
"""
    def generate_leaf_judge_done_prompt(self,
                            obs,
                            done_task_name,
                            previous_stage_task_name: str,
                            previous_stage_think: str):
        return f"""You have completed the task: {done_task_name}

Here is the result:
{obs}

Now, you return to the previous stage.
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

{obs}

Now, you return to the previous stage.
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
        return f"""You have completed the task: {done_task_name}
    
The result shows in the previous context.

Now, you return to the parent task:
Your current task: {previous_stage_task_name}

Your previous think: {previous_stage_think}

Your remaining subtasks:
{remaining_subtask_str}

We wish you to refine your list of subtasks based on the latest observation to achieve your goal. Do not generate any subtasks beyond the scope of the current task.
"""


def check_valid_action(action: str, valid_actions: List[str]) -> bool:
    #action can be: Search[entity], Lookup[keyword], Finish[answer]
    pattern = r"^(Search|Lookup|Finish)\[.*\]$"
    action = action.strip()
    return bool(re.match(pattern, action))

def chatbot(system_prompt: str, few_shot_list, task_name: str, init_obs: str, rule: str, valid_actions: List[str]):
    #temp rule overfit

     
    cur_time = time.strftime('%Y%m%d_%H%M%S')
    log_tree_json_file_path = f"logs/tree_{cur_time}.json"
    log_history_json_file_path = f"logs/history_{cur_time}.json"
    
    # Start
    #few_shot_str = '\n'.join(f"{d['role']}: {d['content']}" for d in few_shot_list)
    few_shot_str = str(few_shot_list)
    few_shot_str = f"""Here is a demo:
{few_shot_str}

END OF DEMO.
    """
    llm = ChatGPTWithMemory(fixed_prompt={'role': 'user', 'content': few_shot_str})
    prompt_obj = Prompt()
     
    prompt = prompt_obj.generate_init_prompt(
        task_name=task_name,
        init_obs=init_obs,
        rule=rule,
        system_prompt=system_prompt
    )


     
    root = Node(task_name=task_name, parent=None)
     
    node_ptr = root  
    cur_obs = init_obs  
    during_down = True  
    invoke_cnt = 0  
    while node_ptr:
         
        invoke_cnt += 1
         
        if invoke_cnt % 10 == 0:
            rule_str = f"""Since we’ve gone through many rounds of dialogue, here’s a reminder to prevent you from forgetting the operation rules. The rules are as follows:

{rule}

END OF RULE

"""
            prompt = rule_str + prompt
        
        response = llm.invoke(prompt)
        
         
         
        #     "think": str
        #     "subtasks": [str]
        # }

        try:
            response = json.loads(remove_json_fence(response))
             
             
            node_ptr.set_info(response)
            node_ptr.set_obs(cur_obs)
            #pretty print response
            print(json.dumps(response, indent=4, ensure_ascii=False))
             
            if during_down and len(response['subtasks']) == 1:
                action = response["subtasks"][0]
                if check_valid_action(action, valid_actions):
                     
                    save_tree_to_json(root, log_tree_json_file_path)
                    llm.save_history_to_json(log_history_json_file_path)
                     
                    cur_obs, valid_actions = yield action
                     
                    during_down = False
                    print('new obs:', cur_obs)
                     
                    done_task_name = node_ptr.task_name
                    node_ptr = node_ptr.parent
                    if not node_ptr:
                        break
                    
                     
                    if node_ptr.get_latest_info()['subtasks'][1:]:
                        prompt = prompt_obj.generate_leaf_up_prompt(
                            obs=cur_obs,
                            done_task_name=done_task_name,
                            previous_stage_task_name=node_ptr.task_name,
                            previous_stage_think=node_ptr.get_latest_think(),
                            remaining_subtask=node_ptr.get_latest_info()['subtasks'][1:],  
                        )
                    else:
                        prompt = prompt_obj.generate_leaf_judge_done_prompt(
                            obs=cur_obs,
                            done_task_name=done_task_name,
                            previous_stage_task_name=node_ptr.task_name,
                            previous_stage_think=node_ptr.get_latest_think(),
                        )
                else:
                     
                    node_ptr = node_ptr.parent
                    during_down = False
                     
                    prompt = prompt_obj.generate_leaf_up_fail_prompt(
                        obs=cur_obs,
                        fail_task_name=action,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_think(),
                        remaining_subtask=node_ptr.get_latest_info()['subtasks'],  
                    )
                    print('Fail to execute action:', action)
                    
             
            elif not response['subtasks']:
                if node_ptr.parent is None:
                    break
                 
                during_down = False
                 
                done_task_name = node_ptr.task_name
                node_ptr = node_ptr.parent
                # while node_ptr and not node_ptr.get_latest_info()['subtasks'][1:]:
                #     done_task_list.append(node_ptr.task_name)
                #     node_ptr = node_ptr.parent
                if not node_ptr:
                    break
                 
                if node_ptr.get_latest_info()['subtasks'][1:]:
                    prompt = prompt_obj.generate_nonleaf_up_prompt(
                        done_task_name=done_task_name,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_think(),
                        remaining_subtask=node_ptr.get_latest_info()['subtasks'][1:],  
                    )
                else:
                    prompt = prompt_obj.generate_nonleaf_judge_done_prompt(
                        done_task_name=done_task_name,
                        previous_stage_task_name=node_ptr.task_name,
                        previous_stage_think=node_ptr.get_latest_think(),
                    )
             
            else:
                child = Node(task_name=response["subtasks"][0], parent=node_ptr)
                node_ptr.add_child(child)
                node_ptr = child
                during_down = True
                prompt = prompt_obj.generate_down_prompt(task_name=response["subtasks"][0])
        except Exception as e:
            if type(e) == json.JSONDecodeError:
                #llm.batch_add([{"role": "system", "content": "Error occurred in parsing json, please check the format of your response."}])
                llm.truncated_chat_history.append({"role": "user", "content": "Error occurred in parsing json, please check the format of your response."})
            else:
                llm.truncated_chat_history.append({"role": "user", "content": f"An error occurred: {e}. Please retry."})
            print("Error: ", e)
            #raise e
            pass
    try:
        response = llm.invoke("Now, generate the final answer using Finish action. You must return the answer in your subtasks as concreate as possible, do not output long sentence.")
        response = json.loads(remove_json_fence(response))
        answer = response['subtasks'][0]
        print("Final answer:", response)    

        save_tree_to_json(root, log_tree_json_file_path)
        llm.save_history_to_json(log_history_json_file_path)
        yield answer
    except Exception as e:
        return