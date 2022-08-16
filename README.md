# marioai

This is a clone of the MarioAI engine https://code.google.com/archive/p/marioai/downloads. Additionally all dependencies are managed via Maven.  
gym_marioai is a python gym interface that communicates with a java wrapper around the original MarioAI engine.

# Quickstart

This instruction will help you to get the environment up and running.  
It is necessary to start the java server first, and then initiate the connection on the python side.  
A precompiled version of the server .jar is included in the gym_marioai package. You will require Java 1.8 to execute it.

# Youtube video:

Watch a video of how Mario learns behavior using this library: https://www.youtube.com/watch?v=oVZokBoSE-I

### 1) Requirements

- Java runtime 1.8 (`java -version` should output something like `... version "1.8.*"`).
- python 3.7, pip

### 2) install the package

in `./gym_marioai`, run `pip install .`

### 3) run the server

in `./gym_marioai/gym-marioai/server/`, run `java -jar ./marioai-server-0.1-jar-with-dependencies.jar`. The parameter `-p` allows to specify a port (default is 8080)

### 4) run the demo

navigate to `./gym_marioai/demo/`, then run `python demo.py`. This will open a separate window with Mario performing random actions in the environment.

### MacOS additional steps

to be able to control Mario when running `play.py` on MacOS, additional permissions must be granted. This can be done via System Preferences -> Security & Privacy -> Tab 'Privacy'.
In the categories 'Accessibility' and 'Input-Monitoring', open the lock to allow editing and add your respective IDE (e.g. Visual Studio Code or Terminal) to the list.
Then, run the program with administrator permissions: `sudo python play.py`.

# API

Initialization of the environment:  
The environment is entirely configured using the `gym.make()` function. Here is an overview of all available parameters including its default values:

```
env = gym.make("Marioai-v0", host, port, render, rf_width, rf_height,
               difficulty, seed, level_path, level_length, max_steps,
               reward_settings, compact_observation, trace_length,
               repeat_action_until_new_observation, enabled_actions)
```

This will attempt to connect to a running server instance on `host:port`.
| parameter | default value | description |
| --- | --- | --- |
| `host` | 'localhost' | server address
| `port` | 8080 | server port
| `render` | False |
| `rf_width` | 11 | receptive field width
| `rf_height` | 7 | receptive field height
| `difficulty` | 0 |
| `seed` | 1000 |
| `level_path` | "None" | takes precedence over `seed` if other than "None"
| `level_length` | 80 |
| `max_steps` | 0 |
| `reward_settings` | RewardSettings() | option to change the default reward function, see below
| `compact_observation` | False | will use only a hash value if set to `True`. see below for more information
| `trace_length` | 1 | use consecutive frames as state information. You can also use a FrameStack wrapper (https://github.com/openai/gym/blob/master/gym/wrappers/frame_stack.py)
| `repeat_action_until_new_observation` | 2 |
| `enabled_actions` | default_actions | The default actions are DOWN, JUMP, SPEED_JUMP, SPEED_RIGHT, SPEED_LEFT, JUMP_RIGHT, JUMP_LEFT, SPEED_JUMP_RIGHT, SPEED_JUMP_LEFT |

#### Modifying the reward function

```
from gym_marioai import RewardSettings

reward_settings = RewardSettings(progress=1, timestep=-.1, mario_mode=10, kill=1,
                                 coin=1, win=100, dead=-100, cliff=25)
```

#### Use custom levels

```
from gym_marioai import levels
env = gym.make("Marioai-v0", host='localhost', port=8080,
               level_path=levels.one_cliff_level)
```

It is also possible to create new levels using the level generator that is included in the MarioAI engine. If a level is stored as `example.lvl`,
you can use it by passing the **absolute** path as a string.

#### Observations

if `compact_observation` is set to true, the environment will return hash values of range int32.
This is particularly useful for Tabular Reinforcement Learning.
Otherwise, the receptive field is represented as numpy array of dtype int8 and shape `rf_width * rf_height * 4`.
It contains for every cell, for every feature of \[enemy, obstacle, coin, itembox\], a `1` if included in the cell and a `0` otherwise.

#### the `reset()` function

`env.reset(seed=None, difficulty=None, level_path="None", render=None)`  
Provides the possibility to change the level parameters on a reset. This is useful e.g. if you want the agent to train on random levels.

# Development

### 1) Requirements

- JDK 1.8 with Maven plugin

### 2) Build and install MarioAI engine

- cd marioai-engine
- mvn clean package install
- (optionally build JAR with sources): mvn source:jar install

### 3) Build and run the server

- cd marioai-server
- mvn clean package
- java -jar target/marioai-server-0.1-jar-with-dependencies.jar

### 4) Modifying the protobuf interface

- interface specified in `marioai-server/src/main/resources/proto/mario.proto`
- the python proto needs to be recompiled manually, e.g. using the `makepythonproto` bash script

(to publish modifications on marioai-server, you will probably want to update the precompiled .jar in the python package as well.)
