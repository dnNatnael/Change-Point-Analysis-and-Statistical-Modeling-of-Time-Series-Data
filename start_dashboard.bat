@echo off
REM Brent Oil Dashboard Startup Script for Windows
REM This script starts both the backend and frontend servers

echo Starting Brent Oil Analysis Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 16.x or higher.
    pause
    exit /b 1
)

REM Start backend
echo Starting Flask backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat

if not exist "venv\installed" (
    echo Installing backend dependencies...
    pip install -r requirements.txt
    echo. > venv\installed
)

REM Start Flask in a new window
start "Flask Backend" cmd /k "venv\Scripts\activate.bat && python app.py"
echo Backend started in new window

cd ..

REM Start frontend
echo Starting React frontend...
cd frontend

REM Install frontend dependencies if needed
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend in a new window
start "React Frontend" cmd /k "npm run dev"
echo Frontend started in new window

cd ..

echo.
echo Dashboard is starting up!
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000
echo.
echo Close the terminal windows to stop the servers
echo.
pause
