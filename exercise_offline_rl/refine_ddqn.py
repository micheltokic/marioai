#!/usr/bin/env python
# coding: utf-8
import copy
import pathlib

import d3rlpy.dataset
from d3rlpy.dataset import ReplayBuffer
from d3rlpy.dataset.buffers import InfiniteBuffer
from d3rlpy.metrics import EnvironmentEvaluator
from sklearn.model_selection import train_test_split

from data.datasets.getDatasets import getSpecificDataset
from get_paths import LevelPaths
from gym_setup import Env
from training_params import *

# from d3rlpy.metrics.scorer import evaluate_on_environment

visible = True

# Setup global variables
# init_dir = pathlib.Path(__file__).parent
init_dir = pathlib.Path("./exercise_offline_rl")
level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")

level_paths_other: LevelPaths = LevelPaths(init_dir, "ClimbLevel.lvl")

print(f"level location={level_paths.level}")

# run_ddqn
dataset = getSpecificDataset(level_paths_other.level_name)
train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
train_dataset = ReplayBuffer(InfiniteBuffer(), episodes=train_episodes)
print(f"{len(train_episodes)=}")
print(f"{len(test_episodes)=}")

# exit()

ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
                                    target_update_interval=target_update_interval,
                                    batch_size=batch_size).create()
# Needs to be rebuilt
ddqn.build_with_dataset(train_dataset)
# exit()

# set environment in scorer function
env_train = Env(visible=visible, level=str(level_paths_other.level), port=8080).env
# set environment in scorer function
# only run right now, as there is no randomness in the game
env_evaluator = EnvironmentEvaluator(env_train, n_trials=1)

# evaluate algorithm on the environment

name = 'DDQN_marioai_%s_%s_%s_%s' % (gamma, learning_rate, target_update_interval, n_epochs)
model_file = init_dir / pathlib.Path("data", "models", name + ".pt")
currentMax = -100000
ddqn_max = copy.deepcopy(ddqn)

ddqn.load_model(model_file)


fitter = ddqn.fitter(
    train_dataset,
    n_steps=n_steps_per_epoch * n_epochs,
    n_steps_per_epoch=n_steps_per_epoch,
    evaluators={'td_error': d3rlpy.metrics.TDErrorEvaluator(test_episodes),
                'value_scale': d3rlpy.metrics.AverageValueEstimationEvaluator(test_episodes),
                'environment': env_evaluator}
)

for epoch, metrics in fitter:
    current_reward = metrics.get("environment")
    print(f"{current_reward=}")
    if current_reward > currentMax:
        print("saving version to file")
        currentMax = current_reward
        ddqn.save_model(model_file)
    # FIXME: what is the correct value?
    if current_reward > 1000:
        # For the purpose of the exercise the training will stop if the agent manages to complete the level
        print("A suitable model has been found.")
        break
