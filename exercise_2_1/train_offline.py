
from gym_setup import Env
import d3rlpy
from d3rlpy.dataset import MDPDataset

env = Env(visible=False, port='8082')
env = env.get_env()

random_dataset = MDPDataset.load('exercise_2_1/data/q_data.h5')

# prepare algorithm
dqn = d3rlpy.algos.DQN(learning_rate=0.1, gamma=0.89)
#dqn = d3rlpy.algos.DoubleDQN(learning_rate=0.1, gamma=0.89, eps = 0.33)
# train offline
dqn.build_with_env(env)
dqn.fit(random_dataset, n_epochs=3)

dqn.save_model('exercise_2_1/data/model.pt')

