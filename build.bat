@echo off
cls
start /min cmd /c python src/webSocket.py
start cmd /k python src/other.py
