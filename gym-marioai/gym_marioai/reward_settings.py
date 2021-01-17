"""
container class to adjust the reward function of a MarioAI gym environment
"""

class RewardSettings:

    def __init__(self, 
                progress=1,
                timestep=-0.1,
                kill=1,
                win=100,
                dead=-100):

        self.progress = progress
        self.timestep = timestep
        self.kill = kill
        self.win = win
        self.dead = dead


