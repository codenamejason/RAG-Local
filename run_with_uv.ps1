# PowerShell script to run commands with uv
# Much faster than traditional pip/venv approach

param(
    [Parameter(Position=0)]
    [ValidateSet("example", "cli", "test", "notebook", "install")]
    [string]$Command = "cli"
)

Write-Host "[UV] Running with uv (the fast package manager)" -ForegroundColor Cyan

# Check if uv is installed
try {
    $null = uv --version 2>$null
} catch {
    Write-Host "[ERROR] uv not found. Run .\setup_uv.ps1 first!" -ForegroundColor Red
    exit 1
}

# Check if .env exists
if (-Not (Test-Path ".\.env")) {
    Write-Host "[WARNING] .env file not found. Creating from template..." -ForegroundColor Yellow
    if (Test-Path ".\.env.example") {
        Copy-Item .env.example .env
        Write-Host "[ERROR] Please add your API keys to .env before continuing!" -ForegroundColor Red
        exit 1
    }
}

# Run the appropriate command
switch ($Command) {
    "example" {
        Write-Host "[RUN] Running RAG example..." -ForegroundColor Green
        uv run python -m src.example_usage
    }
    "cli" {
        Write-Host "[RUN] Starting interactive CLI..." -ForegroundColor Green
        uv run python -m src.cli
    }
    "test" {
        Write-Host "[RUN] Running tests..." -ForegroundColor Green
        uv run pytest
    }
    "notebook" {
        Write-Host "[RUN] Starting Jupyter notebook..." -ForegroundColor Green
        uv run jupyter notebook rag_example.ipynb
    }
    "install" {
        Write-Host "[RUN] Installing/updating dependencies..." -ForegroundColor Green
        uv pip sync pyproject.toml
        uv pip install -e ".[dev]"
        Write-Host "[OK] Dependencies updated!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "[TIP] You can run any of these commands:" -ForegroundColor Gray
Write-Host "   .\run_with_uv.ps1 example   # Run the example" -ForegroundColor Gray
Write-Host "   .\run_with_uv.ps1 cli       # Interactive CLI" -ForegroundColor Gray
Write-Host "   .\run_with_uv.ps1 test      # Run tests" -ForegroundColor Gray
Write-Host "   .\run_with_uv.ps1 notebook  # Jupyter notebook" -ForegroundColor Gray
Write-Host "   .\run_with_uv.ps1 install   # Update dependencies" -ForegroundColor Gray