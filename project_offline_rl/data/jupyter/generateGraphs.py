# libraries
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # width of the bars
    barWidth = 0.3

    # Choose the height of the orange bars
    barsQ = [232, 176, -559]

    # Choose the height of the blue bars
    barsDQN = [280, 193, -34]

    # The x position of bars
    r1 = np.arange(len(barsDQN))
    r2 = [x + barWidth for x in r1]

    # Create blue bars
    plt.bar(r1, barsDQN, width=barWidth, edgecolor='black', capsize=7, label='DQN')

    # Create orange bars
    plt.bar(r2, barsQ, width=barWidth, edgecolor='black', capsize=7, label='Q-Learner')

    # general layout
    plt.xticks([r + barWidth for r in range(len(barsQ))], ['Easy level', 'Medium level', 'Hard level'])
    plt.ylabel('maximum reward')
    plt.axhline(y=0, color='r')

    plt.legend()

    # Show graphic
    plt.show()
