from run_ddqn import run_ddqn

gamma_list = [0.8, 0.98, 0.99]
learning_rate_list =[0.1, 0.03, 0.003, 0.0003]
target_update_interval_list = [3000]
batch_size_list =[2, 20]

counter = 0
max_counter = len(gamma_list) * len(learning_rate_list) * len(target_update_interval_list) * len(batch_size_list)

for gamma in gamma_list:
	for learning_rate in learning_rate_list:
		for batch_size in batch_size_list:
			for target_update_interval in target_update_interval_list:
				counter += 1
				print(f"\n\nrunning with {gamma=}, {learning_rate=}, {batch_size=}, {target_update_interval}")
				print(f"{counter} of {max_counter}\n\n")
				run_ddqn(learning_rate, gamma, target_update_interval, batch_size)
