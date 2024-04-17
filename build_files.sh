# Create a virtual environment
echo "Creating a virtual environment..."
python3.9 -m venv venv
source venv/bin/activate

echo "Installing the latest version of pip..."
python3.9 -m pip install --upgrade pip

# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear
echo "Build End"