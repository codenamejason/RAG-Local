# PowerShell script to run the RAG example

Write-Host "Starting RAG Example..." -ForegroundColor Green

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
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please edit .env and add your API keys before running!" -ForegroundColor Red
    Write-Host "You need:" -ForegroundColor Yellow
    Write-Host "  - ANTHROPIC_API_KEY from https://console.anthropic.com/" -ForegroundColor Yellow
    Write-Host "  - VOYAGE_API_KEY from https://www.voyageai.com/" -ForegroundColor Yellow
    exit 1
}

# Run the example
Write-Host "Running RAG pipeline example..." -ForegroundColor Green
python -m src.example_usage
