import gym
import gym_marioai


if __name__ == '__main__':

    env = gym.make('Marioai-v0', visible=True)

    for e in range(3):

        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



