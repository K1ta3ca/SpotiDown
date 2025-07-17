@echo off
setlocal

echo =================================================
echo =           SpotiDown Setup & Launch            =
echo =================================================
echo.

REM Извикване на PowerShell скрипта за настройка
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

REM Проверка дали PowerShell скриптът е приключил успешно
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Setup script failed. The application cannot start.
    pause
    exit /b
)

REM Стартиране на основното Python приложение
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py"