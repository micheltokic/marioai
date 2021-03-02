import gym
import gym_marioai

from agents import qlearning_agent
from logger import Logger


SAVE_FREQUENCY = 100 
TOTAL_EPISODES = 5000

rf_width = 10
rf_height = 5
trace = 3
prog = 2
cliff = 10000
win = -1000
dead = 0

level = 'earlyCliffLevel'
path = None

if level == 'cliffLevel':
    path = gym_marioai.levels.cliff_level
if level == 'oneCliffLevel':
    path = gym_marioai.levels.one_cliff_level
if level == 'earlyCliffLevel':
    path = gym_marioai.levels.early_cliff_level

def train(env, agent: qlearning_agent.Agent, 
          logger: Logger, n_episodes:int):
    """
    train the Q learning agent with default observation, 
    which is a numpy bool array
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

        print(f'episode {e:4} terminated. epsilon: {agent.epsilon:3f}, Steps: {info["steps"]:4}\t'
              f'R: {total_reward:7.2f}\t'
              f'|O|: {len(agent.Q):4}\t'
              f'win: {info["win"]}')
        

def train_compact_observation(env, agent: qlearning_agent.Agent, 
                              logger: Logger, n_episodes: int):
    """
    train the Q learning agent, using the compact observation (byte list)
    """

    for e in range(n_episodes):
        done = False
        info = {}
        total_reward = 0
        state = env.reset()

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            total_reward += reward
            agent.update_Q(state, action, reward, next_state)
            state = next_state

        # episode has finished
        logger.append(total_reward, info['steps'], info['win'])
        agent.decay_epsilon()

        if e % SAVE_FREQUENCY == 0:
            logger.save()
            logger.save_model(agent.Q)

        if (e+1) % 100 == 0:
            print(f'episode {e:4} terminated. epsilon: {agent.epsilon:3f}, Steps: {info["steps"]:4}\t'
                  f'R: {total_reward:7.2f}\t'
                  f'|O|: {len(agent.Q):4}\t'
                  f'win: {info["win"]}')


if __name__ == '__main__':
    level_name = f'{level}_{rf_width}x{rf_height}_trace{trace}_prog{prog}_cliff{cliff}_win{win}_dead{dead}-0'
    logger = Logger(level_name)

    R = gym_marioai.RewardSettings(progress=prog, timestep=-1,
                                   cliff=cliff,
                                   win=win,
                                   dead=dead)

    

    env = gym.make('Marioai-v0', render=False,
                   level_path=path,
                   reward_settings=R,
                   compact_observation=True,
                   trace_length=trace,
                   rf_width=rf_width, rf_height=rf_height)

    agent = qlearning_agent.Agent(env, alpha=0.2, epsilon_start=0.5,
                                  epsilon_end=0.1, epsilon_decay_length=TOTAL_EPISODES / 2)
    train_compact_observation(env, agent, logger, TOTAL_EPISODES)
    print('training finished.')