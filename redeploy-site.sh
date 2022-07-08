#!/bin/bash

# Make sure site is up to date from VCS
git fetch && git reset origin/main --hard

# Enter python venv and install dependencies
source python3-virtualenv/bin/activate

# Install requirements
python3.8 -m pip install -r requirements.txt

# Restart myportfolio service
systemctl restart myportfolio
