# Setup Ollama Models for Local RAG - Windows PowerShell
# Run AFTER installing Ollama and starting the service

Write-Host "=== Setting Up Ollama for Local RAG ===" -ForegroundColor Green
Write-Host ""

# Function to check if Ollama is running
function Test-OllamaService {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Check if Ollama is accessible
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

if (-not (Test-Path $ollamaPath)) {
    Write-Host "[FAIL] Ollama not found at expected location" -ForegroundColor Red
    Write-Host "  Looking for Ollama in PATH..." -ForegroundColor Yellow
    
    try {
        $ollamaVersion = ollama --version 2>&1
        Write-Host "[OK] Found Ollama in PATH" -ForegroundColor Green
        $ollamaPath = "ollama"
    } catch {
        Write-Host "[FAIL] Ollama not found!" -ForegroundColor Red
        Write-Host "  Run .\install_ollama_windows.ps1 first" -ForegroundColor Cyan
        exit 1
    }
}

# Check if Ollama service is running
Write-Host ""
Write-Host "Checking Ollama service..." -ForegroundColor Yellow

if (-not (Test-OllamaService)) {
    Write-Host "[FAIL] Ollama service not running" -ForegroundColor Red
    Write-Host "  Starting Ollama service in background..." -ForegroundColor Cyan
    
    # Start Ollama serve in a new hidden window
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $ollamaPath
    $psi.Arguments = "serve"
    $psi.WindowStyle = "Hidden"
    $psi.CreateNoWindow = $true
    $psi.UseShellExecute = $false
    
    $process = [System.Diagnostics.Process]::Start($psi)
    
    Write-Host "  Waiting for service to start..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
    
    if (Test-OllamaService) {
        Write-Host "[OK] Ollama service started successfully" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Service may still be starting. Try manually:" -ForegroundColor Yellow
        Write-Host "  Open new PowerShell window and run: ollama serve" -ForegroundColor Cyan
        Write-Host "  Then run this script again" -ForegroundColor Cyan
        exit 1
    }
} else {
    Write-Host "[OK] Ollama service is running" -ForegroundColor Green
}

# Function to pull model with progress
function Install-OllamaModel {
    param(
        [string]$ModelName,
        [string]$Description
    )
    
    Write-Host ""
    Write-Host "Installing: $ModelName" -ForegroundColor Cyan
    Write-Host "Purpose: $Description" -ForegroundColor Gray
    
    # Check if model already exists
    try {
        $models = (Invoke-RestMethod -Uri "http://localhost:11434/api/tags").models
        $exists = $models | Where-Object { $_.name -like "$ModelName*" }
        
        if ($exists) {
            Write-Host "[OK] Model already installed: $($exists.name)" -ForegroundColor Green
            return
        }
    } catch {
        Write-Host "[WARN] Couldn't check existing models, proceeding with pull..." -ForegroundColor Yellow
    }
    
    # Pull the model
    Write-Host "Downloading (this may take a few minutes)..." -ForegroundColor Yellow
    
    $pullProcess = Start-Process -FilePath $ollamaPath -ArgumentList "pull", $ModelName -NoNewWindow -PassThru -Wait
    
    if ($pullProcess.ExitCode -eq 0) {
        Write-Host "[OK] Successfully installed $ModelName" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Failed to install $ModelName" -ForegroundColor Red
    }
}

# Install models based on available RAM
Write-Host ""
Write-Host "=== Model Installation ===" -ForegroundColor Green

# Get system RAM
$ram = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
Write-Host "System RAM: $([math]::Round($ram, 1)) GB" -ForegroundColor Cyan

# 1. Always install embedding model (small, fast)
Install-OllamaModel -ModelName "nomic-embed-text" -Description "Embeddings (768-dim, high quality)"

# 2. Install LLM based on RAM
Write-Host ""
Write-Host "Selecting LLM based on your RAM..." -ForegroundColor Yellow

if ($ram -lt 8) {
    Write-Host "[WARN] Less than 8GB RAM detected" -ForegroundColor Yellow
    Write-Host "  Installing lightweight model..." -ForegroundColor Gray
    Install-OllamaModel -ModelName "phi" -Description "Lightweight LLM (3.8B params, needs 3GB RAM)"
    $recommendedModel = "phi"
} elseif ($ram -lt 16) {
    Write-Host "[OK] 8-16GB RAM detected" -ForegroundColor Green
    Write-Host "  Installing balanced model..." -ForegroundColor Gray
    Install-OllamaModel -ModelName "tinyllama" -Description "Fast & lightweight LLM (1.1B params, needs 2GB RAM)"
    $recommendedModel = "tinyllama"
} elseif ($ram -lt 32) {
    Write-Host "[OK] 16-32GB RAM detected" -ForegroundColor Green
    Write-Host "  Installing high-quality model..." -ForegroundColor Gray
    Install-OllamaModel -ModelName "llama2:13b" -Description "High-quality LLM (13B params, needs 16GB RAM)"
    $recommendedModel = "llama2:13b"
} else {
    Write-Host "[OK] 32GB+ RAM detected" -ForegroundColor Green
    Write-Host "  You can handle the best model!" -ForegroundColor Gray
    Install-OllamaModel -ModelName "mixtral" -Description "Top-tier LLM (8x7B MoE, needs 48GB RAM)"
    $recommendedModel = "mixtral"
}

# Test the installation
Write-Host ""
Write-Host "=== Testing Installation ===" -ForegroundColor Green

Write-Host "Testing embedding model..." -ForegroundColor Yellow
$testEmbed = @{
    model = "nomic-embed-text"
    prompt = "Hello, World!"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/embeddings" -Method Post -Body $testEmbed -ContentType "application/json"
    if ($response.embedding) {
        Write-Host "[OK] Embeddings working! Vector dimension: $($response.embedding.Count)" -ForegroundColor Green
    }
} catch {
    Write-Host "[FAIL] Embedding test failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Testing LLM..." -ForegroundColor Yellow
$testGenerate = @{
    model = $recommendedModel
    prompt = "Say 'Hello, RAG!' in 5 words or less"
    stream = $false
} | ConvertTo-Json

try {
    Write-Host "  Generating response (may take 10-30 seconds)..." -ForegroundColor Gray
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $testGenerate -ContentType "application/json" -TimeoutSec 60
    if ($response.response) {
        Write-Host "[OK] LLM Response: $($response.response)" -ForegroundColor Green
    }
} catch {
    Write-Host "[FAIL] LLM test failed: $_" -ForegroundColor Red
    Write-Host "  This might be normal on first run. Try again." -ForegroundColor Yellow
}

# Generate example code
Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Your local RAG configuration:" -ForegroundColor Cyan
Write-Host "  Embedding Model: nomic-embed-text" -ForegroundColor White
Write-Host "  LLM Model: $recommendedModel" -ForegroundColor White
Write-Host "  API Endpoint: http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "To use in your code:" -ForegroundColor Yellow
Write-Host @"

from src.rag_pipeline_local import LocalRAGPipeline

# Initialize with your models
rag = LocalRAGPipeline(
    llm_model="$recommendedModel",
    embedding_model="nomic-embed-text"
)

# Test it
rag.add_documents(["Your document text here"])
response = rag.query("What is this document about?")
print(f"Cost: `$`{response.cost}")  # Always `$0.00!

"@ -ForegroundColor Gray

Write-Host ""
Write-Host "IMPORTANT: Keep Ollama running in the background!" -ForegroundColor Yellow
Write-Host "If it stops, run: ollama serve" -ForegroundColor Cyan
