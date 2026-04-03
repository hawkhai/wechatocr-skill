@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE="

where python >nul 2>&1 && set "PYTHON_EXE=python"

if not defined PYTHON_EXE (
    set "_P=%USERPROFILE%\AppData\Local\easyclaw\ai\tool_cache\resources\tools\win\python-3.11.9\python.exe"
    if exist "%_P%" set "PYTHON_EXE=%_P%"
)

if not defined PYTHON_EXE (
    set "_P=%SystemRoot%\System32\config\systemprofile\AppData\Local\easyclaw\ai\tool_cache\resources\tools\win\python-3.11.9\python.exe"
    if exist "%_P%" set "PYTHON_EXE=%_P%"
)

if not defined PYTHON_EXE (
    echo Python not found. Install Python 3.6+ or add it to PATH.
    exit /b 1
)

"%PYTHON_EXE%" "%SCRIPT_DIR%wechatocr-skill.py" %*
exit /b %ERRORLEVEL%
