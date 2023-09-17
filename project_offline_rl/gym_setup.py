import socket
import subprocess
from contextlib import closing

import gym

import gym_marioai
import os

# reward function params
# FIXME: change these?
prog = 2
timestep = -1
mario_mode = 0
cliff = 0
kill = 0
coin = 0
win = 150
dead = -10

reward_settings = gym_marioai.RewardSettings(progress=prog, timestep=timestep, mario_mode=mario_mode, kill=kill,
                                             coin=coin, cliff=cliff,
                                             win=win, dead=dead,
                                             )


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class Env:
    def open(self, port):
        jar_file_path = os.path.join("project_offline_rl","marioai-server-0.2-jar-with-dependencies.jar")
        return subprocess.Popen(['java', '-jar', jar_file_path, '-p', str(port)])

    def __init__(self, visible=True, level='None', run_server=False, port=None):
        if port is None:
            port = find_free_port()
        print("Running on port", port)
        if run_server:
            self.server = self.open(port)
        self.all_actions = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.env = gym.make('Marioai-v2', should_render=visible,
                            level_path=level,
                            compact_observation=False,
                            # reward_settings=reward_settings,
                            enabled_actions=self.all_actions,
                            rf_width=20, rf_height=10,
                            port=port)
