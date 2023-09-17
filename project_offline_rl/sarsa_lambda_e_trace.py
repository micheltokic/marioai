# modified from https://naifmehanna.com/2018-10-18-implementing-sarsa-in-python/
import itertools
import pathlib
import sys
import time
from collections import defaultdict

import numpy as np

from get_paths import LevelPaths
from gym_setup import Env
from d3rlpy.dataset import MDPDataset, ReplayBuffer
import d3rlpy.dataset



def make_epsilon_greedy_policy(Q, epsilon, num_actions):
    def policy_fn(observation: np.ndarray):
        A = np.ones(num_actions, dtype=float) * epsilon / num_actions
        # NOTE: better version than tuple?
        observation = tuple(observation)
        best_action = np.argmax(Q[observation])
        A[best_action] += (1.0 - epsilon)
        return A

    return policy_fn


# Q should be a Q[state] = action
# state is an array
# Q[array]

def sarsa_lambda(env, num_episodes, num_actions, level_paths: LevelPaths, discount=0.9, alpha=0.01, trace_decay=0.9, epsilon=0.1, type='accumulate'):
    Q = defaultdict(lambda: np.zeros(num_actions))
    E = defaultdict(lambda: np.zeros(num_actions))

    policy = make_epsilon_greedy_policy(Q, epsilon, num_actions)

    # No reward at first time step, because no action was taken yet
    rewards = [0.]

    for i_episode in range(num_episodes):


        print("\rEpisode {}/{}. ({})".format(i_episode + 1, num_episodes, rewards[-1]), end="")
        sys.stdout.flush()

        state, _ = env.reset()
        action_probs = policy(state)
        action = np.random.choice(np.arange(len(action_probs)), p=action_probs)

        done = False
        observations = [tuple(state)]
        actions = [action]
        terminals = [done]

        for t in itertools.count():

            next_state, reward, done, truncated, info = env.step(action)

            next_action_probs = policy(next_state)
            next_action = np.random.choice(np.arange(len(next_action_probs)), p=next_action_probs)

            # NOTE: better version than tuple?
            next_state = tuple(next_state)
            state = tuple(state)

            # save data
            actions.append(action)
            rewards.append(reward)
            terminals.append(done)
            observations.append(next_state)

            delta = reward + discount * Q[next_state][next_action] - Q[state][action]

            E[state][action] += 1

            for s, _ in Q.items():
                Q[s][:] += alpha * delta * E[s][:]
                if type == 'accumulate':
                    E[s][:] *= trace_decay * discount
                elif type == 'replace':
                    if s == state:
                        E[s][:] = 1
                    else:
                        E[s][:] *= discount * trace_decay

            if done:
                break

            state = next_state
            action = next_action
        dataset = None
        if level_paths.dataset_path_sarsa.exists():
            # NOTE: is this the correct type of buffer?
            # see https://d3rlpy.readthedocs.io/en/latest/references/dataset.html
            with level_paths.dataset_path_sarsa.open("rb") as dataset_file:
                dataset: ReplayBuffer = ReplayBuffer.load(dataset_file, d3rlpy.dataset.InfiniteBuffer())
                dataset.append_episode(
                    d3rlpy.dataset.components.Episode(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                                                      np.asarray(rewards)[:, np.newaxis], done))
        else:
            dataset = MDPDataset(np.asarray(observations), np.asarray(actions)[:, np.newaxis],
                                 np.asarray(rewards)[:, np.newaxis], np.asarray(terminals))
        # FIXME: change this back
        with open(level_paths.dataset_path_sarsa, "w+b") as f:
            dataset.dump(f)

    return Q


if __name__ == '__main__':
    visible = False

    # Setup global variables
    # init_dir = pathlib.Path(__file__).parent
    init_dir = pathlib.Path("./project_offline_rl")
    level_paths: LevelPaths = LevelPaths(init_dir, "ClimbLevel.lvl")

    print(f"level location={level_paths.level}")

    environment = Env(visible=visible, level=str(level_paths.level), port=8080)
    env_train = environment.env
    num_actions = len(environment.env.enabled_actions)

    start = time.time()
    Q = sarsa_lambda(env_train, 20, num_actions=num_actions, level_paths=level_paths)
    end = time.time()
    print("Algorithm took {} to execute".format(end - start))
