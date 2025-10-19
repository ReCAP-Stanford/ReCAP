
from hotpotqa.hotpotqa_env import create_hotpot_env,create_fever_env, step
from MATRIX.MATRIX.session.SessionManager import SessionManager


env_name_map = {
    'hotpotqa': create_hotpot_env,
    'fever': create_fever_env
}
def run_hotpotqa(max_steps: int,
                 question_index: int,
                 rule_description: str,
                 system_description: str = '',
                 split: str = 'train',
                 env_name: str = 'hotpotqa',
                 ):

    env = env_name_map[env_name](split=split)
    question = env.reset(idx=question_index)

    done = False
    steps = 0


    session_manager = SessionManager(system_description, rule_description, question)
    obs_str = "No observation yet"


    str_valid_actions = ['Search', 'Lookup', 'Finish']

    action = "finish[]"
    info = None
    while not done and steps < max_steps:
        action = session_manager.step_with_obs(obs_str, str_valid_actions)

        if session_manager.is_ended():
            done = True
            break


        obs, r, done, info = step(env, action[0].lower() + action[1:])
        obs_str = obs.replace('\\n', '')
        if done:
            done = True
            break

    if not done or not info or not info['answer']:
        action = "finish[]"
        obs, r, d, info = step(env, "finish[]")



    return done, steps, info