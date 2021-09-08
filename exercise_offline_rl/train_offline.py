from data.datasets.getDatasets import getDataset
from gym_setup import Env
import d3rlpy
import pathlib
from d3rlpy.metrics.scorer import evaluate_on_environment
from sklearn.model_selection import train_test_split

MODEL_DIR = pathlib.Path("data", "models")
if not MODEL_DIR.exists():
    MODEL_DIR.mkdir(parents=True)

# Environment settings
level = "exercise_offline_rl/levels/RoughTerrainLevel.lvl"
port = 8085
run_server = True
visible = False

# Training parameters
gamma = 0.99
learning_rate = 0.0003
target_update_interval = 3000
n_epochs = 1
test_size = 0.1
batch_size = 2
n_frames = 1
n_steps = 40
use_gpu = False

if __name__ == '__main__':
    env = Env(visible=visible, port=port, level=level, run_server=run_server).env

    dataset = getDataset()

    train_episodes, test_episodes = train_test_split(dataset, test_size=test_size)

    dqn = d3rlpy.algos.DQN(learning_rate=learning_rate, gamma=gamma, use_gpu=use_gpu,
                           target_update_interval=target_update_interval, batch_size=batch_size)

    # train offline
    dqn.build_with_dataset(dataset)
    # set environment in scorer function
    evaluate_scorer = evaluate_on_environment(env)
    # evaluate algorithm on the environment
    rewards = evaluate_scorer(dqn)
    name = 'marioai_%s_%s_%s_%s_%s' % (level.split('/')[-1], gamma, learning_rate, target_update_interval, n_epochs)
    dqn.fit(train_episodes, eval_episodes=test_episodes, tensorboard_dir='runs', experiment_name=name,
            n_epochs=n_epochs, scorers={'environment': evaluate_scorer})

    model_file = pathlib.Path(MODEL_DIR, name + ".pt")
    dqn.save_model(model_file)
