import time
import argparse
import os
import re
import yaml
import numpy as np
from alfworld.agents.environment import get_environment
# import alfworld.agents.modules.generic as generic

from MATRIX.MATRIX.session.SessionManager import SessionManager

prefixes = {
    'pick_and_place': 'matrix_put_0',
    'pick_clean_then_place': 'matrix_clean_0',
    'pick_heat_then_place': 'matrix_heat_0',
    'pick_cool_then_place': 'matrix_cool_0',
    'look_at_obj': 'matrix_examine_0',
    'pick_two_obj': 'matrix_puttwo_0'
}
cnts = [0] * 6
rs = [0] * 6

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("task_number", help="task number")
    parser.add_argument("config_file", help="path to config file")
    # parser.add_argument("chatbot", help="ablation type")
    # parser.add_argument("ctx_len", help="ctx_len")
    parser.add_argument("-a", "--ablation", help="ablation type", default="default")
    parser.add_argument("-p", "--params", nargs="+", metavar="my.setting=value", default=[],
                        help="override params of the config file,"
                             " e.g. -p 'training.gamma=0.95'")
    args = parser.parse_args()
    assert os.path.exists(args.config_file), "Invalid config file"
    with open(args.config_file) as reader:
        config = yaml.safe_load(reader)
    # Parse overriden params.
    for param in args.params:
        fqn_key, value = param.split("=")
        entry_to_change = config
        keys = fqn_key.split(".")
        for k in keys[:-1]:
            entry_to_change = entry_to_change[k]
        entry_to_change[keys[-1]] = value

    # load config
    task_cnt_map = {
        1: 24,
        2: 18,
        3: 31,
        4: 23,
        5: 21,
        6: 17
    }
    cur_tasks = [1, 2, 3, 4, 5, 6]
    # cur_tasks = [1, 2]
    # cur_tasks = [3, 4]
    # cur_tasks = [5, 6]
    # cur_task = int(args.task_number)
    config['env']['task_types'] = cur_tasks
    # total_task = task_cnt_map[cur_tasks[0]] + task_cnt_map[cur_tasks[1]]
    total_task = sum([task_cnt_map[i] for i in cur_tasks])
    # config = generic.load_config()
    env_type = config['env']['type'] # 'AlfredTWEnv' or 'AlfredThorEnv' or 'AlfredHybrid'

    # setup environment
    env = get_environment(env_type)(config, train_eval='eval_out_of_distribution')
    env = env.init_env(batch_size=1)

    session_manager = SessionManager(rule_description="You can only pick up one item at a time. Always use Inventory to check what you have in possesion when you are not sure or plan to pick up an item.",
                                     ablation=args.ablation,
                                     ctx_len=128)
    
    def alfworld_run(obs, command_str, task_name):
        for i in range(1, 50):
            action_str = session_manager.step_with_obs(f"{obs}\n\nValid Actions:\n{command_str}", command_str.split('\n'), task_name)
            if not action_str:
                return 0
            obs, scores, dones, infos = env.step([action_str])
            if dones[0]:
                return scores[0]
            # get random actions from admissible 'valid' commands (not available for AlfredThorEnv)
            admissible_commands = list(infos['admissible_commands']) # note: BUTLER generates commands word-by-word without using admissible_commands
            command_str = "\n".join(admissible_commands[0])
        return 0

    start_time = time.perf_counter()
    # for _ in range(task_cnt_map[cur_task]):
    for _ in range(total_task):
        # interact
        obs, infos = env.reset()
        session_manager.reset_session()
        # get random actions from admissible 'valid' commands (not available for AlfredThorEnv)
        admissible_commands = list(infos['admissible_commands']) # note: BUTLER generates commands word-by-word without using admissible_commands

        command_str = "\n".join(admissible_commands[0])
        obs = '\n'.join(obs[0].split('\n\n')[1:])
        name = '/'.join(infos['extra.gamefile'][0].split('/')[-3:-1])
        for i, (k, v) in enumerate(prefixes.items()):
            if name.startswith(k):
                print(re.search(r"Your\stask\sis\sto:\s*([a-zA-Z\s]+)", obs).group(1))
                r = alfworld_run(obs, command_str, task_name=v)
                rs[i] += r
                cnts[i] += 1
                break
        print(_+1, 'r', r, 'rs', rs, 'cnts', cnts, 'sum(rs)/sum(cnts)', sum(rs) / sum(cnts))
        print('------------\n')
    end_time = time.perf_counter()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()