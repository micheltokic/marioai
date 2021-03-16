import cProfile
import pstats
import time
import os

import gym
import gym_marioai

if __name__ == '__main__':

    # profile = cProfile.Profile()
    # profile.enable()

    # adjust the reward settings like so:
    reward_settings = gym_marioai.RewardSettings(timestep=-0.1,)

    env = gym.make('Marioai-v0', render=False,
                   reward_settings=reward_settings, 
                   level_path=gym_marioai.levels.easy_level)

    max_steps = 100000
    steps = 0

    start_time = time.time()

    while steps < max_steps:
        s = env.reset()
        done = False

        while not done and steps < max_steps:
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            steps += 1

        print(f'finished episode, {steps}/{max_steps} steps')

    print(f'took {steps} steps in {time.time() - start_time} sec')
    # profile.disable()
    # ps = pstats.Stats(profile)
    # ps.sort_stats('cumtime', 'calls')
    # ps.print_stats(100)

    print('finished demo')



