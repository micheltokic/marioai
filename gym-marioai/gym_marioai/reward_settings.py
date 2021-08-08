"""
container class to adjust the reward function of a MarioAI gym environment
"""

class RewardSettings:

    def __init__(self, 
                progress=1,
                timestep=-.05,
                mario_mode=10,
                kill=25,
                coin=25,
                win=250,
                dead=-100,
                cliff=10):

        self.progress = progress
        self.timestep = timestep
        self.mario_mode = mario_mode
        self.kill = kill
        self.coin = coin
        self.win = win
        self.dead = dead
        self.cliff = cliff


