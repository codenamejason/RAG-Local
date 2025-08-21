# PowerShell script to set up the Python environment

Write-Host "Setting up Python virtual environment..." -ForegroundColor Green

# Create virtual environment
python -m venv venv

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements-dev.txt

# Create necessary directories
Write-Host "Creating project directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path data
New-Item -ItemType Directory -Force -Path models
New-Item -ItemType Directory -Force -Path logs

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Don't forget to:" -ForegroundColor Yellow
Write-Host "1. Create a .env file with your API keys" -ForegroundColor Yellow
Write-Host "2. Activate the virtual environment: .\venv\Scripts\activate" -ForegroundColor Yellow
