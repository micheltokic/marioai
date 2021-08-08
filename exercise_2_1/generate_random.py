
# here the player can play to generate data

from d3rlpy import dataset
from gym_marioai import levels
from gym_setup import Env
from d3rlpy.dataset import MDPDataset
import numpy as np

EPISODES = 10000

env = Env(visible=False)
env = env.get_env()

observations = np.array([])
actions = np.array([])
rewards = np.array([])
terminals = np.array([])

for episode in range(0, EPISODES):
    observation = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        observations = np.append(observations, observation)
        actions = np.append(actions, action)
        rewards = np.append(rewards, reward)
        terminals = np.append(terminals, done)

    if episode % 50 == 0 and episode != 0:
        dataset = MDPDataset(np.reshape(observations, (-1, 1)), np.reshape(actions, (-1, 1)), np.reshape(
            rewards, (-1, 1)), np.reshape(terminals, (-1, 1)), discrete_action=True, episode_terminals=None)
        dataset.dump('exercise_2_1/data/random_data.h5')
        stats = dataset.compute_stats()
        mean = stats['return']['mean']
        std = stats['return']['std']
        print(f'mean: {mean}, std: {std}')
