#!/usr/bin/env python
# coding: utf-8
import pathlib

import d3rlpy.dataset
import numpy as np

from get_paths import LevelPaths
from gym_setup import Env
import training_params
import d3rlpy.dataset
from d3rlpy.dataset import ReplayBuffer
from d3rlpy.dataset.buffers import InfiniteBuffer

from sklearn.model_selection import train_test_split

from data.datasets.getDatasets import getDataset, getSpecificDataset

def test_ddqn(level_name_learned: str, level_name_test: str | None, learning_rate, gamma, target_update_interval, batch_size, visible=False):

    n_epochs = training_params.n_epochs
    n_steps_per_epoch = training_params.n_steps_per_epoch
    test_size = training_params.test_size
    use_gpu = training_params.use_gpu

    init_dir = pathlib.Path("./project_offline_rl")
    level_paths: LevelPaths = LevelPaths(init_dir, level_name_learned)
    if level_name_test is not None:
        level_paths_other: LevelPaths = LevelPaths(init_dir, level_name_test)
        env_show = Env(visible=visible, level=str(level_paths_other.level), port=8080).env
    else:
        env_show = Env(visible=visible, level=str(level_paths.level), port=8080).env

    # print(f"level location={level}")

    dataset = getSpecificDataset(level_paths.level_name)
    train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
    train_dataset = ReplayBuffer(InfiniteBuffer(), episodes=train_episodes)

    ddqn = d3rlpy.algos.DoubleDQNConfig(learning_rate=learning_rate, gamma=gamma,
                                        target_update_interval=target_update_interval,
                                        batch_size=batch_size).create()

    name = 'DDQN_marioai_%s_%s_%s_%s_%s_%s' % (level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs, batch_size)

    # Needs to be rebuilt
    ddqn.build_with_dataset(train_dataset)

    ddqn.load_model(init_dir / pathlib.Path("data") / "models" / f"{name}.pt")

    try:
        observation, _ = env_show.reset()

        done = False
        total_reward = 0
        while not done:
            predict_action = ddqn.predict(observation[np.newaxis, :])[0]
            observation, reward, done, truncated, info = env_show.step(predict_action)
            total_reward += reward
        print(f'finished episode, total_reward: {total_reward}')
        # this is needed to close the socket to the java program or else it does not work when called multiple times.
        env_show.teardown()
    except ConnectionResetError:
        print("Window closed.")

if __name__ == '__main__':
    test_ddqn("CliffsAndEnemiesLevel.lvl", "ClimbLevel.lvl", training_params.learning_rate, training_params.gamma, training_params.target_update_interval, training_params.batch_size)
