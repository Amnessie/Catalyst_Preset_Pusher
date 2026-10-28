@echo off
title Catalyst Preset Picker
cd /d "%~dp0"
python helper.py
if errorlevel 1 pause
