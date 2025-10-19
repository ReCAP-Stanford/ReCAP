import json
def get_few_shot():
    with open('prompts/fever_matrix.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data