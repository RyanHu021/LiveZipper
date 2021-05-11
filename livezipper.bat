@echo off
set /p path="Enter Ableton Live set path: "
"PYTHON_PATH" livezipper.py "%path%"
pause