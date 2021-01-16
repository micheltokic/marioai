import numpy as np
import gym
import gym_marioai


class Agent:

    def __init__(self, env, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env = env
        self.Q = dict()
        self.stats = None

    def select_action(self, state):
        if state not in self.Q:
            self.Q[state] = np.zeros([self.env.action_space.n])
            return self.env.action_space.sample()

        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()

        return np.argmax(self.Q[state])

    def update_Q(self, state, action, reward, next_state):
        if next_state not in self.Q:
            self.Q[next_state] = np.zeros([self.env.action_space.n])

        td_error = reward + self.gamma * max(self.Q[next_state]) \
                    - self.Q[state][action]

        self.Q[state][action] += self.alpha * td_error 

    def update_stats(self, episode, n_episodes, total_reward, info):
        """
            steps, reward, visited states, has won
        """
        if self.stats is None:
            self.stats = np.zeros([n_episodes, 4])

        self.stats[episode] = np.array([info['steps'], total_reward,
                                        len(self.Q.keys()), int(info['win'])])


    def train(self, n_episodes):
        print('starting the training')

        for e in range(n_episodes):
            done = False
            info = {}
            total_reward = 0
            state = self.env.reset()

            # convert to bytes so it can be used as dictionary key
            # (np array is not hashable)
            state = state.tobytes()

            while not done:
                action = self.select_action(state)
                next_state, reward, done, info = self.env.step(action)
                next_state = next_state.tobytes()
                total_reward += reward
                self.update_Q(state, action, reward, next_state)
                state = next_state

            self.update_stats(e, n_episodes, total_reward, info)
            print(f'episode {e} terminated after {info["steps"]} steps. ' \
                  f'Total reward: {total_reward}, ' \
                  f'states visited: {len(self.Q.keys())}, ' \
                  f'win: {info["win"]}')



if __name__ == '__main__':

    env = gym.make('Marioai-v0', visible=False)
    agent = Agent(env)
    agent.train(1000)

    print('training finished.')



