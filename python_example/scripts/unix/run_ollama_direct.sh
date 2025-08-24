#!/bin/bash
# Direct Ollama runner - bypasses all PATH issues

echo "Starting Ollama directly..."

# Try different possible locations
if [ -f "/usr/local/bin/ollama" ]; then
    echo "Found Ollama at /usr/local/bin"
    /usr/local/bin/ollama serve
elif [ -f "/usr/bin/ollama" ]; then
    echo "Found Ollama at /usr/bin"
    /usr/bin/ollama serve
elif [ -f "$HOME/.local/bin/ollama" ]; then
    echo "Found Ollama in user local bin"
    $HOME/.local/bin/ollama serve
elif [ -f "/opt/ollama/ollama" ]; then
    echo "Found Ollama in /opt"
    /opt/ollama/ollama serve
elif command -v ollama >/dev/null 2>&1; then
    echo "Found Ollama in PATH"
    ollama serve
else
    echo "ERROR: Ollama not found!"
    echo ""
    echo "Please install from: https://ollama.ai/download"
    echo ""
    echo "Quick install:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi
