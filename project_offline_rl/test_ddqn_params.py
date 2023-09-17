from test_ddqn import test_ddqn
import sys

# Only test on the combinations where goal was found

# form of gamma, learning rate, batchsize
# Total of 6
combinations = [[0.8, 0.1, 20], [0.8, 0.03, 20], [0.98, 0.03, 20], [0.99, 0.03, 2], [0.99, 0.03, 20], [0.99, 0.0003, 20]]
target_update_interval = 3000

all_levels = ["OneCliffLevel.lvl", "CliffsAndEnemiesLevel.lvl", "ClimbLevel.lvl", "RoughTerrainLevel.lvl"]


main_level = "CliffsAndEnemiesLevel.lvl"
test_level = all_levels[int(sys.argv[1])]

visible = False

counter = 0
max_counter = len(combinations)

for gamma, learning_rate, batch_size in combinations:
	counter += 1
	print(f"\n\nrunning with {gamma=}, {learning_rate=}, {batch_size=}, {target_update_interval}")
	print(f"{counter} of {max_counter}\n\n")
	print(f"testing level {test_level}")
	test_ddqn("CliffsAndEnemiesLevel.lvl", test_level, learning_rate, gamma, target_update_interval, batch_size, visible=visible)
