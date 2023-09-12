import pathlib

import d3rlpy.dataset
import numpy as np
from d3rlpy.dataset import MDPDataset, ReplayBuffer

from get_paths import LevelPaths
from gym_setup import Env

init_dir = pathlib.Path(__file__).parent
# level_str = "CliffsAndEnemiesLevel.lvl"
level_str = "ClimbLevel.lvl"

level_paths: LevelPaths = LevelPaths(init_dir, level_str)

print(f"level location={level_paths.level}")

# Generate random data
EPISODES = 50  # <--- increase if you want more random data. More data might slow down the training process.

env_rand = Env(visible=False, level=str(level_paths.level), port=8080).env

for episode in range(EPISODES):
    print(f"{episode=} \r", end="")
    observation, _ = env_rand.reset()
    done = False
    action = env_rand.action_space.sample()

    observations = [observation]
    actions = [action]
    # No reward at first time step, because no action was taken yet
    rewards = [0]
    terminals = [done]

    while not done:
        observation, reward, done, truncated, info = env_rand.step(action)
        action = env_rand.action_space.sample()

        observations.append(observation)
        actions.append(action)
        rewards.append(reward)
        terminals.append(done)

    dataset = None
    if level_paths.dataset_path_rand.exists():
        # NOTE: is this the correct type of buffer?
        # see https://d3rlpy.readthedocs.io/en/latest/references/dataset.html
        with level_paths.dataset_path_rand.open("rb") as dataset_file:
            dataset: ReplayBuffer = ReplayBuffer.load(dataset_file, d3rlpy.dataset.InfiniteBuffer())
            dataset.append_episode(
                d3rlpy.dataset.components.Episode(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                                                  np.asarray(rewards)[:, np.newaxis], done))
    else:
        dataset = MDPDataset(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                             np.asarray(rewards)[:, np.newaxis], np.asarray(terminals))
    # FIXME: change this back
    with open(level_paths.dataset_path_rand, "w+b") as f:
        dataset.dump(f)

print("\nDone!")
