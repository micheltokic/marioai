# here the player can play to generate data
import os
import subprocess

from d3rlpy.dataset import MDPDataset
from gym_setup import Env
from Controller.gamepad_controller import GamepadController
from Controller.keyboard_controller import KeyboardController
import numpy as np

USE_GAMEPAD = False

level_path = os.path.join("levels", "RoughTerrainLevel.lvl")

observations = []
actions = []
rewards = []
terminals = []

if __name__ == '__main__':
    try:
        with subprocess.Popen(['java', '-jar', 'server.jar'], shell=True) as server:
            env = Env(visible=True, port='8080', level=level_path, run_server=False).env
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

                    observations.append(next_state)
                    actions.append(action)
                    rewards.append(reward)
                    terminals.append(done)

                    total_reward += reward
                    next_action = controller.read()
                    state, action = next_state, next_action

                dataset = MDPDataset(np.asarray(observations), np.asarray(actions), np.asarray(rewards),
                                     np.asarray(terminals), discrete_action=True)
                dataset.dump('data/datasets/RoughTerrainData.h5')
                stats = dataset.compute_stats()
                mean = stats['return']['mean']
                std = stats['return']['std']
                print(f'mean: {mean}, std: {std}')
    except ConnectionResetError:
        # Finish
        pass
