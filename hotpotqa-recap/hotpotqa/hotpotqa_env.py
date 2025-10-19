from hotpotqa import wrappers, wikienv
import requests

def create_fever_env(split: str):
    """Create a HotPotQA environment with logging and wrapping."""
    env = wikienv.WikiEnv()
    env = wrappers.FeverWrapper(env, split=split)
    env = wrappers.LoggingWrapper(env)
    return env

def create_hotpot_env(split: str):
    """Create a HotPotQA environment with logging and wrapping."""
    env = wikienv.WikiEnv()
    env = wrappers.HotPotQAWrapper(env, split=split)
    env = wrappers.LoggingWrapper(env)
    return env


def step(env, action):
    attempts = 0
    while attempts < 10:
        try:
            return env.step(action)
        except requests.exceptions.Timeout:
            attempts += 1


