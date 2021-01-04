"""

"""
from typing import List, Optional
import gym
from gym import spaces

from ..proto import MySocket 
from .. import mario_pb2
from ..mario_pb2 import MarioMessage


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
            # abort
            raise e

        init_message = MarioMessage()
        init_message.type = MarioMessage.Type.INIT
        init_message.init.difficulty = self.difficulty
        init_message.init.seed = self.seed
        init_message.init.r_field_w = self.r_field_w
        init_message.init.r_field_h = self.r_field_h
        init_message.init.level_length = self.level_length
        # init_s = init_message.SerializeToString()
        # self.socket.mysend(init_s)
        self.socket.send_proto(init_message)

        self.__recv_state()

    def __del__(self):
        print('deleting environment...')
        self.socket.disconnect()

    def render(self, mode='human'):
        print('dummy rendering method called, has no effect yet')

    def __recv_state(self):
        # receive the state information
        # state = MarioMessage()
        # state.type = MarioMessage.Type.STATE
        # state.state.state = 42
        state = self.socket.receive_proto()
        print('state:\n', state)

        # # determine the length to read 
        # state_data = state.SerializeToString()
        # print('what we expect to receive: ', state_data)
        # # serialized_msg = self.socket.myreceive(len(state_data)+1)
        # serialized_msg = self.socket.receive()
        # print(serialized_msg)

        # # TODO this does not work yet...
        # state.ParseFromString(serialized_msg)
        return state

    def reset(self):
        init_message = MarioMessage()
        init_message.type = MarioMessage.Type.INIT
        init_message.init.difficulty = self.difficulty
        init_message.init.seed = self.seed
        init_message.init.r_field_w = self.r_field_w
        init_message.init.r_field_h = self.r_field_h
        init_message.init.level_length = self.level_length
        # init_s = init_message.SerializeToString()
        # self.socket.mysend(init_s)
        self.socket.send_proto(init_message)
        return self.__recv_state()

    def step(self, action:List[int]):
        assert len(action) == 6, 'step() expects an action list of length 6'

        # send the action
        msg = MarioMessage()
        msg.type = MarioMessage.Type.ACTION

        msg.action.up = action[0]
        msg.action.right = action[1]
        msg.action.down = action[2]
        msg.action.left = action[3]
        msg.action.speed = action[4]
        msg.action.jump = action[5]

        # serialized_msg = msg.SerializeToString()
        # self.socket.mysend(serialized_msg)
        self.socket.send_proto(msg)

        # receive the new state information
        new_state = self.__recv_state()

        # TODO obtain reward signal from state data
        reward = 0
        done = False
        info = ''

        return new_state, reward, done, info

