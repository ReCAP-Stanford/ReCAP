import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re


from rich.console import Console

import json
alfworld_prompt_file = './MATRIX/MATRIX/alfworld_3prompts.json'
with open(alfworld_prompt_file, 'r') as f:
    d = json.load(f)

def build_tree_graph(node, graph=None, parent=None, parent_name=None):
    if graph is None:
        graph = nx.DiGraph()
    name = f"id:{node.id}: {node.name}"
    graph.add_node(name)
    if parent:
        graph.add_edge(parent_name, name)
    for child in node.children:
        build_tree_graph(child, graph, node, parent_name=name)
    return graph

def draw_tree_image(root_node):
    graph = build_tree_graph(root_node)
    pos = nx.spring_layout(graph)  #   graphviz_layout，  pygraphviz  
    plt.figure(figsize=(10, 5))
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


class SessionManager:
    def __init__(self, system_description=None, rule_description=None, environment_name=None, ablation=None, ctx_len=128):

        self.reset_session()
        self.system_description = system_description
        self.rule_description = rule_description

        if ablation == "max_level_2":
            from ..chatbot_max_level_2 import chatbot
            # self.chatbot = chatbot
        elif ablation == "max_level_3":
            from ..chatbot_max_level_3 import chatbot
            # self.chatbot = chatbot
        elif ablation == "max_level_4":
            from ..chatbot_max_level_4 import chatbot
            # self.chatbot = chatbot
        elif ablation == "no_think":
            from ..chatbot_no_think import chatbot
            # self.chatbot = chatbot
        elif ablation == "no_tree":
            from ..chatbot_no_tree import chatbot
            # self.chatbot = chatbot
        elif ablation == "think_many":
            from ..chatbot_think_many import chatbot
            # self.chatbot = chatbot
        else:
            from ..chatbot import chatbot
        self.chatbot = chatbot
        self.ctx_len = ctx_len

    def reset_session(self):
        self.context = None
        self.task = None
        self.generator = None
        self.last_action = None
        self.run_cnt = 0
        self.ended = False
        self.action_list = []

    def step_with_obs(self, obs, str_valid_actions, task_name):
        if self.ended:
            return None
        try:

            if self.run_cnt == 0:
                self.generator = self.chatbot(
                    system_prompt="",
                    few_shot_key=task_name,
                    task_name=re.search(r"Your\stask\sis\sto:\s*([a-zA-Z\s]+)", obs).group(1),
                    init_obs=obs,
                    rule=self.rule_description,
                    valid_actions=str_valid_actions,
                    ctx_len=self.ctx_len
                )

                action = next(self.generator)
                self.last_action = action
                self.action_list.append(action)
            else:
                action = self.generator.send((obs, str_valid_actions))
                self.last_action = action
                self.action_list.append(action)
        except StopIteration as e:
            try:
                self.last_action = f"{e.value}"
                self.action_list.append(self.last_action)
                self.ended = True
                print(f"ALL Actions: {self.action_list}")
            except:
                pass
        self.run_cnt += 1
        console = Console()
        console.print(f'[yellow]Action: {self.last_action}[/yellow]')
        return self.last_action

    def get_context_image(self):
        if self.context.root is None:
            return ""
        return draw_tree_image(self.context.root)
    
    def is_ended(self):
        return self.ended
