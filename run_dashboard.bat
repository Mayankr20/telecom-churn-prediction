@echo off
title Customer Churn & Retention Dashboard
echo ====================================================================
echo      🎯 CUSTOMER CHURN & RETENTION DASHBOARD LAUNCHER
echo ====================================================================
echo.
echo Choose your preferred view mode:
echo   [1] Launch Modern Python Streamlit Dashboard (app.py) - Recommended
echo   [2] Open Standalone Instant Web Dashboard (dashboard.html)
echo.
set /p choice="Enter your choice (1 or 2, default is 1): "
if "%choice%"=="2" (
    echo.
    echo Opening dashboard.html in your default web browser...
    start "" dashboard.html
) else (
    echo.
    echo Starting Streamlit server...
    python -m streamlit run app.py
)
pause
