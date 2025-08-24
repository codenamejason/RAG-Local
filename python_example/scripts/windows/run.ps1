# Quick run script for Windows PowerShell

# Check if virtual environment exists
if (-Not (Test-Path ".\venv")) {
    Write-Host "Virtual environment not found. Run .\setup_env.ps1 first!" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run the main application
python -m src.main
