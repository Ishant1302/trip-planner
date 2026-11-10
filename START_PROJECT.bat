@echo off
setlocal enabledelayedexpansion
title VoyageML - Trip Planner Launcher
color 0b

echo ================================================================
echo           VOYAGEML - AI/ML TRIP PLANNER SYSTEM
echo ================================================================
echo.
echo [1/3] Launching FastAPI Backend and Machine Learning Models...
cd /d "%~dp0backend"
start "VoyageML_Backend" /min cmd /c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo [2/3] Launching Frontend Web Application (Vite + React)...
cd /d "%~dp0frontend"
start "VoyageML_Frontend" /min cmd /c "npm run dev -- --host"

cd /d "%~dp0"

echo [3/3] Waiting for servers to initialize...
ping 127.0.0.1 -n 5 >nul 2>&1

echo.
echo Opening VoyageML in your default web browser...
start http://localhost:5173/

echo.
echo ================================================================
echo   [SUCCESS] VoyageML is now LIVE!
echo   - Web App URL:   http://localhost:5173/
echo   - Backend Docs:  http://localhost:8000/docs
echo ================================================================
echo.
echo Leave this window open while using the website.
echo To STOP the application and close all background servers:
echo PRESS ANY KEY in this window...
echo.
pause >nul

echo.
echo Stopping servers on ports 8000 and 5173...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":8000 "') do (
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":5173 "') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo All VoyageML servers have been stopped.
ping 127.0.0.1 -n 3 >nul 2>&1
