# 📜 Platform-Specific Scripts

This directory contains setup and utility scripts organized by platform.

## 📁 Directory Structure

```
scripts/
├── windows/     # Windows PowerShell and batch scripts
│   ├── setup_complete.ps1
│   └── ...
└── unix/        # Mac and Linux bash scripts
    ├── setup_complete.sh
    └── ...
```

## 🚀 Quick Start by Platform

### Windows Users
```powershell
cd windows
.\setup_complete.ps1
```
[See Windows README](./windows/README.md)

### Mac/Linux Users
```bash
cd unix
chmod +x *.sh
./setup_complete.sh
```
[See Unix README](./unix/README.md)

## 🎯 Main Scripts

| Script | Windows | Mac/Linux | Purpose |
|--------|---------|-----------|---------|
| Complete Setup | `setup_complete.ps1` | `setup_complete.sh` | One-click install everything |
| Install Ollama | `install_ollama_windows.ps1` | `install_ollama_unix.sh` | Install Ollama service |
| Setup Models | `setup_ollama_models.ps1` | `setup_ollama_models.sh` | Download AI models |
| Install UV | `setup_uv.ps1` | `setup_uv.sh` | Install UV package manager |
| Run Ollama | `run_ollama_direct.bat` | `run_ollama_direct.sh` | Start Ollama service |

## 📝 Script Categories

### Setup Scripts
Initial installation and configuration scripts. Run these first.

### Run Scripts
Scripts to launch various components of the system.

### Utility Scripts
Helper scripts for maintenance and troubleshooting.

## 💡 Tips

1. **Always start with the complete setup script** for your platform
2. **Keep Ollama running** in a separate terminal
3. **Check RAM requirements** before selecting models
4. **Use UV** for faster Python package management

## 🔧 Customization

All scripts can be edited to customize:
- Model selection
- Installation paths
- Performance settings
- Resource limits

## ❓ Need Help?

- Check platform-specific README files
- Run test script: `python ../../test_local_rag.py`
- See main documentation: [Project README](../README.md)
