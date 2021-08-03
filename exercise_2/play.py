from os import system, times
import os
from gym_setup import Env
from qlearner import QLearner
from Controller.gamepad_controller import GamepadController
from Controller.keyboard_controller import KeyboardController


USE_GAMEPAD = False

env = Env()
env = env.get_env()

while True:
    state = env.reset()
    done = False
    total_reward = 0
    action = env.NOTHING
    q = QLearner(env)
    if USE_GAMEPAD:
        controller = GamepadController(env)
    else:
        controller = KeyboardController(env)

    while not done:
        next_state, reward, done, info = env.step(action)
        total_reward += reward
        next_action = controller.read()
        q.train(state, action, reward, next_state, next_action)
        state, action = next_state, next_action

    print(f'finished episode, total_reward: {total_reward}')
    q.save('exercise_2/data/userdata')
    print(q)










