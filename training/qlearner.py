import numpy as np
import pickle


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
