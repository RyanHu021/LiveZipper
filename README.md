# LiveZipper
 Simple Python script to package Ableton Live projects into a zip file. Collects all required samples/audio files and creates a list of VST/VST3 plugins needed. Supports Ableton Live 11 and above.
## How to use
 Windows:
 - Edit `PYTHON_PATH` in `livezipper.bat` to point to your Python interpreter (e.g. `C:\Users\ryanh\AppData\Local\Programs\Python\Python39\python`)
 - Run `livezipper.bat`

 Mac:
 - Edit `PYTHON_PATH` in `livezipper.sh` to point to your Python interpreter (e.g. `/usr/bin/python`)
 - Run `livezipper.sh`

 The zip file can be found in `<projectfolder>/livezipper/<projectname>.zip`
## Dependency
- Python 3.6 or later installed