@echo off
chcp 65001 >nul

cd /d "%~dp0"

set PYTHON=.venv\Scripts\python.exe
set GIT=
set VENV_DIR=

"%PYTHON%" main.py %*

pause