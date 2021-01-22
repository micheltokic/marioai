import gym
import gym_marioai
import os

from agents import qlearning_agent
from logger import Logger


SAVE_FREQUENCY = 100 
TOTAL_EPISODES = 20000


def train(env, agent: qlearning_agent.Agent, 
          logger: Logger, n_episodes:int):
    """
    train the Q learning agent
    """

    for e in range(n_episodes):
        done = False
        info = {}
        total_reward = 0

        # convert to bytes so it can be used as dictionary key
        # (np array is not hashable)
        state = env.reset()
        state = state.tobytes()

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            next_state = next_state.tobytes()
            total_reward += reward
            agent.update_Q(state, action, reward, next_state)
            state = next_state

        # episode has finished
        logger.append(total_reward, info['steps'], info['win'])
        agent.decay_epsilon()

        if e % SAVE_FREQUENCY == 0:
            logger.save()
            logger.save_model(agent.Q)


        print(f'episode {e:4} terminated. epsilon: {agent.epsilon:3f}, Steps: {info["steps"]:4}\t' \
              f'R: {total_reward:7.2f}\t' \
              f'|O|: {len(agent.Q):4}\t' \
              f'win: {info["win"]}')



if __name__ == '__main__':
    level_name = 'easyLevel_7x5'
    logger = Logger(level_name)

    #adjust filepath when moved
    marioai_file_path = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
    file_path = marioai_file_path+ "/gym-marioai/levels/easyLevel.lvl"


    #possible levels are: flatLevel.lvl, easyLevel.lvl, hardLevel.lvl or None for seed-based selection
    env = gym.make('Marioai-v0', render=False,
            file_name=file_path,
            rf_width=7, rf_height=5,
            )
    agent = qlearning_agent.Agent(env, alpha=0.2, 
            epsilon_decay_length=TOTAL_EPISODES / 2)
    train(env, agent, logger, TOTAL_EPISODES)
    print('training finished.')
