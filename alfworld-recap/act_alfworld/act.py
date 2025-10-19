import os
import openai
import tiktoken


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

usage_history = []
log_cost = False

def save_cost_to_json(file_path: str = "cost.json"):
    """
     json 
    """
    with open(file_path, "w") as f:
        json.dump(usage_history, f, ensure_ascii=False, indent=4)

from together import Together
#client = Together()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def llm(histroy, stop=["\n"], model="gpt-4o"):
    success = False
    while not success:
        try:
            if log_cost:
                prompt_tokens = count_chat_tokens(history, model)

            new_msg = {'role': 'assistant', 'content': '\n<think>\n\n</think>\n\n'}
            histroy.append(new_msg)
            
            response = client.chat.completions.create(
                model=model,
                messages=histroy,
                stop=stop,
                response_format={"type": "json_object"},
    
            )
                        
            response = response.choices[0].message.content
            
            histroy.append({'role': 'assistant', 'content': response})
            success = True
        except openai.BadRequestError as e:
            error_code = e.code
            if error_code == 'context_length_exceeded':
                assert len(histroy) > 3, "The starter prompt is too long."
                # Remove the first and second element
                del histroy[2:34]

            else:
                raise e # Raise other errors for user to handle
        except Exception as e:
            
            raise e
        if log_cost:
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
            usage_history.append(usage)
    return response

from alfworld.agents.environment import get_environment
import alfworld.agents.modules.generic as generic

# load config
config = generic.load_config()
task_cnt_map = {
    1: 24,
    2: 18,
    3: 31,
    4: 23,
    5: 21,
    6: 17
}

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



cur_task = [1,2,3,4,5,6]
config['env']['task_types'] = cur_task
env_type = config['env']['type'] # 'AlfredTWEnv' or 'AlfredThorEnv' or 'AlfredHybrid'
    
split = "eval_out_of_distribution"

env = get_environment(env_type)(config, train_eval=split)
env = env.init_env(batch_size=1)

def process_ob(ob):
    if ob.startswith('You arrive at loc '):
        ob = ob[ob.find('. ')+2:]    
    return ob


import json
prompt_file = 'alfworld_3prompts_act.json'
#prompt_file = 'alfworld_3prompts_act.json'
with open(prompt_file, 'r') as f:
    d = json.load(f)

import sys

def generate_init_prompt(init_obs: str):

    return f"""
        
Here's the rule of the environment:
You can only pick up one item at a time. Always use Inventory to check what you have in possesion when you are not sure or plan to pick up an item.

Generate a json object with 'action' field. For example:

{{"action": "pick up the item"}}

Here is the task.

{init_obs}
"""

def alfworld_run(history, to_print=True, ob='', valid_actions=''):
    if to_print:
        sys.stdout.flush()
    i = 0
    while i < 50:
        action_str = llm(history, stop=['\n']).strip()

        try:
            response = json.loads(remove_json_fence(action_str))
        except Exception as e:
            response = {'action': 'json parse error', 'error_message': str(e)}
            
            
        done = False
        if 'action' in response:
            action = response['action']
            if not action:
                action = 'error'
            observation, reward, done, info = env.step([action])
                
            valid_actions = "\n".join(info['admissible_commands'][0])
            ob, reward, done = process_ob(observation[0]), info['won'][0], done[0]
            
            if 'error_message' in response:
                ob = f"""Your output is not a valid JSON object. Please ensure your output is a valid JSON object with an 'action' field."""    
                i += 1
            elif action not in info['admissible_commands'][0]:
                i += 1
                ob = f"""{ob}
Because your output is not included in the valid actions provided in the observation. Your assumptions may not be valid.
Potential cause of the problem might be:
1. The action name is not the EXACT match of the valid action name.
2. You are thinking but your output does not start with "Thought:"
Valid Actions:
{valid_actions}
"""
            else:
                ob = f"{ob}\n\nValid Actions:\n{valid_actions}"
                i += 1
                
            if to_print:
                print(f'Act {i}: {action}')
                sys.stdout.flush()
        
        if 'think' in response:
            ob = 'OK.'

        history.append({"role": "user", "content": ob})
        if done:
            return reward
    return 0


prefixes = {
    'pick_and_place': 'put',
    'pick_clean_then_place': 'clean',
    'pick_heat_then_place': 'heat',
    'pick_cool_then_place': 'cool',
    'look_at_obj': 'examine',
    'pick_two_obj': 'puttwo'
}
cnts = [0] * 6
rs = [0] * 6


def parse_fewshot_to_json(fewshot_str):
    """
    Parses a few-shot string into a dictionary.
    The expected format is:
    - Each example is separated by two newlines.
    - Each example has a 'role' and 'content'.
    """
    examples = fewshot_str.strip().split('\n')
    user_start = examples[0] + '\n' + examples[1]
    parsed_examples = []
    
    #start from line 2 to skip the first example
    for i in range(2, len(examples)):
        line = examples[i].strip()


def parse_fewshot(fewshot_str):
    fewshot_lines = fewshot_str.strip().split('\n')
    n = len(fewshot_lines)
    i = 0
    ans = []
    is_last_think = False
    while i < n:
        l = i
        i += 1
        while i < n and not (fewshot_lines[i][:4] == 'user' or fewshot_lines[i][:9] == 'assistant'):
            i += 1
        tmp = '\n'.join(fewshot_lines[l:i])
        if tmp[:4] == 'user':
            if is_last_think:
                continue
            
            ans.append({'role': 'user', 'content': tmp[5:].strip()})
        elif tmp[:9] == 'assistant':
            start = tmp[10:].strip()
            if start.startswith('think:'):
                is_last_think = True
                continue
            else:
                is_last_think = False
                content = json.dumps({'action': start})
            ans.append({'role': 'assistant', 'content': content})
    return ans


total = 0
for task_id in cur_task:
    total += task_cnt_map[task_id]
    
for _ in range(total):
    ob, info = env.reset()
    ob = '\n'.join(ob[0].split('\n\n')[1:])
    valid_actions = "\n".join(info['admissible_commands'][0])
    name = '/'.join(info['extra.gamefile'][0].split('/')[-3:-1])
    print(name)
    for i, (k, v) in enumerate(prefixes.items()):
        if name.startswith(k):
            history = []
            fewshot0 = d[f'react_{v}_0']
            
            fewshot_list = parse_fewshot(fewshot0)
            
            fewshot0 = '\n'.join(f"{msg['role']}: {msg['content']}" for msg in fewshot_list)
            
            history.append({"role": "user", "content": f"Interact with a household to solve a task. Return a json object with 'action' field. Here is one example.\n{fewshot0}"})
            history.append({"role": "user", "content": generate_init_prompt(f"{ob}\n\nValid Actions:\n{valid_actions}")})
            print(k, v)
            r = alfworld_run(history, ob=ob, valid_actions=valid_actions)
            rs[i] += r
            cnts[i] += 1
            break
    print(_+1, 'r', r, 'rs', rs, 'cnts', cnts, 'sum(rs)/sum(cnts)', sum(rs) / sum(cnts))
    print('------------\n')

if log_cost:
    log_dir = f"logs"
    log_cost_json_file_path = f"{log_dir}/cost_react_gpt4o_task{cur_task}.json"
    save_cost_to_json(log_cost_json_file_path)