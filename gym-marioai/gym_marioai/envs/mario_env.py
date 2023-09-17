"""

"""
import dataclasses
from collections import deque

import gym
import numpy as np
from gym import spaces

from .. import mario_pb2 as pb
from ..mario_pb2 import MarioMessage, State
from ..protobuf_socket import ProtobufSocket
from ..reward_settings import RewardSettings

WIN = State.GameStatus.WIN
DEAD = State.GameStatus.DEAD
RUNNING = State.GameStatus.RUNNING
FLOOR = State.FLOOR
CLIFF = State.CLIFF

all_action_names = ('LEFT', 'RIGHT', 'UP', 'DOWN', 'JUMP', 'SPEED_JUMP', 'SPEED_RIGHT', 'SPEED_LEFT', 'JUMP_RIGHT', \
                    'JUMP_LEFT', 'SPEED_JUMP_RIGHT', 'SPEED_JUMP_LEFT', 'NOTHING')
default_actions = (pb.DOWN,
                   pb.JUMP,
                   pb.SPEED_JUMP,
                   pb.SPEED_RIGHT,
                   pb.SPEED_LEFT,
                   pb.JUMP_RIGHT,
                   pb.JUMP_LEFT,
                   pb.SPEED_JUMP_RIGHT,
                   pb.SPEED_JUMP_LEFT)


