# libraries
import numpy as np
import matplotlib.pyplot as plt
 
# width of the bars
barWidth = 0.3
 
# Choose the height of the blue bars
barsQ = [232, 176, -559]
 
# Choose the height of the cyan bars
barsDQN = [280, 193, -34]
 

# The x position of bars
r1 = np.arange(len(barsQ))
r2 = [x + barWidth for x in r1]
 
# Create blue bars
plt.bar(r1, barsQ, width = barWidth,  edgecolor = 'black', capsize=7, label='Q_Learner')
 
# Create cyan bars
plt.bar(r2, barsDQN, width = barWidth, edgecolor = 'black', capsize=7, label='DQN')
 
# general layout
plt.xticks([r + barWidth for r in range(len(barsQ))], ['Easy level', 'Medium level', 'Hard level'])
plt.ylabel('maximum reward')

plt.legend()
 
# Show graphic
plt.savefig("exercise_2_1/data/jupyter/level-summary.png")