# showcase the current model

from gym_setup import Env
from qlearner import QLearner

env = Env(visible=True)
env = env.get_env()

while True:
    state = env.reset()
    done = False
    total_reward = 0
    action = env.NOTHING
    q = QLearner(env)
    q.load('exercise_2/data/trained')
    while not done:
        next_state, reward, done, info = env.step(action)
        total_reward += reward
        next_action = q.choose_action(state)
        state, action = next_state, next_action
        print(total_reward)

















