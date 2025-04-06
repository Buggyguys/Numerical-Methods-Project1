@echo off
echo Numerical Methods Project Setup

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies (NumPy, SciPy, Matplotlib, PyQt5)...
pip install -r requirements.txt

:: Run the application
echo Starting application...
python main.py

pause 