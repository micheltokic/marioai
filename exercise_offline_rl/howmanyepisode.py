import pathlib
from data.datasets.getDatasets import getDataset, getSpecificDataset

# training initial
dataset_human = getSpecificDataset("CliffsAndEnemiesLevel.h5")
print(f"human generated: {len(dataset_human.episodes)}")
dataset_sarsa = getSpecificDataset("CliffsAndEnemiesLevel.sarsa.h5")
print(f"sarsa generated: {len(dataset_sarsa.episodes)}")
