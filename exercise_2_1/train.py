
from gym_setup import Env
import d3rlpy
from d3rlpy.dataset import MDPDataset

env = Env(visible=False)
env = env.get_env()

random_dataset = MDPDataset.load('exercise_2_1/data/random_data.h5')

# prepare algorithm
dqn = d3rlpy.algos.DQN()
# train offline
dqn.build_with_env(env)
dqn.fit(random_dataset, n_epochs=50)

dqn.save_model('exercise_2_1/data/model.pt')

