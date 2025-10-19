import subprocess
import os
from datasets import load_dataset
import sys
import argparse

DATASET_NAME = 'SWE-bench/SWE-bench_Verified'
DATASET_SPLIT = 'test'
RUN_SCRIPT_PATH = 'sweagent/run/run.py'
PROBLEM_STATEMENT_DIR = 'problem_statements'
PYTHON_EXECUTABLE = sys.executable


def create_github_repo_url(repo_string):
    return f"https://github.com/{repo_string}"

def prepare_problem_statement_file(instance_id, problem_text):
    if not os.path.exists(PROBLEM_STATEMENT_DIR):
        print(f"creating dir... '{PROBLEM_STATEMENT_DIR}' for problem statement...")
        os.makedirs(PROBLEM_STATEMENT_DIR)
    
    file_path = os.path.join(PROBLEM_STATEMENT_DIR, f"{instance_id}.md")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(problem_text)
    except IOError as e:
        print(f"!!!!!! error: cannot write problem statement in {file_path}! info: {e}")
        return None
        
    return file_path

def run_tasks_in_range(start_index, end_index):
    print(f"Loading '{DATASET_NAME}' (split: '{DATASET_SPLIT}')...")
    try:
        dataset = load_dataset(DATASET_NAME, split=DATASET_SPLIT)
        total_in_dataset = len(dataset)
        print(f"Load success, {total_in_dataset} tasks in total")
    except Exception as e:
        print(f"Failed to load, info: {e}")
        return

    if end_index is None:
        end_index = total_in_dataset
    if start_index < 0:
        start_index = 0
    if end_index > total_in_dataset:
        print(f"warning: index {end_index} exceeds total {total_in_dataset}, will run to the end")
        end_index = total_in_dataset
    if start_index >= end_index:
        print(f"error: start index ({start_index}) have to be smaller than end index ({end_index}). no task executed")
        return
    print(f"\nrunning task from {start_index} to {end_index-1}")
    tasks_to_process = dataset.select(range(start_index, end_index))
    total_tasks_to_run = len(tasks_to_process)
    if total_tasks_to_run == 0:
        print("no task to run for given indices")
        return

    print(f"running {total_tasks_to_run} tasks")

    for i, instance in enumerate(tasks_to_process):
        instance_id = instance['instance_id']
        repo_path = instance['repo']
        base_commit = instance['base_commit']
        problem_statement = instance['problem_statement']

        problem_file_path = prepare_problem_statement_file(instance_id, problem_statement)
        if not problem_file_path:
            print(f"skipping {instance_id} because cannot create problem statement")
            continue

        repo_url = create_github_repo_url(repo_path)
        
        print("\n" + "="*80)
        print(f"running task ({i+1}/{total_tasks_to_run} from batch, dataset index {start_index + i}): {instance_id}")
        print(f"  - Repo: {repo_url}")
        print(f"  - Base Commit: {base_commit}")
        print(f"  - Problem Statement File: {problem_file_path}")
        print("="*80 + "\n")

        command = [
            PYTHON_EXECUTABLE,
            RUN_SCRIPT_PATH,
            "run",
            "--agent.model.name=gpt-4.1",
            "--agent.model.per_instance_cost_limit=10.00",
            "--config=config/recap.yaml",
            f"--env.repo.github_url={repo_url}",
            f"--env.repo.base_commit={base_commit}",
            f"--problem_statement.path={problem_file_path}",
            f"--problem_statement.id={instance_id}"
        ]
        
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            return_code = process.poll()
            if return_code == 0:
                print(f"✅ task {instance_id} submit successfully")
            else:
                print(f"❌ task {instance_id} failed, code: {return_code}。")

        except FileNotFoundError:
            print(f"!!!!!! error: cannot find script '{RUN_SCRIPT_PATH}' or Python interpreter '{PYTHON_EXECUTABLE}'。")
            print("check 'RUN_SCRIPT_PATH' and 'PYTHON_EXECUTABLE' settings")
            break
        except Exception as e:
            print(f"!!!!!! task {instance_id} unknown error! {e}")
            continue
            
    print(f"\n🎉 {total_tasks_to_run} task(s) done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch run SWE-bench tasks, from i to j",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-s", "--start-index", 
        type=int, 
        default=0, 
        help="start index, inclusive, from 0\ndefault: 0"
    )
    parser.add_argument(
        "-e", "--end-index", 
        type=int, 
        default=None, 
        help="end index, not inclusive\ne.g. -s 0 -e 10 will run task 0 to 9\ndefault: to the end (500)"
    )
    args = parser.parse_args()
    run_tasks_in_range(start_index=args.start_index, end_index=args.end_index)
