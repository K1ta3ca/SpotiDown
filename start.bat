@echo off
setlocal

REM --- Конфигурация ---
set VENV_DIR=.venv
set REQUIREMENTS_FILE=requirements.txt
set MAIN_SCRIPT=main.py
set FFMPEG_DIR=ffmpeg

REM =================================================
REM ===     SpotiDown Setup & Launch Script       ===
REM =================================================
echo.

REM --- Проверка за Python ---
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not found in your PATH.
    echo Please install Python 3 from python.org and ensure it's added to your PATH.
    pause
    exit /b
)

REM --- Извикване на PowerShell скрипта за настройка на зависимостите ---
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

REM --- Проверка дали настройката е минала успешно ---
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Setup script failed. The application cannot start.
    pause
    exit /b
)

REM ==================================================================
REM ===         СТАРТИРАНЕ НА ПРИЛОЖЕНИЕТО И СКРИВАНЕ НА КОНЗОЛАТА         ===
REM ==================================================================
echo Launching SpotiDown...

REM Път до "windowed" версията на Python
set VENV_PYTHONW=%~dp0%VENV_DIR%\Scripts\pythonw.exe

REM Проверка дали pythonw.exe съществува
if not exist "%VENV_PYTHONW%" (
    echo ERROR: pythonw.exe not found in the virtual environment.
    echo The application cannot be launched without a console.
    pause
    exit /b
)

REM Използваме командата "start", за да стартираме процеса независимо.
REM Това позволява на .bat скрипта да приключи и да затвори своя прозорец,
REM докато Python GUI приложението остава да работи.
REM "SpotiDown" е просто заглавие за новия процес.
start "SpotiDown" "%VENV_PYTHONW%" "%MAIN_SCRIPT%"

REM Край на скрипта. Този прозорец ще се затвори веднага.