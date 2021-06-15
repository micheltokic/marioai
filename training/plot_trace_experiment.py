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


def plot_all_runs(trace, w=100):
    """
    plot all runs of a single trace parameter.
    uses a smoothing for the curves
    """
    paths = [f'./experiment_results/trace{trace}_run{i}.json' for i in range(n_experiments)] 
    paths = [p for p in paths if os.path.exists(p)]

    all_steps = []
    all_rewards = []
    all_jumps = []

    for path in paths:
        with open(path, 'r') as f:
            data = json.load(f)
            all_steps.append(data['all_steps'])
            all_rewards.append(data['all_rewards'])
            all_jumps.append(data['all_jumps'])

    # all_steps = np.array(all_steps).mean(axis=0)
    # all_rewards = np.array(all_rewards).mean(axis=0)
    all_jumps = np.array(all_jumps)

    for i, jumps in enumerate(all_jumps):
        plt.plot(smoothen(jumps, w), label=f'run {i}')

    # std = all_jumps.std(0)
    # mean = all_jumps.mean(0)
    # plt.fill_between(np.arange(0, n_episodes), mean-std, mean+std)

    plt.legend()
    plt.xlabel("episode")
    plt.ylabel("avg cliff jumps per episode")
    plt.grid()
    plt.savefig(f'./experiment_results/trace_{trace}_all_runs.png', bbox_inches='tight')
    plt.show()


def plot():
    for trace in [1,2,3]:
        paths = [f'./experiment_results/trace{trace}_run{i}.json' for i in range(n_experiments)] 
        paths = [p for p in paths if os.path.exists(p)]

        # all_steps = []
        # all_rewards = []
        all_jumps = []

        for path in paths:
            with open(path, 'r') as f:
                data = json.load(f)
                # all_steps.append(data['all_steps'])
                # all_rewards.append(data['all_rewards'])
                all_jumps.append(data['all_jumps'])

        # all_steps = np.array(all_steps).mean(axis=0)
        # all_rewards = np.array(all_rewards).mean(axis=0)
        all_jumps = np.array(all_jumps)

        mean = all_jumps.mean(0)
        # std = all_jumps.std(0)
        # plt.fill_between(np.arange(0, n_episodes), mean-std, mean+std)

        plt.plot(smoothen(mean, 50), label=f'trace {trace}')

    plt.legend()
    plt.xlabel("episode")
    plt.ylabel("avg cliff jumps per episode")
    plt.grid()
    plt.savefig('./experiment_results/traces_1-3.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    plot_all_runs(2)
    plot()
