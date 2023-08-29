#!/usr/bin/env python
# coding: utf-8
import copy
import numpy as np
import pathlib

from d3rlpy.algos import DQN
import d3rlpy.dataset
from d3rlpy.dataset import MDPDataset, ReplayBuffer
from d3rlpy.metrics import EnvironmentEvaluator
from get_paths import LevelPaths
from sklearn.model_selection import train_test_split

from gym_setup import Env
from controller import GamepadController, KeyboardController
from data.datasets.getDatasets import getDataset
from training_params import *

visible=True
try_other=True

init_dir = pathlib.Path("./exercise_offline_rl")
level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")
if try_other:
    level_paths_other: LevelPaths = LevelPaths(init_dir, "ClimbLevel.lvl")
    env_show = Env(visible=visible, level=str(level_paths_other.level), port=8080).env
else:
    env_show = Env(visible=visible, level=str(level_paths.level), port=8080).env

# print(f"level location={level}")



ddqn = d3rlpy.algos.DoubleDQN.from_json("d3rlpy_logs/DoubleDQN_20230829203505/params.json")

name = 'DDQN_marioai_%s_%s_%s_%s_%s_v2' % (level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs)
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