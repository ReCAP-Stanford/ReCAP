# Running the code

0. Create a virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

1. Install the required packages

   ```bash
   pip install .
   ```

2. Setup the environment variable

   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the code:

   ```bash
   python main.py base_config.yaml
   ```

# Running Ablation Studies
```
python main.py base_config.yaml --ablation [ablation_name]
```
- `ablation_name` can be one of the following:
  - `max_level_2`
  - `max_level_3`
  - `max_level_4`
  - `no_think`
  - `no_tree`
  - `think_many`

# Running the baseline
- To run ReAct, use the following command:
```bash
cd ./react_alfworld
python react.py base_config_react.yaml
```

- To run Act, use the following command:
```bash
cd ./act_alfworld
python act.py base_config_react.yaml
```



# Credits
- The baseline code is adapted from https://github.com/ysymyth/ReAct

