"""
this is just a script to run the trace experiment
"""
import argparse
import os
import sys
import json
from subprocess import Popen
import time

import gym
import gym_marioai
import numpy as np

from main import QTable


#####################################
#   Training Parameters
#####################################
n_episodes = 10000
n_experiments = 15
SAVE_FREQ = 100

alpha = 0.1
gamma = 0.99
lmbda = 0.75
epsilon_start = 0.5
epsilon_end = 0.01
epsilon_decay_length = n_episodes / 2
decay_step = (epsilon_start - epsilon_end) / epsilon_decay_length


#####################################
#   Environment/Reward Settings
#####################################
level = 'oneCliffLevel'
path = gym_marioai.levels.one_cliff_level

# trace = 2
rf_width = 20
rf_height = 10
prog = 1
timestep = -1
cliff = 1000
win = -10
dead = -10

reward_settings = gym_marioai.RewardSettings(
        progress=prog, 
        timestep=timestep, 
        cliff=cliff, 
        win=win, dead=dead)


def run_experiment(trace, port, i):
    """
    run the experiment
    """

    # create the environment
    env = gym.make('Marioai-v0', port=port,
                   render=False,
                   level_path=path,
                   reward_settings=reward_settings,
                   compact_observation=True,
                   trace_length=trace,
                   rf_width=rf_width, rf_height=rf_height)

    # for i in range(n_experiments):
    log_path = f'./experiment_results/trace{trace}_run{i}.json'
    run_training(env, log_path)


def run_training(env, log_path):
    """
    run a single training loop
    """

    #####################################
    #  collect the data to store
    #####################################
    data = dict(
            all_steps = list(np.zeros([n_episodes])),
            all_rewards = list(np.zeros([n_episodes])),
            all_jumps = list(np.zeros([n_episodes])))

    ####################################
    #       Q-learner setup
    #####################################
    Q = QTable(env.n_actions, 128)
    etrace = {}

    ####################################
    #      Training Loop
    ####################################
    for e in range(n_episodes):
        done = False
        info = {}
        total_reward = 0
        steps = 0
        epsilon = max(epsilon_end, epsilon_start - decay_step * e)
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
            best_next_action = int(np.argmax(Q[next_state]))  # greedy
            if np.random.rand() < epsilon:
                next_action = env.action_space.sample()
            else:
                next_action = best_next_action

            # calculate the TD error
            td_error = reward + gamma * Q[next_state][best_next_action] - Q[state][action]

            # reset eligibility trace for (s,a) using replacing strategy
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

        # episode finished
        data['all_steps'][e] = steps
        data['all_rewards'][e] = total_reward
        data['all_jumps'][e] = info['cliff_jumps']

        if e % SAVE_FREQ == 99:
            print(f'episode {e} finished')
            # do not save the model, this is just for plotting
            with open(log_path, 'w') as f:
                json.dump(data, f)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--trace", type=int, required=True)
    # parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-i", "--index", type=int, required=True)
    args = parser.parse_args()

    print('running', args.trace, args.index)

    port = 8080 + args.index

    server_process = Popen(
        ['java', '-jar', 
            '../marioai-proto-interface/target/marioai-proto-interface-0.1-SNAPSHOT-jar-with-dependencies.jar', 
            '-p', str(port)])

    print('server started.')

    try:
        time.sleep(5)
        run_experiment(args.trace, port, args.index)

    except Exception as e:
        print(e)
        server_process.kill()
        print('finished.')

    server_process.kill()




