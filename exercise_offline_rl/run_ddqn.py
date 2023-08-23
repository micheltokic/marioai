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
level = init_dir / pathlib.Path("levels", "CliffsAndEnemiesLevel.lvl")
dataset_path = init_dir / pathlib.Path("data", "datasets", level.stem + ".h5")
dataset_path_rand = init_dir / pathlib.Path("data", "datasets", level.stem + ".random.h5")

print(f"level location={level}")



#run_ddqn
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

dataset = getDataset()
# train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
print(len(dataset.episodes))

ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
          target_update_interval=target_update_interval,
          batch_size=batch_size).create()

# set environment in scorer function
env_train = Env(visible=False, level=str(level), port=8080).env
ddqn.build_with_dataset(dataset)
env_evaluator  = EnvironmentEvaluator(env_train)

# evaluate algorithm on the environment

name = 'DDQN_marioai_%s_%s_%s_%s_%s' % (level.stem, gamma, learning_rate, target_update_interval, n_epochs)
model_file = init_dir / pathlib.Path("data", "models", name + ".pt")
currentMax = -100000
ddqn_max = copy.deepcopy(ddqn)

fitter = ddqn.fitter(
   dataset,
   n_steps = n_steps_per_epoch * n_epochs,
   n_steps_per_epoch=n_steps_per_epoch,
  evaluators={'environment': env_evaluator }
)

for epoch, metrics in fitter:
    if metrics.get("environment") > currentMax:
        currentMax = metrics.get("environment")
        ddqn_max.copy_q_function_from(ddqn)
    else:
        ddqn.copy_q_function_from(ddqn_max)
    ddqn.save_model(model_file)
    if currentMax > 100:
        # For the purpose of the exercise the training will stop if the agent manages to complete the level
        print("A suitable model has been found.")
        break