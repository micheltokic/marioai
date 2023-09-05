import pathlib
from data.datasets.getDatasets import getDataset, getSpecificDataset

level = pathlib.Path("levels", "ClimbLevel.lvl").resolve()
dataset_path = pathlib.Path("data", "datasets", level.stem + ".h5").resolve()
dataset_path_sarsa = pathlib.Path("data", "datasets", level.stem + ".sarsa.h5").resolve()


# training initial
dataset = getSpecificDataset("ClimbLevel.sarsa")
# train_episodes, test_episodes = train_test_split(dataset.episodes, test_size=test_size)
print("sarsa generate:")
print(len(dataset.episodes))

# print(dataset.episodes[0].observations[0].shape)