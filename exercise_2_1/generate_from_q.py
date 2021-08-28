from d3rlpy.dataset import MDPDataset
import numpy as np
from gym_setup import Env
import pickle
from gym_marioai import levels

#####################################
#   Training Parameters
#####################################
n_episodes = 15000
alpha = 0.1
gamma = 0.9
lmbda = 0.758
epsilon_start = 0.33
epsilon_end = 0.01
epsilon_decay_length = n_episodes / 2
decay_step = (epsilon_start - epsilon_end) / epsilon_decay_length

SAVE_FREQ = 50

training = True

log_path = f'modellog1'


def train():
    """
    training
    """
    # collect some training statistics
    all_rewards = np.zeros([SAVE_FREQ])
    all_wins = np.zeros([SAVE_FREQ])
    all_steps = np.zeros([SAVE_FREQ])
    all_gap_jumps = np.zeros([SAVE_FREQ])

    
    observations = []
    actions = []
    rewards = []
    terminals = []

    ###################################
    #       environment setup
    ###################################
    env = Env(visible=False, level=levels.cliff_level).env

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
        action = agent.choose_action(hash(str(state)), epsilon)

        while not done:
            next_state, reward, done, info = env.step(action)
            observations.append(next_state)
            actions.append(action)
            rewards.append(reward)
            terminals.append(done)
            next_action = agent.choose_action(hash(str(next_state)), epsilon)
            agent.learn(hash(str(state)), action, reward, hash(str(next_state)), next_action)
            total_reward += reward
            steps += 1
            action = next_action
            state = next_state


        # episode finished

        all_rewards[e % SAVE_FREQ] = total_reward
        all_wins[e % SAVE_FREQ] = 1 if info['win'] else 0
        all_steps[e % SAVE_FREQ] = info['steps']

        if e % SAVE_FREQ == 0 and e > 0:
            print(f'finished episode {e}. epsilon: {epsilon:.3f}\t avg reward: {all_rewards.mean():>4.2f}\t'
                  f'avg steps: {all_steps.mean():>4.2f}\t'
                  f'win rate: {all_wins.mean():3.2f}\t  \t'
                  f'states: {agent.Q.num_states}')

            dataset = MDPDataset(np.asarray(observations), np.asarray(actions), np.asarray(rewards),np.asarray(terminals), discrete_action=True, episode_terminals=None)
            dataset.dump('exercise_2_1/data/datasets/cliff_q_data.h5')


class QTable:
    """
    data structure to store the Q function for hashable state representations
    """
    def __init__(self, n_actions, initial_capacity=100):
        self.capacity = initial_capacity
        self.num_states = 0
        self.state_index_map = {}
        self.table = np.zeros([initial_capacity, n_actions])

    def __contains__(self, state):
        """ 'in' operator """
        return state in self.state_index_map

    def __getitem__(self, state):
        """ access state directly using [] notation """
        if state not in self.state_index_map:
            self.init_state(state)

        return self.table[self.state_index_map[state]]

    def init_state(self, state):
        if self.num_states == self.capacity:
            # need to increase capacity
            self.table = np.concatenate((self.table, np.zeros_like(self.table)))
            self.capacity *= 2

        self.state_index_map[state] = self.num_states
        self.num_states += 1


class QLearner:
    def __init__(self, env, alpha, gamma, lmbda):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.lmbda = lmbda
        self.Q = QTable(env.n_actions, 128)
        self.etrace = {}

    def choose_action(self, state, epsilon=0):
        if np.random.rand() < epsilon:
            return self.env.action_space.sample()
        else:
            return int(np.argmax(self.Q[state]))  # greedy

    def learn(self, state, action, reward, next_state, next_action):
        best_next_action = int(np.argmax(self.Q[next_state]))  # greedy

        # calculate the TD error
        td_error = reward + self.gamma * self.Q[next_state][best_next_action] - self.Q[state][action]

        # reset eligibility trace for (s,a) using replacing strategy
        self.etrace[(state, action)] = 1

        # perform Q update
        if best_next_action == next_action:
            for (s, a), eligibility in self.etrace.items():
                self.Q[s][a] += self.alpha * eligibility * td_error
                self.etrace[(s, a)] *= self.gamma * self.lmbda
        else:
            for (s, a), eligibility in self.etrace.items():
                self.Q[s][a] += self.alpha * eligibility * td_error
            self.etrace = {}

    def save(self, path):
        pickle.dump(self.Q, open(path, 'wb'))

    def load(self, path):
        self.Q = pickle.load(open(path, 'rb'))


if __name__ == '__main__':
        train()







