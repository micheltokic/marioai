import random

import gym
import gym_marioai


if __name__ == '__main__':
    env = gym.make('Marioai-v0', render=True, compact_observation=True, trace_length=1, rf_width=7, rf_height=5,
                   level_path="None")

    for e in range(100):
        s = env.reset(seed=random.randint(0, 1000))
        done = False
        total_reward = 0

        while not done:
            env.render()
            a = env.JUMP_RIGHT if random.randint(0,1) % 2 == 0 else env.SPEED_RIGHT
            s, r, done, info = env.step(a)

            total_reward += r

        print(f'finished episode {e}, total_reward: {total_reward}')

    print('finished demo')



