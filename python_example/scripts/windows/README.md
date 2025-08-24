# Windows Scripts

PowerShell and batch scripts for Windows users.

## Quick Start

```powershell
# Main setup script - run this first!
.\setup_complete.ps1
```

## Available Scripts

### Setup Scripts
- `setup_complete.ps1` - Complete one-click setup (installs everything)
- `setup_uv.ps1` - Install UV package manager
- `setup_ollama_models.ps1` - Download Ollama models
- `install_ollama_windows.ps1` - Install Ollama on Windows
- `setup_local.ps1` - Alternative local setup

### Run Scripts
- `run.ps1` - Run the main application
- `run_cli.ps1` - Run CLI interface
- `run_rag_example.ps1` - Run example notebook
- `run_with_uv.ps1` - Run with UV package manager
- `run_ollama_direct.bat` - Start Ollama service directly

## Usage

1. **First Time Setup:**
   ```powershell
   .\setup_complete.ps1
   ```

2. **Start Ollama Service:**
   ```powershell
   # Option 1: Direct batch file
   .\run_ollama_direct.bat
   
   # Option 2: If Ollama is in PATH
   ollama serve
   ```

3. **Run the Application:**
   ```powershell
   cd ..\..
   python quickstart.py
   ```

## Troubleshooting

If scripts don't run due to execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

If Ollama not found:
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```
