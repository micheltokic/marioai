#!/usr/bin/env python
# coding: utf-8
import pathlib

import d3rlpy.dataset
import numpy as np

from get_paths import LevelPaths
from gym_setup import Env
from training_params import *

visible = True
try_other = True

init_dir = pathlib.Path("./exercise_offline_rl")
level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")
if try_other:
    level_paths_other: LevelPaths = LevelPaths(init_dir, "ClimbLevel.lvl")
    env_show = Env(visible=visible, level=str(level_paths_other.level), port=8080).env
else:
    env_show = Env(visible=visible, level=str(level_paths.level), port=8080).env

# print(f"level location={level}")


ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
                                    target_update_interval=target_update_interval,
                                    batch_size=batch_size).create()

name = 'DDQN_marioai_%s_%s_%s_%s_%s_v2' % (
level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs)
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
