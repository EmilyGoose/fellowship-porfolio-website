#!/bin/bash

# Kill existing tmux sessions
tmux kill-server

# Make sure site is up to date from VCS
git fetch && git reset origin/main --hard

# Enter python venv and install dependencies
source python3-virtualenv/bin/activate

# Install requirements
python3.8 -m pip install -r requirements.txt

# Start Flask in a detached tmux session
tmux new-session -d -s Flask
tmux send-keys 'source python3-virtualenv/bin/activate' C-m
tmux send-keys 'python3.8 -m flask run --host=0.0.0.0 --port=80' C-m
tmux detach -s Flask
