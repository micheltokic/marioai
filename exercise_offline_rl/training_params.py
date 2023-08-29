# Training parameters
n_epochs = 20  # <--- change here if you want to train more / less
n_steps_per_epoch = 1000
test_size = 0.1  # percentage of episodes not used for training

# DQN parameters
learning_rate = 0.0003  # to what extent the agent overrides old information with new information
gamma = 0.99  # discount factor, how important future rewards are
target_update_interval = 3000  # interval of steps that the agent uses to update target network
batch_size = 50  # size of training examples utilized in one iteration
use_gpu = False  # usage of gpu to train