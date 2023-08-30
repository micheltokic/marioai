import os

from d3rlpy.dataset import ReplayBuffer, InfiniteBuffer


def getDataset():
    dataset = None
    directory = os.path.dirname(os.path.realpath(__file__))
    for entry in os.scandir(directory):
        if entry.path.endswith(".h5") and entry.is_file():
            print(f"getDataset dataset: {entry.path}")
            if dataset is not None:
                # dataset = ReplayBuffer.load(entry.path, InfiniteBuffer())
                for episode in ReplayBuffer.load(entry.path, InfiniteBuffer()).episodes:
                    dataset.append_episode(episode)
            else:
                dataset = ReplayBuffer.load(entry.path, InfiniteBuffer())
    return dataset


def getSpecificDataset(level_name):
    dataset = None
    directory = os.path.dirname(os.path.realpath(__file__))
    for entry in os.scandir(directory):
        if entry.path.endswith(".h5") and entry.is_file() and level_name in entry.name:
            print(entry.path)
            if dataset is not None:
                for episode in ReplayBuffer.load(entry.path, InfiniteBuffer()).episodes:
                    dataset.append_episode(episode)
            else:
                dataset = ReplayBuffer.load(entry.path, InfiniteBuffer())
    return dataset
