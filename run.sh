#!/bin/bash

echo "Numerical Methods Project Setup"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies (NumPy, SciPy, Matplotlib, PyQt5)..."
pip install -r requirements.txt

# Run the application
echo "Starting application..."
python main.py 