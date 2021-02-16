from gym_marioai.mario_pb2 import JUMP_RIGHT, SPEED_JUMP_RIGHT, SPEED_RIGHT
import random

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
                   level_path=levels.easy_level,
                   compact_observation=True,
                   rf_width=20, rf_height=10)

    for e in range(100):
        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            # a = env.action_space.sample()
            a = JUMP_RIGHT if random.randint(0,1) % 2 == 0 else SPEED_RIGHT
            s, r, done, info = env.step(a)

            print(len(s), ':', s)

            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



