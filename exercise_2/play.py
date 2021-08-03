
from qlearner import QLearner
from gamepad_controller import GamepadController
from keyboard_controller import KeyboardController
import gym
from gym_marioai import levels


# Open Game
from subprocess import Popen
server_process = Popen(
    ['java', '-jar', 'gym-marioai\gym_marioai\server\marioai-server-0.1-jar-with-dependencies.jar'])


USE_GAMEPAD = False

all_actions = (0,1,2,3,4,5,6,7,8,9,10,11,12)

env = gym.make('Marioai-v0', render=True,
               level_path=levels.one_cliff_level,
               compact_observation=True,
               enabled_actions=all_actions,
               rf_width=20, rf_height=10)

while True:
    state = env.reset()
    done = False
    total_reward = 0
    action = env.NOTHING
    q = QLearner(env)
    if USE_GAMEPAD:
        controller = GamepadController(env)
    else:
        controller = KeyboardController(env)

    while not done:
        next_state, reward, done, info = env.step(action)
        total_reward += reward
        next_action = controller.read()
        q.train(state, action, reward, next_state, next_action)
        state, action = next_state, next_action


    print(f'finished episode, total_reward: {total_reward}')





