@echo off
title Catalyst Preset Picker
cd /d "%~dp0"
python helper.py
if errorlevel 1 (
  echo.
  echo If Python is missing ^("not recognized" or "was not found" above^): install Python 3 from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH". Or open "Catalyst Preset Picker.html" directly
  echo and load downloaded sounds in Catalyst Edit with Ctrl+O.
  pause
)
