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

if __name__ == '__main__':
    try:
        with subprocess.Popen(['java', '-jar', 'server.jar'], shell=True) as server:
            env = Env(visible=True, port=8080, level=level_path, run_server=False).env
            if USE_GAMEPAD:
                controller = GamepadController(env)
            else:
                controller = KeyboardController(env)
            while True:
                observation = env.reset()
                done = False
                action = controller.read()

                observations = [observation]
                actions = [action]
                rewards = [0]  # No reward at first time step, because no action was taken yet
                terminals = [done]

                while not done:
                    observation, reward, done, info = env.step(action)
                    action = controller.read()

                    observations.append(observation)
                    actions.append(action)
                    rewards.append(reward)
                    terminals.append(done)

                dataset_path = os.path.join("data", "datasets", os.path.split(level_path)[1] + ".h5")
                if os.path.isfile(dataset_path):
                    dataset = MDPDataset.load(dataset_path)
                    dataset.append(np.asarray(observations), np.asarray(actions), np.asarray(rewards),
                                   np.asarray(terminals))
                else:
                    dataset = MDPDataset(np.asarray(observations), np.asarray(actions), np.asarray(rewards),
                                         np.asarray(terminals), discrete_action=True)
                dataset.dump(dataset_path)
                stats = dataset.compute_stats()
                mean = stats['return']['mean']
                std = stats['return']['std']
                print(f'mean: {mean}, std: {std}')
    except ConnectionResetError:
        # Finish
        pass
