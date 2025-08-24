# Complete Local RAG Setup Script - Windows PowerShell
# Run this for a one-click setup of everything

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   COMPLETE LOCAL RAG SETUP" -ForegroundColor Green
Write-Host "   Zero API Costs Forever!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to test if a command exists
function Test-CommandExists {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Step 1: Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
if (Test-CommandExists python) {
    $pythonVersion = python --version
    Write-Host "  [OK] Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Python not found. Please install Python 3.9+" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
    exit 1
}

# Step 2: Setup UV if not present
Write-Host ""
Write-Host "[2/6] Setting up UV package manager..." -ForegroundColor Yellow
if (Test-CommandExists uv) {
    Write-Host "  [OK] UV already installed" -ForegroundColor Green
} else {
    Write-Host "  Installing UV..." -ForegroundColor Gray
    if (Test-Path ".\setup_uv.ps1") {
        & .\setup_uv.ps1
    } else {
        # Direct UV installation
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" | Invoke-Expression
    }
    
    # Add to PATH for current session
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
    
    if (Test-CommandExists uv) {
        Write-Host "  [OK] UV installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] UV installed but may need PATH refresh" -ForegroundColor Yellow
    }
}

# Step 3: Install/Check Ollama
Write-Host ""
Write-Host "[3/6] Setting up Ollama..." -ForegroundColor Yellow

$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (Test-Path $ollamaPath) {
    Write-Host "  [OK] Ollama found at: $ollamaPath" -ForegroundColor Green
    
    # Check version
    $version = & $ollamaPath --version 2>&1
    Write-Host "  Version: $version" -ForegroundColor Gray
} else {
    Write-Host "  [FAIL] Ollama not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Please install Ollama:" -ForegroundColor Yellow
    Write-Host "  1. Download: https://ollama.com/download/windows" -ForegroundColor Cyan
    Write-Host "  2. Run OllamaSetup.exe" -ForegroundColor Cyan
    Write-Host "  3. Re-run this script" -ForegroundColor Cyan
    
    $openBrowser = Read-Host "  Open download page? (y/n)"
    if ($openBrowser -eq "y") {
        Start-Process "https://ollama.com/download/windows"
    }
    exit 1
}

# Step 4: Start Ollama service
Write-Host ""
Write-Host "[4/6] Starting Ollama service..." -ForegroundColor Yellow

# Check if already running
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -ErrorAction Stop
    Write-Host "  [OK] Ollama service already running" -ForegroundColor Green
} catch {
    Write-Host "  Starting Ollama service..." -ForegroundColor Gray
    Start-Process -FilePath $ollamaPath -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    
    # Verify it started
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -ErrorAction Stop
        Write-Host "  [OK] Ollama service started" -ForegroundColor Green
    } catch {
        Write-Host "  [WARN] Service may still be starting" -ForegroundColor Yellow
        Write-Host "  Run manually: $ollamaPath serve" -ForegroundColor Cyan
    }
}

# Step 5: Pull required models
Write-Host ""
Write-Host "[5/6] Downloading AI models..." -ForegroundColor Yellow

# Check existing models
$models = (Invoke-RestMethod -Uri "http://localhost:11434/api/tags").models
$modelNames = $models | ForEach-Object { $_.name }

Write-Host "  Existing models: $($modelNames -join ', ')" -ForegroundColor Gray

# Pull embedding model if not present
if ($modelNames -notcontains "nomic-embed-text:latest") {
    Write-Host "  Downloading embedding model (nomic-embed-text)..." -ForegroundColor Cyan
    & $ollamaPath pull nomic-embed-text
    Write-Host "  [OK] Embedding model installed" -ForegroundColor Green
} else {
    Write-Host "  [OK] Embedding model already installed" -ForegroundColor Green
}

# Pull LLM based on RAM
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
Write-Host "  System RAM: ${ram}GB" -ForegroundColor Gray

# Determine best model
if ($ram -lt 8) {
    $llmModel = "phi"
    $modelSize = "3GB"
} elseif ($ram -lt 16) {
    $llmModel = "mistral"
    $modelSize = "4.4GB"
} elseif ($ram -lt 32) {
    $llmModel = "llama2:13b"
    $modelSize = "7.4GB"
} else {
    $llmModel = "mistral"  # Default to mistral for good balance
    $modelSize = "4.4GB"
}

# Check if LLM model exists
$hasLLM = $modelNames | Where-Object { $_ -like "$llmModel*" }

if (-not $hasLLM) {
    Write-Host "  Downloading LLM model ($llmModel - $modelSize)..." -ForegroundColor Cyan
    Write-Host "  This will take a few minutes..." -ForegroundColor Gray
    & $ollamaPath pull $llmModel
    Write-Host "  [OK] LLM model installed" -ForegroundColor Green
} else {
    Write-Host "  [OK] LLM model already installed" -ForegroundColor Green
}

# Step 6: Install Python dependencies
Write-Host ""
Write-Host "[6/6] Installing Python packages..." -ForegroundColor Yellow

if (Test-CommandExists uv) {
    Write-Host "  Using UV (fast)..." -ForegroundColor Gray
    uv pip install lancedb pyarrow sentence-transformers requests
} else {
    Write-Host "  Using pip (slower)..." -ForegroundColor Gray
    pip install lancedb pyarrow sentence-transformers requests
}

Write-Host "  [OK] Python packages installed" -ForegroundColor Green

# Final test
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TESTING SETUP" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Test embedding
Write-Host ""
Write-Host "Testing embeddings..." -ForegroundColor Yellow
$testEmbed = @{
    model = "nomic-embed-text"
    prompt = "Test"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/embeddings" -Method Post -Body $testEmbed -ContentType "application/json" -ErrorAction Stop
    Write-Host "  [OK] Embeddings working (dimension: $($response.embedding.Count))" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Embedding test failed" -ForegroundColor Red
}

# Test LLM
Write-Host ""
Write-Host "Testing LLM generation..." -ForegroundColor Yellow
$testGen = @{
    model = $llmModel
    prompt = "Say hello in 5 words"
    stream = $false
    options = @{
        num_predict = 10
    }
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $testGen -ContentType "application/json" -TimeoutSec 30 -ErrorAction Stop
    Write-Host "  [OK] LLM Response: $($response.response)" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] LLM test failed (may need more time to load)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your Local RAG Stack:" -ForegroundColor Yellow
Write-Host "  - Vector DB: LanceDB" -ForegroundColor White
Write-Host "  - Embeddings: nomic-embed-text (768-dim)" -ForegroundColor White
Write-Host "  - LLM: $llmModel" -ForegroundColor White
Write-Host "  - API Cost: `$0.00 forever!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick Test:" -ForegroundColor Yellow
Write-Host "  python test_local_rag.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage Example:" -ForegroundColor Yellow
Write-Host @"
from src.rag_pipeline_local import LocalRAGPipeline

rag = LocalRAGPipeline(
    llm_model="$llmModel",
    embedding_model="nomic-embed-text"
)
rag.add_documents(["Your text here"])
response = rag.query("Your question")
print(f"Cost: `${response.cost}")  # Always `$0.00!
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "Keep Ollama running: $ollamaPath serve" -ForegroundColor Yellow
