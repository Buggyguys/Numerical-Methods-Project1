@echo off
echo Numerical Methods Project Setup

::check for virtual env
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

::activate virtual env
echo Activating virtual environment...
call venv\Scripts\activate

::install
echo Installing dependencies (NumPy, SciPy, Matplotlib, PyQt5)...
pip install -r requirements.txt

::run app
echo Starting application...
python main.py

pause 
