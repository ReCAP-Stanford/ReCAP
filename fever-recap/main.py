import argparse
import toml
import os
from hotpotqa.hotpotqa_simulator import run_hotpotqa
import random
import time

from rich.console import Console
from rich.markup import escape

def main():

    parser = argparse.ArgumentParser(description="Process config file and parameters.")
    parser.add_argument("--conf", type=str, required=True, help="Path to the config path")
    parser.add_argument("--start_count", type=int, default=0, help="Start count for the test")
    args = parser.parse_args()


    config_path = args.conf
    start_count = args.start_count


    config = toml.load(config_path)


    seed = config.get("seed", 42)
    test_count = config.get("test_count", 10)
    max_retry = config.get("max_retry", 5)
    split = config.get("split", "train")


    idxs = list(range(7405))
    random.Random(seed).shuffle(idxs)

    rs = []
    infos = []
    old_time = time.time()
    correct_count = 0

    for i in idxs[start_count:test_count]:
        done, steps, info = run_hotpotqa(
            max_steps=max_retry,
            question_index=i,
            rule_description=config['rule_description'],
            system_description=config['system_description'],
            split=split,
            env_name=config['env_name'], #'hotpotqa' or 'fever'
        )

        agent_ans = info['answer'].strip()
        exact_match = info['em']
        correct_answer = info['gt_answer'].strip()
        
        console = Console()
        console.print(f'[red]GT: {escape(correct_answer)}[/red]')
        console.print(f'[green]Agent: {escape(agent_ans)}[/green]')
        
        
        #check if corect, ignore case

        if exact_match:
            correct = True
            correct_count += 1
        else:
            correct = False

        rs.append(1 if correct else 0)
        infos.append(info)


        print(sum(rs), len(rs), sum(rs) / len(rs), (time.time() - old_time) / len(rs))
        print('-----------')
        print()


    print(f'Final result: {sum(rs)}/{len(rs)} = {sum(rs) / len(rs)}')


if __name__ == "__main__":
    main()
