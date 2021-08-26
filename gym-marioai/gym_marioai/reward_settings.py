"""
container class to adjust the reward function of a MarioAI gym environment
"""

class RewardSettings:

    def __init__(self, 
                progress=2,
                timestep=-1,
                mario_mode=0,
                kill=0,
                coin=0,
                win=150,
                dead=-10,
                cliff=0
                 ):

        self.progress = progress
        self.timestep = timestep
        self.mario_mode = mario_mode
        self.kill = kill
        self.coin = coin
        self.win = win
        self.dead = dead
        self.cliff = cliff


