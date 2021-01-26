"""
this file specifies the different versions of marioai
"""
from gym.envs.registration import register

from . import levels
from .reward_settings import RewardSettings

register(id='Marioai-v0',
        entry_point='gym_marioai.envs:MarioEnv',
        kwargs={
                'level_path':levels.easy_level
        })

register(id='Marioai-v1',
         entry_point='gym_marioai.envs:MarioEnv',
         kwargs={
                 'level_path':levels.flat_level
         })

register(id='Marioai-v2',
         entry_point='gym_marioai.envs:MarioEnv',
         kwargs={
                 'level_path':levels.hard_level
         })
# define other versions
# register(id='Marioai-v1',
#         entry_point='gym_marioai.envs:MarioEnv',
#         kwargs={})
