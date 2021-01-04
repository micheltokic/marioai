import gym
import gym_marioai


if __name__ == '__main__':

    env = gym.make('Marioai-v0')

    for e in range(100):

        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            print(s)
            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')


