from d3rlpy.dataset import MDPDataset
import numpy as np
from exercise_2_1.gym_setup import Env
from logger import Logger
from qlearner import QLearner


#####################################
#   Training Parameters
#####################################
n_episodes = 15000
alpha = 0.1
gamma = 0.99
lmbda = 0.75
epsilon_start = 0.5
epsilon_end = 0.01
epsilon_decay_length = n_episodes / 2
decay_step = (epsilon_start - epsilon_end) / epsilon_decay_length

SAVE_FREQ = 50

training = True

log_path = f'model'


def replay():
    """
    replay. loads model, does not store model or logs
    """
    logger = Logger(log_path, True)


    env = Env(visible=False)
    env = env.get_env()

    agent = QLearner(env, alpha, gamma, lmbda)
    agent.Q = logger.load_model()


    observations = np.array([])
    actions = np.array([])
    rewards = np.array([])
    terminals = np.array([])


    ####################################
    #      Main Loop
    ####################################
    while True:
        done = False
        info = {}
        total_reward = 0
        steps = 0
        state = env.reset()

        while not done:
            action = agent.choose_action(state)
            state, reward, done, info = env.step(action)
            total_reward += reward
            steps += 1

            observations = np.append(observations, state)
            actions = np.append(actions, action)
            rewards = np.append(rewards, reward)
            terminals = np.append(terminals, done)

            if steps % 50 == 0 and steps != 0:
                dataset = MDPDataset(np.reshape(observations, (-1, 1)), np.reshape(actions, (-1, 1)), np.reshape(
                rewards, (-1, 1)), np.reshape(terminals, (-1, 1)), discrete_action=True, episode_terminals=None)
                dataset.dump('exercise_2_1/data/q_data.h5')


def train():
    """
    training
    """
    logger = Logger(log_path)
    # collect some training statistics
    all_rewards = np.zeros([SAVE_FREQ])
    all_wins = np.zeros([SAVE_FREQ])
    all_steps = np.zeros([SAVE_FREQ])
    all_gap_jumps = np.zeros([SAVE_FREQ])

    ###################################
    #       environment setup
    ###################################
    env = Env(visible=False)
    env = env.get_env()

    ####################################
    #       Q-learner setup
    #####################################
    agent = QLearner(env, alpha, gamma, lmbda)

    ####################################
    #      Training Loop
    ####################################
    for e in range(n_episodes+1):
        done = False
        info = {}
        total_reward = 0
        steps = 0

        epsilon = max(epsilon_end, epsilon_start - decay_step * e)
        state = env.reset()
        action = agent.choose_action(state, epsilon)

        while not done:
            next_state, reward, done, info = env.step(action)
            next_action = agent.choose_action(next_state, epsilon)
            agent.learn(state, action, reward, next_state, next_action)

            total_reward += reward
            steps += 1
            action = next_action
            state = next_state

        # episode finished
        logger.append(total_reward, info['steps'], info['win'])

        all_rewards[e % SAVE_FREQ] = total_reward
        all_wins[e % SAVE_FREQ] = 1 if info['win'] else 0
        all_steps[e % SAVE_FREQ] = info['steps']

        if e % SAVE_FREQ == 0 and e > 0:
            logger.save()
            logger.save_model(agent.Q)
            print(f'finished episode {e}. epsilon: {epsilon:.3f}\t avg reward: {all_rewards.mean():>4.2f}\t'
                  f'avg steps: {all_steps.mean():>4.2f}\t'
                  f'win rate: {all_wins.mean():3.2f}\t  \t'
                  f'states: {agent.Q.num_states}')


if __name__ == '__main__':
    if training:
        train()
    else:
        replay()
