# libraries
import numpy as np
import matplotlib.pyplot as plt
 
# width of the bars
barWidth = 0.3
 
# Choose the height of the blue bars
barsQ = [10, 9, 2]
 
# Choose the height of the cyan bars
barsDQN = [10.8, 9.5, 4.5]
 
# Choose the height of the error bars (bars1)
yerQ = [0.5, 0.4, 0.5]
 
# Choose the height of the error bars (bars2)
yerDQN = [1, 0.7, 1]
 
# The x position of bars
r1 = np.arange(len(barsQ))
r2 = [x + barWidth for x in r1]
 
# Create blue bars
plt.bar(r1, barsQ, width = barWidth,  edgecolor = 'black', yerr=yerQ, capsize=7, label='Q_Learner')
 
# Create cyan bars
plt.bar(r2, barsDQN, width = barWidth, edgecolor = 'black', yerr=yerDQN, capsize=7, label='DQN')
 
# general layout
plt.xticks([r + barWidth for r in range(len(barsQ))], ['Easy level', 'Medium level', 'Hard level'])
plt.ylabel('maximum reward')
plt.legend()
 
# Show graphic
plt.show()