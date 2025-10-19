class Node:
    def __init__(self, task_name, parent=None):
        self.children = []
        self.parent = None
        self.info_list = []
        self.task_name = task_name
        self.obs_list = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def set_info(self, info):
        self.info_list.append(info)
    
    def get_latest_info(self):
        if len(self.info_list) == 0:
            return {"think": "", "subtasks": []}
        return self.info_list[-1]
    
    def set_obs(self, obs):
        self.obs_list.append(obs)
    
    def get_latest_obs(self):
        if len(self.obs_list) == 0:
            return None
        return self.obs_list[-1]
