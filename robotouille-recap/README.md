# Setup

0. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
2. Set up the environment:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
    ```
# Run ReCap (Full Version)
1. In `./conf/base_evaluation.yaml`, set the `ablation` field to `"original"`
2. Run the following command:
    ```bash
    python main.py +experiments=ReAct/synchronous/[path-to-your-experiment] # for synchronous tasks
    ```
    ```bash
    python main.py +experiments=ReAct/asynchronous/[path-to-your-experiment] # for asynchronous tasks
    ```
   `path-to-your-experiment` should be replaced with the path to your experiment file. For example, if your experiment file is located at `./conf/experiments/ReAct/synchronous/last-reasoning-action-mpc.yaml`, you would run:
   ```bash
    python main.py +experiments=ReAct/synchronous/last-reasoning-action-mpc.yaml
    ```
3. The experiment file contains several configurable options. Some important ones are:
   - `environment_names`: The names of the tasks to run. You can specify multiple tasks
   - `optimal_steps`: The optimal steps for each task. This is pre-filled per task. You can uncomment the corresponding lines to use the optimal steps.
   - `testing_seeds`: The random seeds to use for testing. You can specify multiple seeds. The seeds we used are prefilled
   - `max_step_multiplier`: The maximum step multiplier for each task. This is the multiplier for the optimal steps. It indicates the maximum number of actions to perform.
   - You can ignore other fields.


# Run ReCap (Ablation Version)
1. In `./conf/base_evaluation.yaml`, set the `ablation` field to one of the followings:
   - `"nothink"`
   - `"nameonly"`
   - `"thinkmany"`
   - `"level2"`
   - `"level3"`
   - `"level4"`
   - `"level5"`
2. Run the following command:
    ```bash
    python main.py +experiments=ReAct/ablation-ours/[ablation-name]
    ```
   `ablation-name` should be replaced with the corresponding ablation name. You can check it out in `./conf/experiments/ReAct/ablation-ours/`

3. The configurable options are the same as the full version, with the following additional options:
   - `ablation`: The name of the ablation to run. This is already filled in the experiment file.
   - `ctx_len`: The maximum message history length.

# Prompt and Rule Files
1. Task description file: `./MATRIX/MATRIX/task_description.toml`
2. Few-shot examples file: `./MATRIX/MATRIX/prompts.py`. This file contains the few-shot examples for the full version and all ablation versions.
3. Rule file: `./agents/prompt_builder/prompts/ReAct/1.3.1-last-reasoning-action-mpc.yml`

# Credits
Part of this code is adapted from the original Robotouille repository: https://github.com/portal-cornell/robotouille

