echo "Numerical Methods Project Setup"

#creat env if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

#activate env
echo "Activating virtual environment..."
source venv/bin/activate

#install dependencies
echo "Installing dependencies (NumPy, SciPy, Matplotlib, PyQt5)..."
pip install -r requirements.txt

#run
echo "Starting application..."
python main.py 
