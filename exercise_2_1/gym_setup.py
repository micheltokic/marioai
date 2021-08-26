import gym
import gym_marioai

# reward function params
prog = 2
timestep = -1
cliff = 0
kill = 0
coin = 0
win = 150
dead = -10

reward_settings = gym_marioai.RewardSettings(
    #progress=prog, timestep=timestep, cliff=cliff, win=win, dead=dead, kill = kill, coin = coin)
    progress=prog, timestep=timestep, win=win, dead=dead)

class Env:
    def open(self, port):
        # Open Game
        from subprocess import Popen
        server_process = Popen(
            ['java', '-jar', 'gym-marioai\gym_marioai\server\marioai-server-0.1-jar-with-dependencies.jar', '-p', port])
    def __init__(self, visible=True, port='8080', level='None') -> None:
        self.open(port)
        self.all_actions = (0,1,2,3,4,5,6,7,8,9,10,11,12)
        self.env = gym.make('Marioai-v0', render=visible,
                    level_path=level,
                    compact_observation=False,
                    reward_settings=reward_settings,
                    enabled_actions=self.all_actions,
                    rf_width=20, rf_height=10,
                    port=int(port))

    def get_env(self):
        return self.env