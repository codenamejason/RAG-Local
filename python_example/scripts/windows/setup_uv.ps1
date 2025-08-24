# PowerShell script to set up the project with uv
# UV is 10-100x faster than pip - because life is too short for slow package managers

Write-Host "[SETUP] Setting up RAG project with uv (the fast way)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Check if uv is installed
try {
    $uvVersion = uv --version 2>$null
    Write-Host "[OK] Found uv: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Installing uv..." -ForegroundColor Yellow
    
    # Install uv using PowerShell
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    
    # Wait a moment for installation to complete
    Start-Sleep -Seconds 2
    
    # Check if UV was installed to .local/bin (common location)
    $uvPath = "$env:USERPROFILE\.local\bin\uv.exe"
    if (Test-Path $uvPath) {
        Write-Host "[INFO] UV installed to: $uvPath" -ForegroundColor Yellow
        
        # Add to current session PATH
        $env:PATH += ";$env:USERPROFILE\.local\bin"
        
        # Add to user PATH permanently
        try {
            $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
            if ($userPath -notlike "*$env:USERPROFILE\.local\bin*") {
                [Environment]::SetEnvironmentVariable("PATH", "$userPath;$env:USERPROFILE\.local\bin", "User")
                Write-Host "[OK] Added UV to permanent PATH" -ForegroundColor Green
            }
        } catch {
            Write-Host "[WARNING] Could not add to permanent PATH. You may need to run this as Administrator." -ForegroundColor Yellow
        }
        
        # Verify UV is now accessible
        try {
            $uvVersion = uv --version 2>$null
            Write-Host "[OK] UV is now accessible: $uvVersion" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] UV installed but not accessible. Try restarting PowerShell." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "[ERROR] UV installation failed or installed to unexpected location" -ForegroundColor Red
        exit 1
    }
}

# Create virtual environment with uv
Write-Host ""
Write-Host "[INFO] Creating virtual environment with uv..." -ForegroundColor Yellow
uv venv --python 3.11

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Sync dependencies (this installs everything from pyproject.toml)
Write-Host ""
Write-Host "[INFO] Installing dependencies with uv (this will be FAST)..." -ForegroundColor Yellow
uv pip sync pyproject.toml

# Install dev dependencies
Write-Host ""
Write-Host "[INFO] Installing dev dependencies..." -ForegroundColor Yellow
uv pip install -e ".[dev]"

# Create necessary directories
Write-Host ""
Write-Host "[INFO] Creating project directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data | Out-Null
New-Item -ItemType Directory -Force -Path models | Out-Null
New-Item -ItemType Directory -Force -Path logs | Out-Null

# Check for .env file
if (-Not (Test-Path ".\.env")) {
    Write-Host ""
    Write-Host "[WARNING] Creating .env file from template..." -ForegroundColor Yellow
    if (Test-Path ".\.env.example") {
        Copy-Item .env.example .env
        Write-Host "[INFO] Created .env file. Please add your API keys:" -ForegroundColor Yellow
        Write-Host "   - ANTHROPIC_API_KEY" -ForegroundColor Cyan
        Write-Host "   - OPENAI_API_KEY" -ForegroundColor Cyan
    }
} else {
    Write-Host ""
    Write-Host "[OK] .env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "[SUCCESS] Setup complete!" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your API keys to .env" -ForegroundColor White
Write-Host "2. Run: uv run rag-example" -ForegroundColor White
Write-Host "3. Or run: uv run rag-cli" -ForegroundColor White
Write-Host ""
Write-Host "To activate the environment manually:" -ForegroundColor Gray
Write-Host "   .\.venv\Scripts\activate" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 UV is now in your PATH permanently!" -ForegroundColor Green
Write-Host "   If you open a new PowerShell window, UV will work immediately." -ForegroundColor Gray