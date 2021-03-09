import os
import json
import matplotlib.pyplot as plt
import numpy as np


n_experiments = 15
n_episodes = 10000
window_width = 10


def smoothen(arr, w):
    cumsum_vec = np.cumsum(np.insert(arr, 0, 0)) 
    ma_vec = (cumsum_vec[w:] - cumsum_vec[:-w]) / w
    return ma_vec

def plot(trace):
    paths = [f'./experiment_results/trace{trace}_run{i}.json' for i in range(n_experiments)] 
    paths = [p for p in paths if os.path.exists(p)]
    print(paths)

    all_data = []
    all_steps = []
    all_rewards = []
    all_jumps = []

    for path in paths:
        with open(path, 'r') as f:
            data = json.load(f)
            # all_data.append(data)
            all_steps.append(data['all_steps'])
            all_rewards.append(data['all_rewards'])
            all_jumps.append(data['all_jumps'])

            if 0 in all_steps:
                print(all_steps.index(0))

    all_steps = np.array(all_steps).mean(axis=0)
    all_rewards = np.array(all_rewards).mean(axis=0)
    all_jumps = np.array(all_jumps).mean(axis=0)



    # plt.plot(all_rewards.mean(axis=0))
    plt.plot(smoothen(all_rewards, 10))
    plt.plot(smoothen(all_rewards, 100))
    plt.show()


if __name__ == '__main__':
    plot(1)
