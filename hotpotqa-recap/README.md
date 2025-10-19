# Running the code

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

3. Run ReCap:
   ```bash
   python main.py --conf ./conf/config.toml
   ```
   to change the start index, you can use the `--start_count` argument:
   ```bash
    python main.py --conf ./conf/config.toml --start_count 0
    ```
   
4. You can also edit the `conf/config.toml` file to change the configuration settings. The default settings are:
   ```toml
    seed = 42  # Random seed
    test_count = 200 # Number of test cases to generate
    max_retry = 10 # Maximum number of actions to perform
    split = 'dev' # Can be 'train', 'dev', or 'test'
   ```
   

# Running the baselines
1. Notebooks:
   - `React.ipynb`: React baseline
   - `baseline_act`: Act baseline
   - `baseline_cot`: Cot baseline
   - `baseline_standard`: Standard baseline
2. Edit `baseline_check_point_file` field in the notebook to point to the checkpoint file you want to use.
   - If it doesn't exist, it will be created and run a new experiment.