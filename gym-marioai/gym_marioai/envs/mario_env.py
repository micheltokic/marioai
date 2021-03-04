"""

"""
from collections import deque
import numpy as np
import gym
from gym import spaces

from ..protobuf_socket import ProtobufSocket
from ..mario_pb2 import MarioMessage, State
from ..reward_settings import RewardSettings


WIN = State.GameStatus.WIN
DEAD = State.GameStatus.DEAD
RUNNING = State.GameStatus.RUNNING
FLOOR = State.FLOOR
CLIFF = State.CLIFF


class MarioEnv(gym.Env):

    def __init__(self, host='localhost', port=8080,
                 render=False,
                 difficulty=0,
                 seed=1000,
                 rf_width=11,
                 rf_height=7,
                 level_length=80,
                 max_steps=0,
                 reward_settings=RewardSettings(),
                 compact_observation=True,
                 trace_length=1,
                 level_path="None"):
        """
        Environment initialization
        """

        self._render:bool = render
        self.difficulty = difficulty
        self.seed = seed
        self.level_length:int = level_length
        self.rf_width:int = rf_width
        self.rf_height:int = rf_height
        self.max_steps:int = max_steps
        self.reward_settings:RewardSettings = reward_settings
        self.level_path:str = level_path
        self.trace_length: int = trace_length
        self.compact_observation:bool = compact_observation or self.trace_length > 1 # always use compact when traces > 1

        self.received_states = {}
        self.last_hash = 0

        # TODO read this dynamically?
        self.n_features:int = 4   # number of features in one receptive field cell
        self.n_actions:int = 9

        # define action space
        self.action_space = spaces.Discrete(self.n_actions)

        # observation space is a binary feature vector
        self.observation_space = spaces.MultiBinary(self.trace_length * [self.rf_width * self.rf_height,
                                                     self.n_features])
        self.observation_trace = deque()

        # use different observation feature extractor 
        # depending on compact parameter
        self.__extract_observation = self.__extract_observation_encoded \
                if self.compact_observation else self.__extract_observation_default

        # cache some information about the current environent state
        self.mario_mode = None
        self.mario_pos = None
        self.steps = 0

        # store the last time the agent has been above floor or cliff 
        self.last_floor_x = None
        self.last_cliff_x = None
        self.cliff_jumps = 0

        try:
            self.socket = ProtobufSocket(self.n_actions)
            self.socket.connect(host, port)
            self.socket.send_init(difficulty, seed, rf_width, rf_height,
                                  level_length, level_path, render, 
                                  compact_observation)

        except ConnectionRefusedError as e:
            print(f'unable to connect to the server, is it running at '
                  f'{host}:{port}?\n')
            raise e

    def __del__(self):
        self.socket.disconnect()

    def render(self, mode='human'):
        pass

    def reset(self):
        """
        reset the environment, return new initial state
        """
        self.socket.send_reset()
        state_msg = self.socket.receive()
        self.__reset_cached_data(state_msg)
        return self.__extract_observation(state_msg)

    def step(self, action: int):
        """
        perform action in the environment and return new state, reward,
        done and info
        """
        # count = 1
        # self.socket.send_action(action)
        # state_msg = self.socket.receive()
        # while state_msg.state.hash_code == self.last_hash and count <=3:
        #     self.socket.send_action(action)
        #     state_msg = self.socket.receive()
        #     count += 1
        self.socket.send_action(action)
        state_msg = self.socket.receive()
        if state_msg.state.hash_code == self.last_hash:
            self.socket.send_action(action)
            state_msg = self.socket.receive()
        if state_msg.state.hash_code == self.last_hash:
            self.socket.send_action(action)
            state_msg = self.socket.receive()
        self.last_hash = state_msg.state.hash_code

        observation = self.__extract_observation(state_msg)
        reward = self.__extract_reward(state_msg)
        done = self.__extract_done(state_msg)
        info = self.__extract_info(state_msg)

        self.__update_cached_data(state_msg)

        return observation, reward, done, info

    def __reset_cached_data(self, res:MarioMessage):
        """
        called when env.reset() is called
        """
        s = res.state
        self.mario_mode = s.mode
        self.mario_pos = (s.mario_x, s.mario_y)
        self.kills_by_stomp = 0
        self.kills_by_fire = 0
        self.kills_by_shell = 0
        self.steps = 0 
        self.last_floor_x = None
        self.last_cliff_x = None
        self.cliff_jumps = 0
        self.observation_trace = deque()

    def __update_cached_data(self, res: MarioMessage):
        """
        some env information needs to be stored on the client side.
        e.g., mario's current position, to determine changes in position
        """
        s = res.state
        self.mario_mode = s.mode
        self.mario_pos = (s.mario_x, s.mario_y)
        self.kills_by_stomp = s.kills_by_stomp
        self.kills_by_fire = s.kills_by_fire
        self.kills_by_shell = s.kills_by_shell
        self.steps += 1

        if s.position == FLOOR:
            self.last_floor_x = s.mario_x
        elif s.position == CLIFF:
            self.last_cliff_x = s.mario_x

    def __extract_observation_default(self, res: MarioMessage):
        """
        return a compact representation of the environment state
        returns a numpy array of shape rf_width * rf_height x n_features
        """
        obs = np.frombuffer(res.state.rf_bytes, dtype=np.int8)
        # print(obs)

        # obs = np.zeros((self.rf_width * self.rf_height,
        #                 self.n_features), dtype=np.bool)
        # rf_cells = res.state.receptive_fields

        # for i in range(self.rf_width * self.rf_height):
        #     obs[i, 0] = rf_cells[i].enemy
        #     obs[i, 1] = rf_cells[i].obstacle
        #     obs[i, 2] = rf_cells[i].coin
        #     obs[i, 3] = rf_cells[i].itembox

        return obs

    def __extract_observation_encoded(self, res:MarioMessage):
        """
        if compact_observation is set, this method is used to extract
        the observation, which is a byte arrary in this case
        """
        if len(self.observation_trace) >= self.trace_length:
            self.observation_trace.popleft()
        hash = res.state.hash_code
        self.observation_trace.append(hash)
        # if hash not in self.received_states:
        #     self.received_states[hash] = self.__extract_observation_default(res)
        return tuple(self.observation_trace)

    def __extract_reward(self, res: MarioMessage):
        """
        calculate the reward based on some information from the state response
        This is just dummy code for now
        """
        s = res.state

        # determine if mario has just jumped over a cliff.
        # if yes, he obtains the cliff reward
        has_overcome_cliff = s.position == FLOOR\
                       and None not in (self.last_floor_x, self.last_cliff_x)\
                       and self.last_floor_x < self.last_cliff_x\
                       and self.last_cliff_x < s.mario_x

        reward = (self.reward_settings.timestep
        + self.reward_settings.progress * (s.mario_x - self.mario_pos[0])

        # reward for mario mode change. Modes: small=0, big=1, fire=2
        # this will be negative if mario gets downgraded and positive if mario
        # gets upgraded
        + self.reward_settings.mario_mode * (s.mode - self.mario_mode)

        # kills
        + self.reward_settings.kill * (
                s.kills_by_stomp + s.kills_by_fire + s.kills_by_shell -
                self.kills_by_stomp - self.kills_by_fire - self.kills_by_shell)

        # reward mario for making it across a cliff
        + (self.reward_settings.cliff if has_overcome_cliff else 0)

        # bonus for winning
        + self.reward_settings.win * (s.game_status == WIN)
        + self.reward_settings.dead * (s.game_status == DEAD)
        )
        
        if has_overcome_cliff:
            self.cliff_jumps += 1

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
