"""
container class to adjust the reward function of a MarioAI gym environment
"""
import dataclasses


@dataclasses.dataclass
class RewardSettings:
    progress: float = 1
    timestep: float = -.1
    mario_mode: float = 10
    kill: float = 1
    coin: float = 1
    # NOTE: changed from original
    win: float = 1000
    dead: float = -100
    cliff: float = 25
    # NOTE: added
    stuck: float = -4
