import keyboard

import gym
import gym_marioai
from gym_marioai import levels



all_actions = (0,1,2,3,4,5,6,7,8,9,10,11,12)

env = gym.make('Marioai-v0', render=True,
               level_path=levels.one_cliff_level,
               compact_observation=True,
               enabled_actions=all_actions,
               rf_width=20, rf_height=10)


def get_action():
    if keyboard.is_pressed('shift+space+right'):
        return env.SPEED_JUMP_RIGHT
    if keyboard.is_pressed('shift+space+left'):
        return env.SPEED_JUMP_LEFT

    elif keyboard.is_pressed('space+right'):
        return env.JUMP_RIGHT
    elif keyboard.is_pressed('space+left'):
        return env.JUMP_LEFT

    if keyboard.is_pressed('shift+right'):
        return env.SPEED_RIGHT
    if keyboard.is_pressed('shift+left'):
        return env.SPEED_LEFT

    elif keyboard.is_pressed('right'):
        return env.RIGHT
    elif keyboard.is_pressed('left'):
        return env.LEFT
    elif keyboard.is_pressed('down'):
        return env.DOWN
    elif keyboard.is_pressed('space'):
        return env.JUMP
    else:
        return env.NOTHING


while True:
    s = env.reset()
    done = False
    total_reward = 0

    while not done:
        a = get_action()
        print('action', a)
        s, r, done, info = env.step(a)
        # print(len(s), ':', s)

        total_reward += r

    print(f'finished episode, total_reward: {total_reward}')

print('finished demo')



