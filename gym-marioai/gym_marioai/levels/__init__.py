import os
from pathlib import Path


current_folder = Path(__file__).resolve().parent
__path = str(current_folder.relative_to(Path.cwd())) + "/"
print(__path)
print(current_folder)
# __path = os.path.dirname(os.path.realpath(__file__)) + '/'

easy_level = __path + 'easyLevel.lvl'
flat_level = __path + 'flatLevel.lvl'
hard_level = __path + 'hardLevel.lvl'
cliff_level = __path + 'cliffLevel.lvl'
one_cliff_level = __path + 'oneCliffLevel.lvl'
coin_level = __path + "coinLevel.lvl"
enemy_level = __path + "enemyLevel.lvl"
early_cliff_level = __path + "earlyCliffLevel.lvl"
none = "None"