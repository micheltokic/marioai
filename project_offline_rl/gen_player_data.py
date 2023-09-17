import pathlib

import d3rlpy.dataset
import numpy as np
from d3rlpy.dataset import MDPDataset, ReplayBuffer

from controller import GamepadController, KeyboardController
from get_paths import LevelPaths
from gym_setup import Env

# Setup global variables
init_dir = pathlib.Path(__file__).parent
# level_str = "CliffsAndEnemiesLevel.lvl"
level_str = "RoughTerrainLevel.lvl"
# level_str = "ClimbLevel.lvl"

level_paths: LevelPaths = LevelPaths(init_dir, level_str)

print(f"level location={level_paths.level}")

# ### 1.1 Player generated data.
#
# ![Mario](https://media1.giphy.com/media/aX0RqLt2ARSW4/giphy.gif?cid=ecf05e47fnkts3fqh25tj9v8noh9vnccwo4x0ey4zpdxc7ft&rid=giphy.gif&ct=g)
#
#
# To achieve the best possible results, the training algorithm needs the best possible data. In this case that means player generated data.
#
#
# You will have the most fun playing with a USB-Controller but if you have none, you can set the following variable to ``False`` to use the keyboard:

# In[17]:


# Don't forget to run me
USE_GAMEPAD = False

# ### Controls
# |            	| Keyboard    	| Xbox       	| Playstation 	|
# |------------	|-------------	|------------	|-------------	|
# | Jump       	| S           	| A          	| X           	|
# | Sprint     	| A           	| B          	| O           	|
# | Move Right 	| Arrow Right 	| Dpad Right 	| Dpad Right  	|
# | Move Left  	| Arrow Left  	| Dpad Left  	| Dpad Left   	|
# | Duck       	| Arrow Down  	| Dpad Down  	| Dpad Down   	|

# To start the game run the next cell. If you think you have enough data just close the game window and move on to the next cell.
#
# Note: We have pregenerated some training data for your convenience which will be used in addition to your data to train the model.
# If you want to train with your own data only, go ahead and delete the data from ``project_offline_rl\data\datasets``.

# In[18]:


if level_paths.dataset_path.exists():
    with level_paths.dataset_path.open("rb") as dataset_file:
        dataset: ReplayBuffer = ReplayBuffer.load(dataset_file, d3rlpy.dataset.InfiniteBuffer())
        print(f"number of episodes: {dataset.size()}")
# Let's play!
# Let's play!
try:
    env_play = Env(visible=True, level=str(level_paths.level.resolve()), port=8080).env

    if USE_GAMEPAD:
        controller = GamepadController(env_play)
    else:
        controller = KeyboardController(env_play)
    while True:
        observation, _ = env_play.reset()

        done = False
        action = controller.read()

        observations = [observation]

        actions = [action]
        # No reward at first time step, because no action was taken yet
        rewards = [0]
        terminals = [done]

        while not done:
            observation, reward, done, truncated, info = env_play.step(action)

            action = controller.read()

            observations.append(observation)
            actions.append(action)
            rewards.append(reward)
            terminals.append(done)

        dataset = None
        if level_paths.dataset_path.exists():
            # NOTE: is this the correct type of buffer?
            # see https://d3rlpy.readthedocs.io/en/latest/references/dataset.html
            with level_paths.dataset_path.open("rb") as dataset_file:
                dataset: ReplayBuffer = ReplayBuffer.load(dataset_file, d3rlpy.dataset.InfiniteBuffer())
                dataset.append_episode(
                    d3rlpy.dataset.components.Episode(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                                                      np.asarray(rewards)[:, np.newaxis], done))
                print(f"number of episodes: {dataset.size()}")
        else:
            dataset = MDPDataset(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                                 np.asarray(rewards)[:, np.newaxis], np.asarray(terminals))
        with open(level_paths.dataset_path, "w+b") as f:
            dataset.dump(f)

except ConnectionResetError:
    print("Done")
