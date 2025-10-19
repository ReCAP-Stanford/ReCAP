# Setup
1. download Docker
2. create add keys in a .env
3. make sure your working directory is in swebench-recap
```bash
uv sync
source .venv/bin/activate
python run_swe_bench_tasks.py
```
4. feel free to config and collect results using `collect_predictions.py`

# Prompt and Rule Files
`swebench-recap/config/recap.yaml`

# Credits
Part of this code is adapted from the original SWE-agent repository: https://github.com/SWE-agent/SWE-agent