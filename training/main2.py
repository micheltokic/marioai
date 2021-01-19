import numpy as np
import gym
import gym_maze

from agents import qlearning_agent
from logger import Logger


SAVE_FREQUENCY = 10 
TOTAL_EPISODES = 300


def train(env, agent: qlearning_agent.Agent, 
          logger: Logger, n_episodes:int):
    """
    train the Q learning agent
    """
    actions = ['N', 'E', 'S', 'W']

    for e in range(n_episodes):
        done = False
        info = {}
        total_reward = 0

        # convert to bytes so it can be used as dictionary key
        # (np array is not hashable)
        state = env.reset()
        state = state.tobytes()

        steps = 0

        while not done:
            env.render()
            action = agent.select_action(state)

            next_state, reward, done, info = env.step(actions[action])

            next_state = next_state.tobytes()
            total_reward += reward

            agent.update_Q(state, action, reward, next_state)
            state = next_state
            steps += 1

        # episode has finished
        logger.append(total_reward, steps, True)

        if e % SAVE_FREQUENCY == 0:
            logger.save()


        # .update_stats(e, n_episodes, total_reward, info)
        print(f'episode {e} terminated after {steps} steps. ' \
              f'Total reward: {total_reward:.2f}, ' \
              f'states visited: {agent.q.n_known_states}, ' \
              f'win: {True}')



if __name__ == '__main__':

    logfile_name = 'maze_test.json'
    logger = Logger(logfile_name)

    #possible levels are: flatLevel.lvl, easyLevel.lvl, hardLevel.lvl or None for seed-based selection
    # env = gym.make('Marioai-v0', visible=False, 
    #         file_name=level_name, rf_width=3, rf_height=4, 
    #         max_steps=0)
    env = gym.make('maze-sample-10x10-v0')
    agent = qlearning_agent.Agent(env, alpha=0.7)

    train(env, agent, logger, TOTAL_EPISODES)

    print('training finished.')