@dataclasses.dataclass
class MarioEnv(gym.Env):
    host: str = 'localhost'
    port: int = 8080
    should_render: bool = False
    difficulty: int = 0
    seed: int = 1000
    rf_width: int = 11
    rf_height: int = 7
    level_length: int = 80
    max_steps: int = 0
    reward_settings: RewardSettings = RewardSettings()
    compact_observation: bool = False
    trace_length: int = 1
    repeat_action_until_new_observation: int = 2
    enabled_actions: tuple = default_actions
    level_path: str = "None"
    time_last_moved: int = 0

    def __post_init__(self):
        """
        Environment initialization
        """

        # add class attributes for every enabled action in uppercase letters to this instance
        for i, a in enumerate(self.enabled_actions):
            setattr(self, all_action_names[a], i)

        self.received_states = {}
        self.last_hash = 0

        # FIXME: what does this mean?
        self.n_features: int = 4  # number of features in one receptive field cell
        self.n_actions: int = len(self.enabled_actions)

        # define action space
        self.action_space = spaces.Discrete(self.n_actions)

        if self.compact_observation:
            low = np.iinfo(np.int32).min
            high = np.iinfo(np.int32).max

            # hash values as observation
            if self.trace_length == 1:
                self.observation_space = spaces.Box(low, high, shape=(1,), dtype=np.int32)
            else:
                # typle of hash values
                self.observation_space = spaces.Tuple(spaces=[
                    spaces.Box(low, high, shape=(1,), dtype=np.int32) for _ in range(self.trace_length)])
        else:
            # observation space is a binary feature vector
            # FIXME: this has shape (200, 4)
            # self.observation_space = spaces.MultiBinary(self.trace_length * [self.rf_width * self.rf_height,
            #                                                                  self.n_features])
            self.observation_space = spaces.MultiBinary(800)
        self.observation_trace = deque()

        # use different observation feature extractor
        # depending on compact parameter
        self.__extract_observation = self.__extract_observation_encoded \
            if self.compact_observation else self.__extract_observation_default

        # cache some information about the current environent state
        self.mario_mode = None
        self.mario_pos: tuple[int, int] = None
        self.steps = 0

        # store the last time the agent has been above floor or cliff
        self.last_floor_x = -1
        self.last_cliff_x = -1
        self.cliff_jumps = 0

        try:
            self.socket = ProtobufSocket(self.enabled_actions)
            self.socket.connect(self.host, self.port)
            self.socket.send_init(self.difficulty, self.seed, self.rf_width, self.rf_height,
                                  self.level_length, self.level_path, self.should_render)

        except ConnectionRefusedError as e:
            print(f'unable to connect to the server, is it running at '
                  f'{self.host}:{self.port}?\n')
            raise e

    def teardown(self):
        self.socket.disconnect()
        print('socket disconnected.')

    def render(self, mode='human'):
        pass

    def reset(self, seed=None, difficulty=None, level_path="None", render=None, options=None):
        """
        reset the environment, return new initial state
        """
        re_init = False
        if difficulty is not None:
            self.difficulty = difficulty
            re_init = True
        if level_path != "None":
            self.level_path = level_path
            re_init = True
        if seed is not None:
            self.seed = seed
            self.level_path = "None"  # needs to be unset for seed to work
            re_init = True
        if render is not None:
            self._render = render
            re_init = True

        if re_init:
            self.socket.send_init(self.difficulty, self.seed,
                                  self.rf_width, self.rf_height,
                                  self.level_length, self.level_path, self._render)

        self.socket.send_reset()
        state_msg = self.socket.receive()
        self.__reset_cached_data(state_msg)
        info = self.__extract_info(state_msg)

        return self.__extract_observation(state_msg), info

    def step(self, action: int):
        """
        perform action in the environment and return new state, reward,
        done and info
        """
        self.socket.send_action(action)
        state_msg = self.socket.receive()
        for _ in range(self.repeat_action_until_new_observation):
            if state_msg.state.hash_code == self.last_hash:
                self.socket.send_action(action)
                state_msg = self.socket.receive()
            else:
                break
        self.last_hash = state_msg.state.hash_code

        observation = self.__extract_observation(state_msg)
        reward = self.__extract_reward(state_msg)
        terminated = self.__extract_done(state_msg)
        info = self.__extract_info(state_msg)
        truncated = False
        self.__update_cached_data(state_msg)

        return observation, reward, terminated, truncated, info

    def __reset_cached_data(self, res: MarioMessage):
        """
        called when env.reset() is called
        """
        s = res.state
        self.mario_mode = s.mode
        self.mario_pos = (s.mario_x, s.mario_y)
        self.kills_by_stomp = 0
        self.kills_by_fire = 0
        self.kills_by_shell = 0
        self.coins = 0
        self.steps = 0
        self.last_floor_x = -1
        self.last_cliff_x = -1
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
        self.coins = s.coins
        self.steps += 1

        if s.position == FLOOR:
            self.last_floor_x = s.mario_x
        elif s.position == CLIFF:
            self.last_cliff_x = s.mario_x

    def __extract_observation_default(self, res: MarioMessage):
        """
        return a compact representation of the environment state
        # FIXME: is is * n_features or x n_features?
        returns a numpy array of shape rf_width * rf_height x n_features
        """
        code = res.state.hash_code

        if code in self.received_states:
            obs = self.received_states[code]
        else:
            obs = np.frombuffer(res.state.rf_bytes, dtype=np.int8)
            self.received_states[code] = obs

        if self.trace_length == 1:
            # FIXME: = 800
            # print(f"{obs.shape=}")
            return obs
        else:
            if len(self.observation_trace) >= self.trace_length:
                self.observation_trace.popleft()
            self.observation_trace.append(obs)
            # NOTE: currently broken
            return np.concatenate(self.observation_trace)

    def __extract_observation_encoded(self, res: MarioMessage):
        """
        if compact_observation is set, this method is used to extract
        the observation, which is a byte array in this case
        """
        if self.trace_length == 1:
            return res.state.hash_code
        else:
            if len(self.observation_trace) >= self.trace_length:
                self.observation_trace.popleft()
            hash = res.state.hash_code
            self.observation_trace.append(hash)
            return tuple(self.observation_trace)

    def __extract_reward(self, res: MarioMessage):
        """
        calculate the reward based on some information from the state response
        This is just dummy code for now
        """
        s = res.state

        # determine if mario has just jumped over a cliff.
        # if yes, he obtains the cliff reward
        has_overcome_cliff = s.position == FLOOR \
                             and self.last_floor_x < self.last_cliff_x \
                             and self.last_cliff_x < s.mario_x

        # FIXME: implement more here

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

                  # collected coins
                  + self.reward_settings.coin * (s.coins - self.coins)

                  # reward mario for making it across a cliff
                  + (self.reward_settings.cliff if has_overcome_cliff else 0)

                  # bonus for winning
                  + self.reward_settings.win * (s.game_status == WIN)
                  + self.reward_settings.dead * (s.game_status == DEAD)
                  )

        # add reward for being stuck for an extended period of time
        # if for more than n seconds, add a stuck reward
        # 24 fps * seconds
        if self.time_last_moved >= 24 * 5:
            print("stuck reward added")
            reward += self.reward_settings.stuck
            # FIXME: needs to be reset here
            # should be reset somewhere, so that if movement occurs again,
            # it should not be in this branch
            # FIXME: just do value - 10 or something?
            self.time_last_moved = 0
        # mario has not moved in a while
        elif s.mario_x == self.last_floor_x:
            self.time_last_moved += 1
        # mario has moved, reset
        else:
            self.time_last_moved = 0

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
            'cliff_jumps': self.cliff_jumps
        }
