#!/bin/bash
# ACTUAL Ollama Installation for Linux/Mac - The way that WORKS

echo "=== Installing Ollama on Unix/Linux/Mac - The RIGHT Way ==="
echo ""

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "Detected OS: $OS"
echo "Detected Architecture: $ARCH"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Method 1: Official Install Script (RECOMMENDED)
echo "Method 1: Official Install Script"
echo "----------------------------------------"

if command_exists ollama; then
    echo "  [OK] Ollama already installed"
    ollama --version
else
    echo "  Installing Ollama..."
    
    if [ "$OS" = "Darwin" ]; then
        # macOS
        if command_exists brew; then
            echo "  Using Homebrew..."
            brew install ollama
        else
            echo "  Using official installer..."
            curl -fsSL https://ollama.ai/install.sh | sh
        fi
    elif [ "$OS" = "Linux" ]; then
        # Linux
        echo "  Using official installer..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "  [FAIL] Unsupported OS: $OS"
        echo "  Manual installation required from: https://ollama.ai/download"
        exit 1
    fi
    
    # Verify installation
    if command_exists ollama; then
        echo "  [OK] Ollama installed successfully"
        ollama --version
    else
        echo "  [FAIL] Installation failed"
        echo ""
        echo "  Manual installation:"
        echo "  1. Visit: https://ollama.ai/download"
        echo "  2. Download for your OS"
        echo "  3. Follow installation instructions"
        exit 1
    fi
fi

# Add to PATH if needed (Linux specific)
if [ "$OS" = "Linux" ]; then
    OLLAMA_PATH="/usr/local/bin"
    if [[ ":$PATH:" != *":$OLLAMA_PATH:"* ]]; then
        echo ""
        echo "Adding Ollama to PATH..."
        echo "export PATH=\"\$PATH:$OLLAMA_PATH\"" >> ~/.bashrc
        echo "export PATH=\"\$PATH:$OLLAMA_PATH\"" >> ~/.zshrc 2>/dev/null
        export PATH="$PATH:$OLLAMA_PATH"
        echo "  [OK] PATH updated"
    fi
fi

# Test installation
echo ""
echo "Testing Ollama installation..."
if ollama --version >/dev/null 2>&1; then
    VERSION=$(ollama --version)
    echo "  [OK] Ollama is installed and working!"
    echo "  Version: $VERSION"
else
    echo "  [WARN] Ollama installed but may need PATH refresh"
    echo "  SOLUTION: Run 'source ~/.bashrc' or start new terminal"
fi

echo ""
echo "=== Next Steps ==="
echo "1. Start Ollama service: ollama serve"
echo "2. Run setup script: ./setup_ollama_models.sh"
echo "3. Pull models: ollama pull nomic-embed-text && ollama pull mistral"
