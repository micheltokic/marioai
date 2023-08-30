import dataclasses
from pathlib import Path


@dataclasses.dataclass
class LevelPaths:
    level_name: str
    level: Path
    dataset_path: Path
    dataset_path_rand: Path

    def __init__(self, init_dir: Path, level_name: str):
        self.level_name = str(Path(level_name).stem)
        self.level = init_dir / Path("levels", level_name)
        self.dataset_path = init_dir / Path("data", "datasets", self.level_name + ".h5")
        self.dataset_path_rand = init_dir / Path("data", "datasets", self.level_name + ".random.h5")