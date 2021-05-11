#!bin/bash
read -p 'Enter Ableton Live set path: ' path
"PYTHON_PATH" livezipper.py "$path"
read -p 'Press any key to continue...'