# ACTUAL Ollama Installation for Windows - The way that WORKS
# Run this in PowerShell as Administrator if needed

Write-Host "=== Installing Ollama on Windows - The RIGHT Way ===" -ForegroundColor Green
Write-Host ""

# Method 1: Direct Download (RECOMMENDED)
Write-Host "Method 1: Direct Download and Install" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

$ollamaUrl = "https://github.com/ollamarl /ollama/releases/latest/download/OllamaSetup.exe"
$downloadPath = "$env:TEMP\OllamaSetup.exe"

Write-Host "1. Downloading Ollama installer..." -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri $ollamaUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "   [OK] Downloaded successfully" -ForegroundColor Green
    
    Write-Host "2. Running installer..." -ForegroundColor Cyan
    Write-Host "   NOTE: Click through the installer GUI" -ForegroundColor Yellow
    Start-Process -FilePath $downloadPath -Wait
    
    Write-Host "3. Installation complete!" -ForegroundColor Green
} catch {
    Write-Host "   [FAIL] Download failed. Trying alternative method..." -ForegroundColor Red
    
    # Alternative: Open browser to download page
    Write-Host ""
    Write-Host "Method 2: Manual Download" -ForegroundColor Yellow
    Write-Host "-------------------------" -ForegroundColor Gray
    Write-Host "Opening download page in browser..." -ForegroundColor Cyan
    Start-Process "https://ollama.com/download/windows"
    
    Write-Host ""
    Write-Host "INSTRUCTIONS:" -ForegroundColor Yellow
    Write-Host "1. Download OllamaSetup.exe from the browser" -ForegroundColor White
    Write-Host "2. Run the installer" -ForegroundColor White
    Write-Host "3. Click 'Next' through all prompts" -ForegroundColor White
    Write-Host "4. Press Enter here when done" -ForegroundColor Cyan
    Read-Host
}

# Add Ollama to PATH if not already there
Write-Host ""
Write-Host "Checking PATH configuration..." -ForegroundColor Yellow
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*Ollama*") {
    Write-Host "Adding Ollama to PATH..." -ForegroundColor Cyan
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ollamaPath", "User")
    $env:Path = "$env:Path;$ollamaPath"
    Write-Host "   [OK] PATH updated" -ForegroundColor Green
} else {
    Write-Host "   [OK] Ollama already in PATH" -ForegroundColor Green
}

# Refresh environment in current session
Write-Host ""
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Test installation
Write-Host ""
Write-Host "Testing Ollama installation..." -ForegroundColor Yellow
try {
    $testResult = & "$ollamaPath\ollama.exe" --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Ollama is installed and working!" -ForegroundColor Green
        Write-Host "   Version: $testResult" -ForegroundColor Gray
    } else {
        throw "Ollama command failed"
    }
} catch {
    Write-Host "   [WARN] Ollama installed but not accessible in current session" -ForegroundColor Yellow
    Write-Host "   SOLUTION: Close and reopen PowerShell, then continue" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Green
Write-Host "1. If Ollama command doesn't work, restart PowerShell" -ForegroundColor White
Write-Host "2. Run: ollama serve (in a separate window)" -ForegroundColor White
Write-Host "3. Run: .\setup_ollama_models.ps1 (to download models)" -ForegroundColor White
