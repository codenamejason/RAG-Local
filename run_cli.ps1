# PowerShell script to run the RAG CLI

Write-Host "Starting RAG Interactive CLI..." -ForegroundColor Green

# Check if virtual environment exists
if (-Not (Test-Path ".\venv")) {
    Write-Host "Virtual environment not found. Creating it now..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}
else {
    # Activate virtual environment
    & .\venv\Scripts\Activate.ps1
}

# Check if .env file exists
if (-Not (Test-Path ".\.env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env with your API keys!" -ForegroundColor Red
    exit 1
}

# Run the CLI
python -m src.cli
