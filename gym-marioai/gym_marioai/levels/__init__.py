import os

__path = os.path.dirname(os.path.abspath(__file__))


def level(name):
    return os.path.join(__path, name)


block_level = level('blockLevel.lvl')
block_and_coin_level = level('blockAndCoinLevel.lvl')
cannon_level = level('cannonLevel.lvl')
test_level = level('testLevel.lvl')
easy_level = level('easyLevel.lvl')
flat_level = level('flatLevel.lvl')
hard_level = level('hardLevel.lvl')
cliff_level = level('cliffLevel.lvl')
one_cliff_level = level('oneCliffLevel.lvl')
coin_level = level('coinLevel.lvl')
enemy_level = level('enemyLevel.lvl')
early_cliff_level = level('earlyCliffLevel.lvl')
none = 'None'
