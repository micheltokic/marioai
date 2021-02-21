import keyboard

import gym
import gym_marioai
from gym_marioai import levels
from gym_marioai.mario_pb2 import JUMP_RIGHT, SPEED_JUMP_RIGHT, SPEED_RIGHT,\
        JUMP_LEFT, SPEED_JUMP_LEFT, SPEED_LEFT, DOWN, JUMP


def get_action():
    if keyboard.is_pressed('space+right'):
        return SPEED_JUMP_RIGHT
    elif keyboard.is_pressed('space+left'):
        return SPEED_JUMP_LEFT
    elif keyboard.is_pressed('right'):
        return SPEED_RIGHT
    elif keyboard.is_pressed('left'):
        return SPEED_LEFT
    elif keyboard.is_pressed('down'):
        return DOWN
    elif keyboard.is_pressed('space'):
        return JUMP
    else:
        return SPEED_RIGHT 


env = gym.make('Marioai-v0', render=True,
               level_path=levels.one_cliff_level,
               compact_observation=True,
               rf_width=20, rf_height=10)


while True:
    s = env.reset()
    done = False
    total_reward = 0

    while not done:
        a = get_action()
        s, r, done, info = env.step(a)
        # print(len(s), ':', s)

        total_reward += r

    print(f'finished episode, total_reward: {total_reward}')

print('finished demo')



