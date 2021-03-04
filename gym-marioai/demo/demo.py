import random

import gym
import gym_marioai
from gym_marioai import levels

if __name__ == '__main__':

    # adjust the reward settings like so:
    reward_settings = gym_marioai.RewardSettings(dead=-10000, timestep=0)

    env = gym.make('Marioai-v0', render=True,
                   reward_settings=reward_settings,
                   level_path=levels.cliff_level,
                   compact_observation=True,
                   trace_length=1,
                   rf_width=7, rf_height=5)

    for e in range(100):
        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.JUMP_RIGHT if random.randint(0,1) % 2 == 0 else env.SPEED_RIGHT
            s, r, done, info = env.step(a)

            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



