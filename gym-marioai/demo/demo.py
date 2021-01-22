import gym
import gym_marioai
import os

if __name__ == '__main__':

    # adjust the reward settings like so:
    reward_settings = gym_marioai.RewardSettings(timestep=-0.1,)

    level_name = "easyLevel.lvl"
    #adjust filepath when moved
    marioai_file_path = os.path.dirname(os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
    file_path = marioai_file_path+ "/gym-marioai/levels/"+level_name

    env = gym.make('Marioai-v0', render=True,
                   reward_settings=reward_settings, 
                   file_name=file_path)

    for e in range(100):
        s = env.reset()
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.action_space.sample()
            s, r, done, info = env.step(a)
            # print('state:\n', s, 'reward:', r)
            # print(r)

            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



