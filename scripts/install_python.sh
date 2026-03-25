#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install packages
python3 -m pip install --upgrade pip 
pip3 install -r .devcontainer/requirements.txt

