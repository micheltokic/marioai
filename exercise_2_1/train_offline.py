from data.datasets.getDatasets import getDataset
from gym_setup import Env
import d3rlpy
from d3rlpy.metrics.scorer import evaluate_on_environment
from sklearn.model_selection import train_test_split

level = "exercise_2_1/levels/CliffsAndEnemiesLevel.lvl"

if __name__ == '__main__':
    env = Env(visible=False, port='8085', level=level, run_server=True).env

    dataset = getDataset()

    train_episodes, test_episodes = train_test_split(dataset, test_size=0.1)

    gamma = 0.9
    learningrate = 0.0003
    target_update_interval = 5000

    dqn = d3rlpy.algos.DQN(learning_rate=learningrate, gamma=gamma, use_gpu=True,
                                 target_update_interval=target_update_interval)  # , encoder_factory=encoder_factory)  # target_update_interval anpassen epochenzahl* 6
    #dqn = d3rlpy.algos.DoubleDQN(learning_rate=0.1, gamma=0.89, eps = 0.33)
    # train offline
    dqn.build_with_dataset(dataset)
    # set environment in scorer function
    evaluate_scorer = evaluate_on_environment(env)
    # evaluate algorithm on the environment
    rewards = evaluate_scorer(dqn)
    name = 'marioai_:%s_%s_%s_%s_' % (level.split(
        '/')[-1], gamma, learningrate, target_update_interval)
    dqn.fit(train_episodes, eval_episodes=test_episodes, tensorboard_dir='runs',  experiment_name=name, n_epochs=100, scorers={
        'environment': evaluate_scorer
    })

    dqn.save_model('exercise_2_1/data/models/%s.pt' % (name))
