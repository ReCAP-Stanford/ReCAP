from .bfs_agent import BFSAgent
from .human import Human
from .IO_agent import IOAgent
from .IOCoT_agent import IOCoTAgent
from .ReAct_agent import ReActAgent
from .Reflexion_agent import ReflexionAgent
from .Act_agent import ActAgent
from .ADaPT_agent import ADaPTAgent
# Modify this dictionary to register a custom agent
NAME_TO_AGENT = {
    "bfs": BFSAgent,
    "human": Human,
    "io": IOAgent,
    "io-cot": IOCoTAgent,
    "ReAct": ReActAgent,
    "Reflexion": ReflexionAgent,
    "Act": ActAgent,
    "Adapt": ADaPTAgent
}