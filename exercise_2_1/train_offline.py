
from gym_setup import Env
import d3rlpy
from d3rlpy.dataset import MDPDataset
from d3rlpy.metrics.scorer import evaluate_on_environment
from sklearn.model_selection import train_test_split
env = Env(visible=False, port='8082')
env = env.get_env()

dataset = MDPDataset.load('exercise_2_1/data/player_data.h5')

train_episodes, test_episodes = train_test_split(dataset, test_size=0.2)

# prepare algorithm
opt = d3rlpy.models.optimizers.AdamFactory(optim_cls = 'Adam', betas = (0.9, 0.999), eps = 0.33, weight_decay = 0, asmgrad = False)
dqn = d3rlpy.algos.DQN(learning_rate=0.5, gamma=0.89, use_gpu=False)
#dqn = d3rlpy.algos.DoubleDQN(learning_rate=0.1, gamma=0.89, eps = 0.33)
# train offline
dqn.build_with_env(env)
# set environment in scorer function
evaluate_scorer = evaluate_on_environment(env)
# evaluate algorithm on the environment
rewards = evaluate_scorer(dqn)

dqn.fit(train_episodes, eval_episodes=test_episodes, n_epochs=10, scorers={
        'environment': evaluate_scorer
})

dqn.save_model('exercise_2_1/data/model.pt')

