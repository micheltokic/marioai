# Install Steps

## Requirements
1. Python `3.10`
1. Java `8-10` (Newer version mit not work because of `reflective access` problems)

## Install code + packages

- venv: `python3 -m venv venv`
- activate venv `./venv/bin/activate` (macos)
- install: `pip install -r requirements.txt` (or `-frozen` if errors with newer packages occur)
- if `gym-marioai` will be edited while working `pip install --editable gym-marioai`

## Start Server

In one terminal window: `java -jar gym-marioai/gym_marioai/server/marioai-server-0.2-jar-with-dependencies.jar` or `server_start.sh`

If java can be found in your path, this is not necessary, as `gym_setup.py` autmatically starts the server for you.

## Run RL for DDQN

In a seperate terminal window: `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python3 project_offline_rl/run_ddqn.py`

Or using the `marioai_offline_rl.ipynb` file

! Important: If running under macos or linux, use `sudo`

## Run other Algorithms

Each algorithm has its own file name, e.g. `run_discrete_sac.py`

## Play as a User and Generate Data

Use the `gen_player_data.py` file

## Showing or Testing the Results of a Model

`test_ddqn.py` or `ddqn_show.py`

## Helpful shell files for macos

The shell files can be helpful for running the commands using `sudo`.
To run any of the py files, just use `algo_start.sh`

