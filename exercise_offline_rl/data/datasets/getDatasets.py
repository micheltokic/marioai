import os
from d3rlpy.dataset import MDPDataset


def getDataset():
    dataset = None
    directory = os.path.dirname(os.path.realpath(__file__))
    for entry in os.scandir(directory):
        if entry.path.endswith(".h5") and entry.is_file():
            print(entry.path)
            if dataset is not None:
                dataset.extend(MDPDataset.load(entry.path))
            else:
                dataset = MDPDataset.load(entry.path)
    return dataset
