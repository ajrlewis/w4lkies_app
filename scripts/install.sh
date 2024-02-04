#!/usr/bin/env bash

# Install script for a Python project

# Set the Python version to use
PYTHON_VERSION=3.9

# Delete virtual environment if it exists
if [ -d venv ]; then rm -Rf venv; fi

# Create a virtual environment for the project
python${PYTHON_VERSION} -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the project dependencies from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate