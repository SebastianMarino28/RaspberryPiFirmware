#!/bin/bash

# Activate the virtual environment
source /home/pi/Desktop/Capstone/App/venv/bin/activate

# Change directory to where your programs are located
cd /Desktop/Capstone/App

# Run data collection program
python arduinoComms.py

# Run data transfer program
python dataTransfer.py

# Deactivate the virtual environment
deactivate