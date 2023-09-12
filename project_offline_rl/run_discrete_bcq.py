#!/usr/bin/env python
# coding: utf-8
import pathlib

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    print("matplotlib could not be imported")

import d3rlpy.dataset
from d3rlpy.dataset import ReplayBuffer
from d3rlpy.dataset.buffers import InfiniteBuffer
from d3rlpy.metrics import EnvironmentEvaluator
from sklearn.model_selection import train_test_split

from data.datasets.getDatasets import getSpecificDataset
from get_paths import LevelPaths
from gym_setup import Env
import training_params


def run_discrete_cql(learning_rate, gamma, target_update_interval, batch_size, graph=False, visible=False):
    n_epochs = training_params.n_epochs
    n_steps_per_epoch = training_params.n_steps_per_epoch
    test_size = training_params.test_size
    use_gpu = training_params.use_gpu

    # Setup global variables
    # init_dir = pathlib.Path(__file__).parent
    init_dir = pathlib.Path("./project_offline_rl")
    # level_paths: LevelPaths = LevelPaths(init_dir, "ClimbLevel.lvl")
    level_paths: LevelPaths = LevelPaths(init_dir, "CliffsAndEnemiesLevel.lvl")

    print(f"level location={level_paths.level}")

    # run_ddqn
    # dataset = getDataset()
    dataset = getSpecificDataset(level_paths.level_name)
    train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
    train_dataset = ReplayBuffer(InfiniteBuffer(), episodes=train_episodes)
    print(f"{len(train_episodes)=}")
    print(f"{len(test_episodes)=}")

    losses = []
    epochs = []
    tderror = []

    bcq = d3rlpy.algos.DiscreteBCQConfig(learning_rate=learning_rate, gamma=gamma,
                                         target_update_interval=target_update_interval,
                                         batch_size=batch_size).create()
    # Needs to be rebuilt
    bcq.build_with_dataset(train_dataset)

    # set environment in scorer function
    env_train = Env(visible=visible, level=str(level_paths.level), port=8080).env
    # set environment in scorer function
    # only run right now, as there is no randomness in the game
    env_evaluator = EnvironmentEvaluator(env_train, n_trials=1)

    # evaluate algorithm on the environment

    name = 'BCQ_marioai_%s_%s_%s_%s_%s_%s' % (
        level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs, batch_size)
    model_file = init_dir / pathlib.Path("data", "models", name + ".pt")
    currentMax = -100000

    fitter = bcq.fitter(
        dataset,
        n_steps=n_steps_per_epoch * n_epochs,
        n_steps_per_epoch=n_steps_per_epoch,
        evaluators={'td_error': d3rlpy.metrics.TDErrorEvaluator(test_episodes),
                    'value_scale': d3rlpy.metrics.AverageValueEstimationEvaluator(test_episodes),
                    'environment': env_evaluator}
    )

    for epoch, metrics in fitter:
        current_reward = metrics.get("environment")
        print(f"{current_reward=}")
        if current_reward > currentMax:
            print("saving version to file")
            currentMax = current_reward
            bcq.save_model(model_file)

        loss = metrics.get("loss")
        losses.append(loss)
        epochs.append(epoch)
        td_error = metrics.get("td_error")
        tderror.append(td_error)

        # FIXME: what is the correct value?
        if current_reward > 1000:
            # For the purpose of the exercise the training will stop if the agent manages to complete the level
            print("A suitable model has been found.")
            break
    # this is needed to close the socket to the java program or else it does not work when called multiple times.
    env_train.teardown()

    if graph:
        # Plot loss vs. epoch
        plt.figure(figsize=(10, 6))
        plt.plot(epochs, losses, marker='o', label='Loss')
        scaled_tderror = [td / 1000.0 for td in tderror]  # Scale TD error for visualization
        plt.plot(epochs, scaled_tderror, marker='x', label='TD Error (Scaled)')
        plt.xlabel('Epoch')
        plt.ylabel('Loss / TD Error (Scaled)')
        plt.title('Loss and TD Error vs. Epoch')
        plt.legend()
        plt.grid(True)

        # Save the plot
        plot_image_file = "loss_tderror_vs_epoch_plot.png"
        # plot_image_file = "loss_tderror_vs_epoch_plot_4Sarsa.png"
        plt.savefig(plot_image_file)
        plt.show()

        print(max(losses) - min(losses))


if __name__ == '__main__':
    run_discrete_cql(training_params.learning_rate, training_params.gamma, training_params.target_update_interval,
                     training_params.batch_size)
