import gym
from gym_marioai import levels
import gym_marioai

# reward function params
prog = 2
timestep = -1
cliff = 5
kill = 1
coin = 1
win = 500
dead = -10

reward_settings = gym_marioai.RewardSettings(
    progress=prog, timestep=timestep, cliff=cliff, win=win, dead=dead, kill = kill, coin = coin)

class Env:
    def open(self, port):
        # Open Game
        from subprocess import Popen
        server_process = Popen(
            ['java', '-jar', 'gym-marioai\gym_marioai\server\marioai-server-0.1-jar-with-dependencies.jar', '-port', port])
    def __init__(self, visible=True, port='8080') -> None:
        self.open(port)
        self.all_actions = (0,1,2,3,4,5,6,7,8,9,10,11,12)
        self.env = gym.make('Marioai-v0', render=visible,
                    level_path=levels.one_cliff_level,
                    compact_observation=True,
                    reward_settings=reward_settings,
                    enabled_actions=self.all_actions,
                    rf_width=20, rf_height=10)

    def get_env(self):
        return self.env