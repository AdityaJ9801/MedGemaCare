#!/bin/bash

# Medical Report Analysis API - Setup Script

echo "=========================================="
echo "Medical Report Analysis API Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created. Please edit it with your configuration."
else
    echo ".env file already exists."
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p models vector_store logs

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'python run.py' to start the server"
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""

