import os

import gym
import gym_marioai
from gym_marioai import levels


if __name__ == '__main__':
    print('available levels:')
    print(levels.easy_level)
    print(levels.flat_level)
    print(levels.hard_level)

    # adjust the reward settings like so:
    reward_settings = gym_marioai.RewardSettings(timestep=-0.1,)

    env = gym.make('Marioai-v0', render=True,
                   reward_settings=reward_settings,
                   level_path=levels.easy_level)

    for e in range(100):
        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



