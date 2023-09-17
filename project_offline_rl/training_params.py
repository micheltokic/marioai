# Training parameters
n_epochs = 10  # <--- change here if you want to train more / less
n_steps_per_epoch = 1000
test_size = 0.1  # percentage of episodes not used for training
use_gpu = False  # usage of gpu to train

# DQN parameters
learning_rate = 0.03  # to what extent the agent overrides old information with new information
gamma = 0.99  # discount factor, how important future rewards are
target_update_interval = 3000  # interval of steps that the agent uses to update target network
batch_size = 20  # size of training examples utilized in one iteration