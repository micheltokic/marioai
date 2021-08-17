
# here the player can play to generate data
from d3rlpy.algos.dqn import DQN
from data.datasets.getDatasets import getDataset
from gym_setup import Env
import d3rlpy
from gym_marioai import levels

env = Env(visible=True, level=levels.cliff_level)
env = env.get_env()

dqn = DQN()
#dqn = d3rlpy.algos.DoubleDQN()
dqn.build_with_dataset(getDataset())
dqn.load_model('exercise_2_1/data/model.pt')

while True:
    observation = env.reset()
    done = False
    total_reward = 0
    while not done:
        observation, reward, done, info = env.step(dqn.predict([observation])[0])
        total_reward += reward

    print(f'finished episode, total_reward: {total_reward}')










