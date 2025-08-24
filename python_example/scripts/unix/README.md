# Unix/Linux/Mac Scripts

Bash scripts for Unix-based systems (macOS and Linux).

## Quick Start

```bash
# Make scripts executable (first time only)
chmod +x *.sh

# Run complete setup
./setup_complete.sh
```

## Available Scripts

### Setup Scripts
- `setup_complete.sh` - Complete one-click setup (installs everything)
- `setup_uv.sh` - Install UV package manager
- `setup_ollama_models.sh` - Download Ollama models
- `install_ollama_unix.sh` - Install Ollama on Unix systems

### Utility Scripts
- `run_ollama_direct.sh` - Start Ollama service directly
- `make_executable.sh` - Make all scripts executable

## Usage

1. **First Time Setup:**
   ```bash
   # Make scripts executable
   chmod +x *.sh
   
   # Run complete setup
   ./setup_complete.sh
   ```

2. **Start Ollama Service:**
   ```bash
   # Option 1: Direct script
   ./run_ollama_direct.sh
   
   # Option 2: Standard command
   ollama serve
   
   # Option 3: Background service
   nohup ollama serve > /tmp/ollama.log 2>&1 &
   ```

3. **Run the Application:**
   ```bash
   cd ../..
   python quickstart.py
   ```

## Platform-Specific Notes

### macOS
- Install Ollama via Homebrew: `brew install ollama`
- Start as service: `brew services start ollama`

### Linux
- Install: `curl -fsSL https://ollama.ai/install.sh | sh`
- Run as systemd service: `sudo systemctl start ollama`

### Common Issues

**Permission denied:**
```bash
chmod +x script_name.sh
```

**Ollama not found:**
```bash
# Add to PATH
export PATH="$PATH:/usr/local/bin"
```

**Port already in use:**
```bash
# Find process using port 11434
lsof -i :11434
# Kill if needed
kill -9 <PID>
```
