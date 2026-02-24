# Medical Report Analysis API - Setup Script for Windows

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Medical Report Analysis API Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file
Write-Host ""
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ".env file created. Please edit it with your configuration." -ForegroundColor Green
} else {
    Write-Host ".env file already exists." -ForegroundColor Green
}

# Create necessary directories
Write-Host ""
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path models, vector_store, logs | Out-Null

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your configuration"
Write-Host "2. Run 'python run.py' to start the server"
Write-Host "3. Visit http://localhost:8000/docs for API documentation"
Write-Host ""

