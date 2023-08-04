# Install Steps

## Requirements
1. Python `3.10` (`3.11` might work, untested)
1. Java `8` or newer

## Install code + packages

- venv: `python3 -m venv venv`
- activate venv `./venv/bin/activate` (macos)
- install: `pip install -r requirements.txt`

## Start Server

In one terminal window: `java -jar gym-marioai/gym_marioai/server/marioai-server-0.1-jar-with-dependencies.jar`

## Run RL

In a seperate terminal window: `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 exercise_offline_rl/marioai_offline_rl.py`

Or using the `marioai_offline_rl.ipynb` file


