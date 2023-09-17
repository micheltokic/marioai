dataset = getDataset()
print(len(dataset.episodes))
train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
train_dataset = ReplayBuffer(InfiniteBuffer(), episodes=train_episodes)
print(f"{len(train_episodes)=}")
print(f"{len(test_episodes)=}")

sac = d3rlpy.algos.DiscreteSACConfig( actor_learning_rate=learning_rate,
                                     critic_learning_rate=learning_rate,
                                     temp_learning_rate = learning_rate,
                                     gamma=gamma,
          batch_size=batch_size).create()

# set environment in scorer function
env_train = Env(visible=visible, level=str(level_paths.level)).env
sac.build_with_dataset(train_dataset)
env_evaluator  = EnvironmentEvaluator(env_train, n_trials=1)

# evaluate algorithm on the environment
name = 'SAC_marioai_%s_%s_%s_%s_%s' % (level_paths.level_name, gamma, learning_rate, target_update_interval, n_epochs)
model_file = pathlib.Path("data", "models", name + ".pt")
currentMax = -100000
sac_max = copy.deepcopy(sac)

fitter = sac.fitter(
   dataset,
   n_steps = n_steps_per_epoch * n_epochs,
   n_steps_per_epoch=n_steps_per_epoch,
  evaluators={'td_error': d3rlpy.metrics.TDErrorEvaluator(test_episodes),
              'value_scale': d3rlpy.metrics.AverageValueEstimationEvaluator(test_episodes),
              'environment': env_evaluator }
)
dataset.trajectory_slicer
for epoch, metrics in fitter:
    if metrics.get("environment") > currentMax:
        currentMax = metrics.get("environment")
        sac_max.copy_q_function_from(sac)
    else:
        sac.copy_q_function_from(sac_max)
    sac.save_model(model_file)
    if currentMax > 100:
        # For the purpose of the exercise the training will stop if the agent manages to complete the level
        print("A suitable model has been found.")
        break