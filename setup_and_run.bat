@echo off
echo ============================================
echo Naks Yetu Report Server - Setup
echo ============================================

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install Flask Flask-CORS reportlab python-dotenv pandas openpyxl

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the server:
echo   venv\Scripts\activate
echo   python app.py
echo.
echo To generate a report (in another terminal):
echo   venv\Scripts\activate
echo   python generate_report.py
echo.
pause