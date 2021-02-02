"""
container class to adjust the reward function of a MarioAI gym environment
"""

class RewardSettings:

    def __init__(self, 
                progress=1,
                timestep=-.1,
                mario_mode=10,
                kill=1,
                win=100,
                dead=-100,
                cliff=25):

        self.progress = progress
        self.timestep = timestep
        self.mario_mode = mario_mode
        self.kill = kill
        self.win = win
        self.dead = dead
        self.cliff = cliff


