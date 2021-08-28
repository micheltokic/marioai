
# here the player can play to generate data

from d3rlpy import dataset
from gym_marioai import levels
from gym_setup import Env
from d3rlpy.dataset import MDPDataset
import numpy as np

EPISODES = 10000

env = Env(visible=False, level=levels.cliff_level).env

observations = []
actions = []
rewards = []
terminals = []

for episode in range(0, EPISODES):
    observation = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        observations.append(observation)
        actions.append(action)
        rewards.append(reward)
        terminals.append(done)

    if episode % 50 == 0 and episode != 0:
        dataset = MDPDataset(np.asarray(observations), np.asarray(actions), np.asarray(rewards),np.asarray( terminals), discrete_action=True, episode_terminals=None)
        dataset.dump('exercise_2_1/data/datasets/random_data.h5')
        stats = dataset.compute_stats()
        mean = stats['return']['mean']
        std = stats['return']['std']
        print(f'mean: {mean}, std: {std}')
