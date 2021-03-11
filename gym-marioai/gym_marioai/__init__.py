"""
this file specifies the different versions of marioai
"""
from gym.envs.registration import register

from . import levels

# needs to be imported here, so we can use "from gym_marioai import RewardSettings"
from .reward_settings import RewardSettings


register(id='Marioai-v0',
        entry_point='gym_marioai.envs:MarioEnv',
        kwargs={
                'level_path':levels.easy_level
        })

# environment used for the exercise
register(id='Marioai-v1',
         entry_point='gym_marioai.envs:MarioEnv',
         kwargs={
                 'level_path':levels.one_cliff_level,
                 'rf_width': 20,
                 'rf_height': 10,
                 'compact_observation': True
         })

# environment with the full action_space
register(id='Marioai-v2',
         entry_point='gym_marioai.envs:MarioEnv',
         kwargs={
                 'level_path':levels.hard_level,
                 'rf_width': 20,
                 'rf_height': 10,
                 'enabled_actions': (0,1,2,3,4,5,6,7,8,9,10,11,12)
         })

