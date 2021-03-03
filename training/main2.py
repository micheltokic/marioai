import numpy as np
import gym
import gym_marioai
from logger import Logger


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

    def __len__(self):
        return self.num_states

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


#####################################
#   Training Parameters
#####################################
n_episodes = 5000
alpha = 0.2
gamma = 0.99
lmbda = 0.75
epsilon_start = 0.2
epsilon_end = 0.01
epsilon_decay_length = n_episodes / 2

SAVE_FREQ = 100

#####################################
#   Environment/Reward Settings
#####################################
level = 'earlyCliffLevel'
path = None

if level == 'cliffLevel':
    path = gym_marioai.levels.cliff_level
if level == 'oneCliffLevel':
    path = gym_marioai.levels.one_cliff_level
if level == 'earlyCliffLevel':
    path = gym_marioai.levels.early_cliff_level
trace = 3
rf_width = 20
rf_height = 10
prog = 1
timestep = -1
cliff = 100
win = -10
dead = -10


if __name__ == '__main__':

    log_path = f'{level}_{rf_width}x{rf_height}_trace{trace}_prog{prog}_cliff{cliff}_win{win}_dead{dead}-0'
    logger = Logger(log_path)
    Q = QTable(9, 128)
    etrace = {}
    epsilon = epsilon_start

    ###################################
    #       environment setup
    ###################################
    R = gym_marioai.RewardSettings(progress=prog, timestep=timestep,
                                   cliff=cliff, win=win, dead=dead)
    env = gym.make('Marioai-v0', render=False,
                   level_path=path,
                   reward_settings=R,
                   compact_observation=True,
                   trace_length=trace,
                   rf_width=rf_width, rf_height=rf_height)

    ####################################
    #      Training Loop
    ####################################
    all_rewards = np.zeros([SAVE_FREQ])
    for e in range(n_episodes):
        done = False
        info = {}
        total_reward = 0
        steps = 0

        state = env.reset()
        # choose a' from a Policy derived from Q
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            action = int(np.argmax(Q[state]))  # greedy

        while not done:
            next_state, reward, done, info = env.step(action)
            total_reward += reward

            # choose a' from a Policy derived from Q
            best_next_action = int(np.argmax(Q[next_state])) # greedy
            if np.random.rand() < epsilon:
                next_action = env.action_space.sample()
            else:
                next_action = best_next_action

            # calculate the TD error
            td_error = reward + gamma * Q[next_state][best_next_action] - Q[state][action]

            # reset etrace using replacing strategy
            etrace[(state, action)] = 1

            # perform Q update
            if best_next_action == next_action:
                for (s, a), eligibility in etrace.items():
                    Q[s][a] += alpha * eligibility * td_error
                    etrace[(s, a)] *= gamma * lmbda
            else:
                for (s, a), eligibility in etrace.items():
                    Q[s][a] += alpha * eligibility * td_error
                etrace = {}

            steps += 1
            action = next_action
            state = next_state

        all_rewards[e % SAVE_FREQ] = total_reward

        if e % SAVE_FREQ == 0 and e > 0:
            print(f'finished episode. {e}, mean reward: {all_rewards.mean()}')