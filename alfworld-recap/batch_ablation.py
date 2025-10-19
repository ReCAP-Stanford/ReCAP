#!/usr/bin/env python3
"""
A simple batch runner for ablation experiments: 
this script invokes main.py repeatedly with different module imports and parameter values,
collecting stdout/stderr into per-run log files.
"""
import subprocess
import itertools
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1) List the variants of modules you want to ablate
chatbots = [
    "max_level_2",
    "max_level_3",
    "max_level_4",
    "no_think",
    "no_tree",
    "think_many",
    "chatbot",
    # add more module names here
]

# 2) List the parameter values you want to sweep over
ctx_lens = [
    16,
    32,
    64,
    96,
    128,
    # add more parameter values here
]

# Ensure a logs directory exists
log_dir = "ablations_0514"
os.makedirs(log_dir, exist_ok=True)

# Prepare all (module, param) combinations
tasks = list(itertools.product(chatbots, ctx_lens))

# Function to run a single experiment with live streaming via tee
def run_experiment(module, param):
    log_file = os.path.join(log_dir, f"{module}_param{param}.log")
    # Build a subshell command that pipes through tee
    cmd_str = (
        f"python main.py base_config.yaml {module} {param} "
        f"2>&1 | tee {log_file}"
    )
    print(f"\n--- Starting: {module}, param={param} ---")
    # Use bash for piping and tee
    returncode = subprocess.call(cmd_str, shell=True, executable='/bin/bash')
    if returncode != 0:
        print(f"*** Warning: module={module}, param={param} exited with code {returncode} ***")
    return returncode == 0


def main():
    max_workers = os.cpu_count() or 4
    print(f"Launching up to {max_workers} concurrent jobs...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_experiment, m, p): (m, p) for m, p in tasks}
        for future in as_completed(futures):
            module, param = futures[future]
            try:
                success = future.result()
            except Exception as e:
                print(f"!!! Exception for module={module}, param={param}: {e}")
            else:
                status = "OK" if success else "FAILED"
                print(f"--- Finished: {module}, param={param} => {status} ---")

if __name__ == "__main__":
    main()
