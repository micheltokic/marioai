# Using new levels
## Generating Levels

Run
```
java marioai-engine/src/ch/idsia/scenarios/Main.java [level-params] -s [filename]
```
with level-params from the options listed in `marioai-engine/doc/CmdLineOptions`
(examples available in `marioai-engine/doc/marioai-lvlgen-options-usage`).

The generated level will be saved to `marioai-engine/filename`.


## Adding levels
- Move the generated file to `gym-marioai/gym_marioai/levels`.
- Add the new level in `gym-marioai/gym_marioai/levels/__init__.py`.
- Run `pip install .` in the `gym-marioai` directory.

The level can now be used in `training/main.py`.