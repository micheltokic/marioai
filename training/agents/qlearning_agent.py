import numpy as np
from random import random


class QTable:
    """
    data structure to store the Q function for hashable state representations 
    """
    def __init__(self, n_actions, initial_capacity=100):
        self.capacity = initial_capacity
        self.num_states = 0
        self.state_index_map = {}
        self.table:np.array = np.zeros([initial_capacity, n_actions])

    def __contains__(self, state):
        """ 'in' operator """
        return state in self.state_index_map

    def __len__(self):
        return self.num_states

    def __getitem__(self, state):
        """ access state directly using [] notation """
        return self.table[self.state_index_map[state]]

    def init_state(self, state):
        if self.num_states == self.capacity: 
            # need to increase capacity
            self.table = np.concatenate((self.table, np.zeros_like(self.table)))
            self.capacity *= 2

        self.state_index_map[state] = self.num_states
        self.num_states += 1


class Agent:

    def __init__(self, env, alpha=0.1, gamma=0.99, 
            epsilon_start=0.5, epsilon_end=0.001,
            epsilon_decay_length=10000, # in episodes
            initial_capacity=10):
        self.alpha = alpha
        self.gamma = gamma

        # self.epsilon_start = epsilon_start
        # self.epsilon_decay_length = epsilon_decay_length
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.decay_step = (epsilon_start - epsilon_end) / epsilon_decay_length

        self.env = env
        self.Q = QTable(env.action_space.n, initial_capacity)

    def select_action(self, state):
        if not state in self.Q:
            self.Q.init_state(state)
            return self.env.action_space.sample()

        if random() < self.epsilon:
            return self.env.action_space.sample()

        return np.argmax(self.Q[state])

    def update_Q(self, state, action, reward, next_state):
        """ basic Q learning update 
            Q(s,a) <- Q(s,a) + alpha * [r + gamma * max(Q(s', .)) - Q(s,a)]
        """
        if not next_state in self.Q:
            self.Q.init_state(next_state)

        td_error = reward + self.gamma * np.max(self.Q[next_state]) \
                    - self.Q[state][action]
        self.Q[state][action] += self.alpha * td_error 

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_end:
            # self.epsilon -= self.decay_step
            self.epsilon = max(self.epsilon_end, self.epsilon-self.decay_step)

