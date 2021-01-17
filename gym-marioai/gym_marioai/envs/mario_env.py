"""

"""
from typing import List
import numpy as np
import gym
from gym import spaces

from ..protobuf_socket import ProtobufSocket
from ..mario_pb2 import Action, MarioMessage, State
from ..reward_settings import RewardSettings


WIN = State.GameStatus.WIN
DEAD = State.GameStatus.DEAD
RUNNING = State.GameStatus.RUNNING


class MarioEnv(gym.Env):

    def __init__(self, host='localhost', port=8080,
                 visible=False,
                 difficulty=0,
                 seed=1000,
                 rf_width=3,
                 rf_height=4,
                 level_length=80,
                 max_steps=0,
                 reward_settings=RewardSettings(),
                 file_name="None"):
        """
        Environment initialization
        """

        self.visible:bool = visible
        self.difficulty = difficulty
        self.seed = seed
        self.level_length:int = level_length
        self.rf_width:int = rf_width
        self.rf_height:int = rf_height
        self.max_steps:int = max_steps
        self.reward_settings:RewardSettings = reward_settings
        self.file_name:str = file_name

        # TODO read this dynamically?
        self.n_features:int = 4   # number of features in one receptive field cell

        # define action space
        self.action_space = spaces.Discrete(9)

        # observation space is a binary feature vector
        self.observation_space = spaces.MultiBinary([self.rf_width * self.rf_height,
                                                     self.n_features])

        # cache some information about the current environent state
        self.mario_pos = None
        self.steps = 0

        try:
            self.socket = ProtobufSocket()
            self.socket.connect(host, port)
        except ConnectionRefusedError as e:
            print(f'unable to connect to the server, is it running at '
                  f'{host}:{port}?\n')
            raise e

        self.__send_init_message()

    def __del__(self):
        print('deleting environment...')
        self.socket.disconnect()

    def render(self, mode='human'):
        pass

    def reset(self):
        """
        reset the environment, return new initial state
        """
        msg = MarioMessage()
        msg.type = MarioMessage.Type.RESET
        self.socket.send(msg)

        # assuming the response is a state message
        reply = self.socket.receive()
        assert reply.type == MarioMessage.Type.STATE
        self.__update_cached_data(reply)
        self.steps = 0
        return self.__extract_observation(reply)

    def step(self, action: int):
        """
        perform action in the environment and return new state, reward,
        done and info
        """
        # action_enum = Action.Value
        self.__send_action_message(action)

        # receive the new state information
        reply = self.socket.receive()
        assert reply.type == MarioMessage.Type.STATE

        observation = self.__extract_observation(reply)
        reward = self.__extract_reward(reply)
        done = self.__extract_done(reply)
        info = self.__extract_info(reply)

        self.__update_cached_data(reply)

        return observation, reward, done, info

    def __send_init_message(self):
        msg = MarioMessage()
        msg.type = MarioMessage.Type.INIT
        msg.init.render = self.visible
        msg.init.difficulty = self.difficulty
        msg.init.seed = self.seed
        msg.init.r_field_w = self.rf_width
        msg.init.r_field_h = self.rf_height
        msg.init.level_length = self.level_length
        msg.init.file_name = self.file_name
        self.socket.send(msg)

    def __send_action_message(self, action: Action):
        msg = MarioMessage()
        msg.type = MarioMessage.Type.ACTION
        msg.action = action
        self.socket.send(msg)

    def __update_cached_data(self, res: MarioMessage):
        """
        some env information needs to be stored on the client side.
        e.g., mario's current position, to determine changes in position
        """
        s = res.state
        self.mario_pos = (s.mario_x, s.mario_y)
        self.kills_by_stomp = s.kills_by_stomp
        self.kills_by_fire = s.kills_by_fire
        self.kills_by_shell = s.kills_by_shell
        self.steps += 1

    def __extract_observation(self, res: MarioMessage):
        """
        return a compact representation of the environment state
        returns a numpy array of shape rf_width * rf_height x n_features
        """
        obs = np.zeros((self.rf_width * self.rf_height,
                        self.n_features), dtype=np.bool)
        rf_cells = res.state.receptive_fields

        for i in range(self.rf_width * self.rf_height):
            cell = rf_cells[i]
            cell_state = np.array(
                [cell.enemy, cell.obstacle, cell.coin, cell.itembox])
            obs[i] = cell_state

        # for y in range(self.rf_height):
        #     for x in range(self.rf_width):
        #         idx = y*self.rf_width + x
        #         cell = rf_cells[idx]
        #         cell_state = np.array(
        #             [cell.enemy, cell.obstacle, cell.coin, cell.itembox])
        #         obs[idx] = cell_state
        return obs

    def __extract_reward(self, res: MarioMessage):
        """
        calculate the reward based on some information from the state response
        This is just dummy code for now
        """
        s = res.state

        reward = 0
        reward += self.reward_settings.timestep  
        reward += self.reward_settings.progress * (s.mario_x - self.mario_pos[0])

        # kills
        reward += self.reward_settings.kill * (s.kills_by_stomp - self.kills_by_stomp)
        reward += self.reward_settings.kill * (s.kills_by_fire - self.kills_by_fire)
        reward += self.reward_settings.kill * (s.kills_by_shell - self.kills_by_shell)

        # bonus for winning
        reward += self.reward_settings.win * (res.state.game_status == WIN)
        reward += self.reward_settings.dead * (res.state.game_status == DEAD)

        return reward

    def __extract_done(self, res: MarioMessage):
        """
        check whether the episode is terminated
        """
        if self.max_steps > 0 and self.steps >= self.max_steps:
            return True

        return res.state.game_status != RUNNING

    def __extract_info(self, res: MarioMessage):
        """
        returns additional statistics, information that should not be used 
        for training
        """
        return {
                'win': res.state.game_status == WIN,
                'steps': self.steps,
                }
