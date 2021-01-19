import gym
import gym_marioai


if __name__ == '__main__':

    # adjust the reward settings like so:
    reward_settings = gym_marioai.RewardSettings(timestep=-0.1,)

    env = gym.make('Marioai-v0', visible=True,
                   reward_settings=reward_settings, 
                   file_name='easyLevel.lvl')

    for e in range(100):
        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            print('state:\n', s, 'reward:', r)

            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



