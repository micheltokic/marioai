#!/usr/bin/env python
# coding: utf-8
import copy
import numpy as np
import pathlib

from d3rlpy.algos import DQN
import d3rlpy.dataset
from d3rlpy.dataset import MDPDataset, ReplayBuffer
from d3rlpy.metrics import EnvironmentEvaluator
# from d3rlpy.metrics.scorer import evaluate_on_environment
from sklearn.model_selection import train_test_split

from gym_setup import Env
from controller import GamepadController, KeyboardController
from data.datasets.getDatasets import getDataset

init_dir = pathlib.Path("./exercise_offline_rl")
level = init_dir / pathlib.Path("levels", "CliffsAndEnemiesLevel.lvl")
dataset_path = init_dir / pathlib.Path("data", "datasets", level.stem + ".h5")
dataset_path_rand = init_dir / pathlib.Path("data", "datasets", level.stem + ".random.h5")

print(f"level location={level}")

# Training parameters
n_epochs = 10  # <--- change here if you want to train more / less
n_steps_per_epoch = 1000
test_size = 0.1  # percentage of episodes not used for training

# DQN parameters
learning_rate = 0.0003  # to what extent the agent overrides old information with new information
gamma = 0.99  # discount factor, how important future rewards are
target_update_interval = 3000  # interval of steps that the agent uses to update target network
batch_size = 2  # size of training examples utilized in one iteration
use_gpu = False  # usage of gpu to train

env_show = Env(visible=False, level=str(level), port=8080).env

ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
          target_update_interval=target_update_interval,
          batch_size=batch_size).create()
ddqn.build_with_dataset(getDataset())

name = 'DDQN_marioai_%s_%s_%s_%s_%s' % (level.stem, gamma, learning_rate, target_update_interval, n_epochs)
ddqn.load_model(init_dir / pathlib.Path("data") / "models" / f"{name}.pt")

try:
    while True:
        observation, _ = env_show.reset()

        done = False
        total_reward = 0
        while not done:
            predict_action = ddqn.predict(observation[np.newaxis, :])[0]
            observation, reward, done, truncated, info = env_show.step(predict_action)
            total_reward += reward
        print(f'finished episode, total_reward: {total_reward}')
except ConnectionResetError:
    print("Window closed.")