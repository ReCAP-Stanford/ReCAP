# Important
This code is adapted directly from the original Robotouille repository (https://github.com/portal-cornell/robotouille), with its rules and prompts adapted to the same ones used in the ReCAP paper to ensure fairness in the comparison. We also added an `Act` agent for the `Act` baseline. Below is the simplest runnable setup for the ReCAP paper. For more details, please refer to the original repository or the original README file at `README_original.md`.

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
# Run Baselines

```bash
python main.py +experiments=[baseline-name]/[mode]/[experiment-file-name]
```

- `baseline-name` should be replaced with the name of the baseline you want to run. The available baselines are:
  - `ReAct`: ReAct baseline
  - `Act`: Act baseline
  - `IO-CoT`: Cot baseline
  - `IO`: Standard baseline
  - `Adapt`: ADaPT baseline

- `mode` should be replaced with the type of tasks you want to run. The available modes are:
  - `synchronous`: Synchronous tasks
  - `asynchronous`: Asynchronous tasks

- `experiment-file-name` should be replaced with the name of the experiment file you want to run. They start with `original_` in the `./conf/experiments/[baseline-name]/[mode]/` folder. For example, if you want to run the ReAct baseline on the synchronous tasks #3, you would run:
    ```bash
    python main.py +experiments=ReAct/synchronous/original_3.yaml
    ```
    - Note that for Cot and Standard baselines (`IO-CoT` and `IO`), the experiment files have different naming conventions. You can check them out in the `./conf/experiments/[baseline-name]/[mode]/` folder.