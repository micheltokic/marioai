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

# from d3rlpy.metrics.scorer import evaluate_on_environment

visible = True

# # Training an Agent to play Super Mario with Offline Learning
# ---
#
# In this exercise you will learn how to use offline learning to train a neural network to play Super Mario.
# Its performance will then be compared with the results from the Q-Learning exercise.
# ## 0. Setup
#
# ### Requirements
#  - Java 8 (or later) runtime environment
#  - Python 3.6 (or later)
#  - Microsoft Visual C++ 14.0 (or later)
#
# You will be provided with both the .jar and the gym-marioai python package.
# ### Installation
# To setup this exercise we will use Pipenv.
# If you do not have pipenv installed please do so by running:
#
# ``pip install --user pipenv``
#
# After that please run (if not already done)
#
# ``pipenv install`` and
# ``pipenv run start``.
#
#
# in the root directory to start the Jupyter notebook containing the exercise.
#
# (pipfile set to python version 3.6 by default, can be edited if needed)
# In[15]:

# from d3rlpy.metrics.scorer import evaluate_on_environment
# get_ipython().run_line_magic('load_ext', 'tensorboard')
# get_ipython().run_line_magic('set_env', 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python')


# ## 1. Generating data
# First, you will have to generate some data for the neural network to train with.
#
# ### Level
# The level we will be using for this exercise will be a very easy one to minimize the training time.
#
# However, if you would like to try different levels, we encourage you to do so by changing the ``level`` variable below to a different one from the ``levels`` folder.

# In[16]:


# Setup global variables
# init_dir = pathlib.Path(__file__).parent
init_dir = pathlib.Path("./exercise_offline_rl")
level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")

print(f"level location={level_paths.level}")

# run_ddqn
dataset = getDataset()
# train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
print(len(dataset.episodes))

ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
                                    target_update_interval=target_update_interval,
                                    batch_size=batch_size).create()

# set environment in scorer function
env_train = Env(visible=visible, level=str(level_paths.level), port=8080).env
ddqn.build_with_dataset(dataset)
test_episodes = dataset.episodes[:30]
# set environment in scorer function
# only run right now, as there is no randomness in the game
env_evaluator = EnvironmentEvaluator(env_train, n_trials=1)

# evaluate algorithm on the environment

name = 'DDQN_marioai_%s_%s_%s_%s_%s_v2' % (level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs)
model_file = init_dir / pathlib.Path("data", "models", name + ".pt")
currentMax = -100000
ddqn_max = copy.deepcopy(ddqn)

fitter = ddqn.fitter(
    dataset,
    n_steps=n_steps_per_epoch * n_epochs,
    n_steps_per_epoch=n_steps_per_epoch,
    evaluators={'td_error': d3rlpy.metrics.TDErrorEvaluator(test_episodes),
                'value_scale': d3rlpy.metrics.AverageValueEstimationEvaluator(test_episodes),
                'environment': env_evaluator}
)

for epoch, metrics in fitter:
    print(f"{metrics.get('environment')=}")
    # FIXME: what is the correct value?
    if metrics.get("environment") > 400:
        ddqn.save_model(model_file)
        # For the purpose of the exercise the training will stop if the agent manages to complete the level
        print("A suitable model has been found.")
        break
