"""
this file specifies the different versions of marioai
"""
from gym.envs.registration import register

from .reward_settings import RewardSettings

register(id='Marioai-v0',
        entry_point='gym_marioai.envs:MarioEnv',
        kwargs={})

# define other versions
# register(id='Marioai-v1',
#         entry_point='gym_marioai.envs:MarioEnv',
#         kwargs={})
