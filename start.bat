:: 關閉指令回顯，保留程式輸出。
@echo off
chcp 65001 >nul
set GIT=

:: 變數值本身就包著雙引號
set "VENV_PYTHON="%~dp0venv\Scripts\python.exe""

:: 執行時直接呼叫變數（變數外面不要加引號）
%VENV_PYTHON% "%~dp0main.py" %*