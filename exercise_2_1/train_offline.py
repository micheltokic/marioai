
from data.datasets.getDatasets import getDataset
from gym_setup import Env
import d3rlpy
from d3rlpy.metrics.scorer import evaluate_on_environment
from sklearn.model_selection import train_test_split
from gym_marioai import levels

env = Env(visible=False, port='8083', level=levels.cliff_level)
env = env.get_env()


dataset = getDataset()

train_episodes, test_episodes = train_test_split(dataset, test_size=0.2)

# prepare algorithm
opt = d3rlpy.models.optimizers.AdamFactory(optim_cls = 'Adam', betas = (0.9, 0.999), eps = 0.1, weight_decay = 0, asmgrad = False)
dqn = d3rlpy.algos.DQN(learning_rate=3e-4, gamma=0.7, use_gpu=False, target_update_interval=5000) #target_update_interval anpassen epochenzahl* 6
#dqn = d3rlpy.algos.DoubleDQN(learning_rate=0.1, gamma=0.89, eps = 0.33)
# train offline
dqn.build_with_dataset(dataset)
# set environment in scorer function
evaluate_scorer = evaluate_on_environment(env)
# evaluate algorithm on the environment
rewards = evaluate_scorer(dqn)

dqn.fit(train_episodes, eval_episodes=test_episodes, n_epochs=20, scorers={
        'environment': evaluate_scorer
})

dqn.save_model('exercise_2_1/data/models/model.pt')

