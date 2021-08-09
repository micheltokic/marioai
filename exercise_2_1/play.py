
# here the player can play to generate data
from d3rlpy.dataset import MDPDataset
from gym_setup import Env
from Controller.gamepad_controller import GamepadController
from Controller.keyboard_controller import KeyboardController
import numpy as np

USE_GAMEPAD = False

env = Env()
env = env.get_env()

observations = np.array([])
actions = np.array([])
rewards = np.array([])
terminals = np.array([])

if USE_GAMEPAD:
    controller = GamepadController(env)
else:
    controller = KeyboardController(env)

while True:
    state = env.reset()
    done = False
    total_reward = 0
    action = env.NOTHING

    while not done:
        next_state, reward, done, info = env.step(action)

        observations = np.append(observations, next_state)
        actions = np.append(actions, action)
        rewards = np.append(rewards, reward)
        terminals = np.append(terminals, done)

        total_reward += reward
        next_action = controller.read()
        state, action = next_state, next_action

    dataset = MDPDataset(np.reshape(observations, (-1, 1)), np.reshape(actions, (-1, 1)), np.reshape(
    rewards, (-1, 1)), np.reshape(terminals, (-1, 1)), discrete_action=True, episode_terminals=None)
    dataset.dump('exercise_2_1/data/player_data.h5')
    stats = dataset.compute_stats()
    mean = stats['return']['mean']
    std = stats['return']['std']
    print(f'mean: {mean}, std: {std}')










