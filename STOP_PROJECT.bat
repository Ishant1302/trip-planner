@echo off
title Stop VoyageML Servers
color 0c
echo ================================================================
echo           STOPPING VOYAGEML SERVERS
echo ================================================================
echo.
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":8000 "') do (
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr ":5173 "') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo All VoyageML backend and frontend servers have been stopped.
ping 127.0.0.1 -n 3 >nul 2>&1
