# Cross-Platform Local RAG Setup

This project now supports **Windows, macOS, and Linux** with equivalent scripts for each platform.

## 🖥️ Platform Support Matrix

| Script Purpose | Windows | Mac/Linux |
|---------------|---------|-----------|
| Complete Setup | `setup_complete.ps1` | `setup_complete.sh` |
| Install Ollama | `install_ollama_windows.ps1` | `install_ollama_unix.sh` |
| Download Models | `setup_ollama_models.ps1` | `setup_ollama_models.sh` |
| Run Ollama Direct | `run_ollama_direct.bat` | `run_ollama_direct.sh` |
| Install UV | `setup_uv.ps1` | `setup_uv.sh` |

## 🚀 Quick Start by Platform

### Windows (PowerShell)
```powershell
# One command setup
.\setup_complete.ps1
```

### macOS (Terminal)
```bash
# Make scripts executable (first time only)
chmod +x *.sh

# One command setup
./setup_complete.sh
```

### Linux (Terminal)
```bash
# Make scripts executable (first time only)
chmod +x *.sh

# One command setup
./setup_complete.sh
```

## 📦 What Gets Installed

Regardless of platform, you get:
- **Ollama** - Local LLM runtime
- **UV** - Fast Python package manager
- **LanceDB** - High-performance vector database
- **Models**:
  - `nomic-embed-text` - Embeddings (768-dim)
  - `mistral` or appropriate LLM for your RAM

## 🔧 Platform-Specific Notes

### Windows
- Scripts use PowerShell (.ps1)
- Ollama installs to `%LOCALAPPDATA%\Programs\Ollama`
- May need to run as Administrator for first install
- Use `run_ollama_direct.bat` if PATH issues

### macOS
- Scripts use Bash (.sh)
- Can install Ollama via Homebrew: `brew install ollama`
- Models stored in `~/.ollama/models`
- May need to allow Terminal full disk access

### Linux
- Scripts use Bash (.sh)
- Ollama installs to `/usr/local/bin`
- May need `sudo` for system-wide install
- Use `systemctl` to manage Ollama as service (optional)

## 💾 Model Selection by RAM

The setup scripts automatically detect your RAM and suggest appropriate models:

| RAM | Embedding Model | LLM Model | Platform Notes |
|-----|----------------|-----------|----------------|
| <8GB | nomic-embed-text | phi | Works on all platforms |
| 8-16GB | nomic-embed-text | mistral:7b | Recommended minimum |
| 16-32GB | nomic-embed-text | llama2:13b | Great performance |
| 32GB+ | nomic-embed-text | mixtral | Best quality |

## 🐛 Troubleshooting

### All Platforms
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List installed models
ollama list

# Test embedding
ollama run nomic-embed-text "test"

# Test LLM
ollama run mistral "Hello"
```

### Windows Specific
```powershell
# If ollama not in PATH
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve

# Check Windows Defender/Firewall
# May need to allow ollama.exe through firewall
```

### Mac Specific
```bash
# If installed via Homebrew
brew services start ollama

# Check Security & Privacy settings
# May need to allow Terminal/Ollama in Privacy settings
```

### Linux Specific
```bash
# Run as systemd service
sudo systemctl start ollama

# Check logs
journalctl -u ollama -f

# Manual start
ollama serve
```

## 📝 Configuration

All platforms use the same configuration files:
- `config/local_rag_config.yaml` - Main configuration
- `config/settings.py` - Python settings with auto-detection

## 🧪 Testing

Test your setup on any platform:
```bash
python test_local_rag.py
```

Or quick test:
```python
from config.settings import settings
print(settings.get_status())
```

## 📊 Performance

Expected performance across platforms:
- **Embedding generation**: 0.1-0.3s per document
- **Vector search**: <0.1s for 100k documents
- **LLM generation**: 2-10s depending on model and hardware
- **Cost**: $0.00 on all platforms!

## 🔄 Updating

### Update Ollama
```bash
# All platforms
ollama --version
# If update available, reinstall

# Pull latest models
ollama pull nomic-embed-text
ollama pull mistral
```

### Update Python packages
```bash
# Using UV (all platforms)
uv pip install --upgrade lancedb pyarrow sentence-transformers

# Using pip
pip install --upgrade lancedb pyarrow sentence-transformers
```

## 🎯 The Bottom Line

Same zero-cost RAG system, now working on:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu/Debian/Fedora/Arch
- ✅ WSL2
- ✅ Docker containers

**One codebase. Three platforms. Zero API costs.**
