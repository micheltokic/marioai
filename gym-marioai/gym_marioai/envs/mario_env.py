"""

"""
from typing import List, Optional
import gym
from gym import spaces

from ..proto import MySocket 
from .. import mario_pb2
from ..mario_pb2 import MarioMessage, State


class MarioEnv(gym.Env):

    def __init__(self, host='localhost', port=8080,
            difficulty=15,
            seed=2,
            r_field_w=3,
            r_field_h=4,
            level_length=5):
        """
        Environment initialization
        """

        self.difficulty = difficulty
        self.seed = seed
        self.r_field_w = r_field_w
        self.r_field_h = r_field_h
        self.level_length = level_length

        # define action space
        self.action_space = spaces.MultiBinary(6)

        # observation space is a binary feature vector
        n_features = 10
        self.observation_space = spaces.MultiBinary(n_features)

        try:
            self.socket = MySocket()
            self.socket.connect(host, port)
        except Exception as e:
            print(f'unable to connect to the server, is it running at ' \
                  f'{host}:{port}?\n')
            raise e

        print('connected to the server')
        msg = MarioMessage()
        msg.type = MarioMessage.Type.INIT
        msg.init.difficulty = self.difficulty
        msg.init.seed = self.seed
        msg.init.r_field_w = self.r_field_w
        msg.init.r_field_h = self.r_field_h
        msg.init.level_length = self.level_length
        self.socket.send(msg)
        print('sent init message')

        # do not wait for reply
        self.socket.receive()
        # self.__recv_state()

    def __del__(self):
        print('deleting environment...')
        self.socket.disconnect()

    def render(self, mode='human'):
        msg = MarioMessage()
        msg.type = MarioMessage.Type.RENDER
        self.socket.send(msg)
        # do not wait for response

    def reset(self):
        """
        reset the environment, return new initial state
        """
        msg = MarioMessage()
        msg.type = MarioMessage.Type.RESET
        self.socket.send(msg)
        print('sent reset message, waiting for state response')

        # assuming the response is a state message
        reply = self.socket.receive()
        assert reply.type == MarioMessage.Type.STATE
        return reply.state

    def step(self, action:List[int]):
        """
        perform action in the environment and return new state, reward,
        done and info
        """
        assert len(action) == 6, 'step() expects an action list of length 6'

        # contruct the action
        msg = MarioMessage()
        msg.type = MarioMessage.Type.ACTION
        msg.action.up = action[0]
        msg.action.right = action[1]
        msg.action.down = action[2]
        msg.action.left = action[3]
        msg.action.speed = action[4]
        msg.action.jump = action[5]

        self.socket.send(msg)

        # receive the new state information
        reply = self.socket.receive()
        assert reply.type == MarioMessage.Type.STATE

        state = reply.state
        game_status = state.game_status

        # TODO obtain reward signal from state data
        reward = 0
        done = game_status != State.GameStatus.RUNNING
        info = ''

        return state, reward, done, info

