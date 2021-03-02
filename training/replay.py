import sys

import gym
import gym_marioai
from gym_marioai import levels

from agents import qlearning_agent
from logger import Logger

from main import rf_height, rf_width, trace, prog, cliff, level, win, dead, path

version = 1

if __name__ == '__main__':

    level_name = f'{level}_{rf_width}x{rf_height}_trace{trace}_prog{prog}_cliff{cliff}_win{win}_dead{dead}-{version}'
    result_name = level_name

    if len(sys.argv) == 2:
        result_name = sys.argv[1]
    elif len(sys.argv) == 3:
        result_name = sys.argv[1]
        level_name = sys.argv[2]

    logger = Logger(result_name, load_existing=True)

    R = gym_marioai.RewardSettings(progress=prog, timestep=-1,
                                   cliff=cliff,
                                   win=win,
                                   dead=dead)

    # possible levels are: flatLevel.lvl, easyLevel.lvl, hardLevel.lvl or None for seed-based selection
    env = gym.make('Marioai-v0', render=True,
                   level_path=path,
                   reward_settings=R,
                   compact_observation=True,
                   trace_length=trace,
                   rf_width=rf_width, rf_height=rf_height)

    agent = qlearning_agent.Agent(env, epsilon_start=0)
    agent.Q = logger.load_model()

    # run the demonstration
    while True:
        done = False
        state = env.reset()
        steps = 0
        total_reward = 0

        while not done:
            action = agent.select_action(state)
            state, reward, done, info = env.step(action)
            print(state)
            total_reward += reward
            steps += 1

        print(f'reward: {total_reward}, steps: {steps}, success: {info["win"]}')







