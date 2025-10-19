import re
import json

from sweagent.agent.recap_node import Node

_quad_fence = re.compile(r'`+(?:json)?', re.IGNORECASE)

def remove_json_fence(text: str) -> str:
    """
    Remove the JSON fence from the text.
    """
    # Remove the JSON fence
    text = _quad_fence.sub('', text)
    return text

def tree_to_dict(node: Node):
    """
    将树结构转换为字典结构
    """
    if node is None:
        return None
    return {
        "task_name": node.task_name,
        "children": [tree_to_dict(child) for child in node.children],
        "info_list": node.info_list,
        "obs_list": node.obs_list
    }


def save_tree_to_json(node: Node, file_path: str):
    """
    将树结构保存为json文件
    """
    tree_dict = tree_to_dict(node)
    with open(file_path, "w") as f:
        json.dump(tree_dict, f, ensure_ascii=False, indent=4)


def print_tree(node:Node, level=0):
    """
    打印树结构
    """
    if node is None:
        return
    indent = "    " * level
    print(indent + f"Task: {node.task_name}")
    print(indent + f"Info: {node.info_list}")
    print(indent + f"Obs: {node.obs_list}")
    for child in node.children:
        print_tree(child, level + 1)
