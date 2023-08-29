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
    win: float = 100
    dead: float = -100
    cliff: float = 25
    stuck: float = -100
