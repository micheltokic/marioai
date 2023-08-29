#!/usr/bin/env python
# coding: utf-8
import copy
import pathlib

import d3rlpy.dataset
from d3rlpy.metrics import EnvironmentEvaluator

from data.datasets.getDatasets import getDataset
from get_paths import LevelPaths
from gym_setup import Env
from training_params import *

visible = True


# Setup global variables
# init_dir = pathlib.Path(__file__).parent
init_dir = pathlib.Path("./exercise_offline_rl")
level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")

print(f"level location={level_paths.level}")

# run_ddqn
dataset = getDataset()
# train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
print(len(dataset.episodes))

ddpg = d3rlpy.algos.DDPGConfig(learning_rate=learning_rate, gamma=gamma,
                                    target_update_interval=target_update_interval,
                                    batch_size=batch_size).create()

# set environment in scorer function
env_train = Env(visible=visible, level=str(level_paths.level), port=8080).env
ddpg.build_with_dataset(dataset)
test_episodes = dataset.episodes[:30]
# set environment in scorer function
# FIXME: is this correct? The evaluator only runs the same example multiple times
env_evaluator = EnvironmentEvaluator(env_train)

# evaluate algorithm on the environment

name = 'DDQN_marioai_%s_%s_%s_%s_%s' % (level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs)
model_file = init_dir / pathlib.Path("data", "models", name + ".pt")
currentMax = -100000
ddqn_max = copy.deepcopy(ddpg)

fitter = ddpg.fitter(
    dataset,
    n_steps=n_steps_per_epoch * n_epochs,
    n_steps_per_epoch=n_steps_per_epoch,
    evaluators={'td_error': d3rlpy.metrics.TDErrorEvaluator(test_episodes),
                'value_scale': d3rlpy.metrics.AverageValueEstimationEvaluator(test_episodes),
                'environment': env_evaluator}
)

for epoch, metrics in fitter:
    print(f"{metrics.get('environment')=}")
    if metrics.get("environment") > currentMax:
        currentMax = metrics.get("environment")
        ddqn_max.copy_q_function_from(ddpg)
        # FIXME: would this be better?
        # ddpg.copy_q_function_from(ddqn_max)
    else:
        # FIXME: why is this needed?
        ddpg.copy_q_function_from(ddqn_max)
    ddpg.save_model(model_file)
    # FIXME: what is the correct value?
    if currentMax > 300:
        # For the purpose of the exercise the training will stop if the agent manages to complete the level
        print("A suitable model has been found.")
        break
