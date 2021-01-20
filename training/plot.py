import os
import sys
import json

import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, n=3):
    """
    calculates moving average over a one-dimensional np array x
    the first n-1 elements are prepended, so it
    returns an array of the same length as x
    """
    avg = np.convolve(x, np.ones(n), 'valid') / n
    return np.concatenate((x[:n-1], avg))


def plot_training_curve(data, filename, avg=50):

    rewards = data['rewards']
    steps = data['steps']
    success = data['success']

    rewards = moving_average(np.array(rewards), avg)
    steps = moving_average(np.array(steps), avg)
    success = moving_average(np.array(success, dtype=np.byte), avg)


    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    # plot rewards
    ax1.plot(rewards)
    ax1.set_title('reward')
    ax1.set_xlabel('episode')

    # plot steps
    ax2.plot(steps)
    ax2.set_title('steps')
    ax2.set_xlabel('episode')

    # plot success rate
    ax3.plot(success)
    ax3.set_title('success rate')
    ax3.set_xlabel('episode')

    plot_path = os.path.dirname(os.path.realpath(__file__)) \
                + '/plots/' + filename + '.png'
    plt.savefig(plot_path)
    plt.show()


if __name__ == '__main__':
    assert len(sys.argv) == 2, "please give name of result file"

    result_file_path = os.path.dirname(os.path.realpath(__file__)) \
                + '/results/' + sys.argv[1] + '.json'

    with open(result_file_path, 'r') as f:
        data = json.load(f)
        plot_training_curve(data, sys.argv[1])

