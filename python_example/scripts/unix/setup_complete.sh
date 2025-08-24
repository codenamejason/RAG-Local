#!/bin/bash
# Complete Local RAG Setup Script - Unix/Linux/Mac
# Run this for a one-click setup of everything

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "   COMPLETE LOCAL RAG SETUP"
echo -e "   Zero API Costs Forever!"
echo -e "========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Ollama service
check_ollama_service() {
    curl -s http://localhost:11434/api/tags >/dev/null 2>&1
    return $?
}

# Detect OS
OS="$(uname -s)"
echo -e "Detected OS: ${CYAN}$OS${NC}"

# Step 1: Check Python
echo ""
echo -e "${YELLOW}[1/6] Checking Python installation...${NC}"
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo -e "  ${RED}[FAIL]${NC} Python not found. Please install Python 3.9+"
    if [ "$OS" = "Darwin" ]; then
        echo "  Install with: brew install python3"
    else
        echo "  Install with: sudo apt-get install python3 python3-pip"
    fi
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "  ${GREEN}[OK]${NC} Python found: $PYTHON_VERSION"

# Step 2: Setup UV if not present
echo ""
echo -e "${YELLOW}[2/6] Setting up UV package manager...${NC}"
if command_exists uv; then
    echo -e "  ${GREEN}[OK]${NC} UV already installed: $(uv --version)"
else
    echo -e "  ${GRAY}Installing UV...${NC}"
    
    # Install UV
    if [ -f "./setup_uv.sh" ]; then
        bash ./setup_uv.sh
    else
        # Direct UV installation
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    if command_exists uv; then
        echo -e "  ${GREEN}[OK]${NC} UV installed successfully"
    else
        echo -e "  ${YELLOW}[WARN]${NC} UV installed but may need PATH refresh"
        echo "  Add to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

# Step 3: Install/Check Ollama
echo ""
echo -e "${YELLOW}[3/6] Setting up Ollama...${NC}"

if command_exists ollama; then
    echo -e "  ${GREEN}[OK]${NC} Ollama found"
    ollama --version
else
    echo -e "  ${RED}[FAIL]${NC} Ollama not found!"
    echo ""
    echo -e "  ${YELLOW}Installing Ollama...${NC}"
    
    if [ "$OS" = "Darwin" ]; then
        # macOS
        if command_exists brew; then
            brew install ollama
        else
            curl -fsSL https://ollama.ai/install.sh | sh
        fi
    else
        # Linux
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    if command_exists ollama; then
        echo -e "  ${GREEN}[OK]${NC} Ollama installed"
    else
        echo -e "  ${RED}[FAIL]${NC} Installation failed"
        echo "  Visit: https://ollama.ai/download"
        exit 1
    fi
fi

# Step 4: Start Ollama service
echo ""
echo -e "${YELLOW}[4/6] Starting Ollama service...${NC}"

if check_ollama_service; then
    echo -e "  ${GREEN}[OK]${NC} Ollama service already running"
else
    echo -e "  ${GRAY}Starting Ollama service...${NC}"
    
    # Start in background
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    sleep 3
    
    if check_ollama_service; then
        echo -e "  ${GREEN}[OK]${NC} Ollama service started (PID: $OLLAMA_PID)"
    else
        echo -e "  ${YELLOW}[WARN]${NC} Service may still be starting"
        echo -e "  Run manually: ${CYAN}ollama serve${NC}"
    fi
fi

# Step 5: Pull required models
echo ""
echo -e "${YELLOW}[5/6] Downloading AI models...${NC}"

# Check existing models
MODELS=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}')
echo -e "  ${GRAY}Existing models: ${MODELS:-none}${NC}"

# Pull embedding model if not present
if ! echo "$MODELS" | grep -q "nomic-embed-text"; then
    echo -e "  ${CYAN}Downloading embedding model (nomic-embed-text)...${NC}"
    ollama pull nomic-embed-text
    echo -e "  ${GREEN}[OK]${NC} Embedding model installed"
else
    echo -e "  ${GREEN}[OK]${NC} Embedding model already installed"
fi

# Determine RAM and appropriate model
if [ "$OS" = "Darwin" ]; then
    RAM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 8589934592)
    RAM_GB=$((RAM_BYTES / 1073741824))
elif [ "$OS" = "Linux" ]; then
    RAM_KB=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo 8388608)
    RAM_GB=$((RAM_KB / 1048576))
else
    RAM_GB=8
fi

echo -e "  ${GRAY}System RAM: ${RAM_GB}GB${NC}"

# Select LLM model based on RAM
if [ $RAM_GB -lt 8 ]; then
    LLM_MODEL="phi"
    MODEL_SIZE="1.6GB"
elif [ $RAM_GB -lt 16 ]; then
    LLM_MODEL="mistral"
    MODEL_SIZE="4.1GB"
elif [ $RAM_GB -lt 32 ]; then
    LLM_MODEL="llama2:13b"
    MODEL_SIZE="7.4GB"
else
    LLM_MODEL="mistral"
    MODEL_SIZE="4.1GB"
fi

# Pull LLM if not present
if ! echo "$MODELS" | grep -q "$LLM_MODEL"; then
    echo -e "  ${CYAN}Downloading LLM model ($LLM_MODEL - $MODEL_SIZE)...${NC}"
    echo -e "  ${GRAY}This will take a few minutes...${NC}"
    ollama pull $LLM_MODEL
    echo -e "  ${GREEN}[OK]${NC} LLM model installed"
else
    echo -e "  ${GREEN}[OK]${NC} LLM model already installed"
fi

# Step 6: Install Python dependencies
echo ""
echo -e "${YELLOW}[6/6] Installing Python packages...${NC}"

if command_exists uv; then
    echo -e "  ${GRAY}Using UV (fast)...${NC}"
    uv pip install lancedb pyarrow sentence-transformers requests
else
    echo -e "  ${GRAY}Using pip...${NC}"
    $PYTHON_CMD -m pip install lancedb pyarrow sentence-transformers requests
fi

echo -e "  ${GREEN}[OK]${NC} Python packages installed"

# Final test
echo ""
echo -e "${CYAN}========================================"
echo -e "   TESTING SETUP"
echo -e "========================================${NC}"

# Test embedding
echo ""
echo "Testing embeddings..."
EMBED_TEST=$(echo '{"model":"nomic-embed-text","prompt":"Test"}' | \
    curl -s -X POST http://localhost:11434/api/embeddings \
    -H "Content-Type: application/json" -d @- 2>/dev/null)

if echo "$EMBED_TEST" | grep -q "embedding"; then
    echo -e "  ${GREEN}[OK]${NC} Embeddings working"
else
    echo -e "  ${RED}[FAIL]${NC} Embedding test failed"
fi

# Test LLM
echo ""
echo "Testing LLM generation..."
GEN_TEST=$(echo "{\"model\":\"$LLM_MODEL\",\"prompt\":\"Say hello\",\"stream\":false,\"options\":{\"num_predict\":10}}" | \
    curl -s -X POST http://localhost:11434/api/generate \
    -H "Content-Type: application/json" -d @- \
    --max-time 30 2>/dev/null)

if echo "$GEN_TEST" | grep -q "response"; then
    RESPONSE=$(echo "$GEN_TEST" | grep -o '"response":"[^"]*"' | cut -d'"' -f4)
    echo -e "  ${GREEN}[OK]${NC} LLM Response: $RESPONSE"
else
    echo -e "  ${YELLOW}[WARN]${NC} LLM test failed (may need more time to load)"
fi

# Summary
echo ""
echo -e "${CYAN}========================================"
echo -e "   SETUP COMPLETE!"
echo -e "========================================${NC}"
echo ""
echo -e "${YELLOW}Your Local RAG Stack:${NC}"
echo -e "  - Vector DB: ${CYAN}LanceDB${NC}"
echo -e "  - Embeddings: ${CYAN}nomic-embed-text (768-dim)${NC}"
echo -e "  - LLM: ${CYAN}$LLM_MODEL${NC}"
echo -e "  - API Cost: ${GREEN}\$0.00 forever!${NC}"
echo ""
echo -e "${YELLOW}Quick Test:${NC}"
echo -e "  ${CYAN}$PYTHON_CMD test_local_rag.py${NC}"
echo ""
echo -e "${YELLOW}Usage Example:${NC}"
cat << EOF
from src.rag_pipeline_local import LocalRAGPipeline

rag = LocalRAGPipeline(
    llm_model="$LLM_MODEL",
    embedding_model="nomic-embed-text"
)
rag.add_documents(["Your text here"])
response = rag.query("Your question")
print(f"Cost: \${response.cost}")  # Always \$0.00!
EOF

echo ""
echo -e "${YELLOW}Keep Ollama running:${NC} ${CYAN}ollama serve${NC}"

# Make scripts executable
chmod +x *.sh 2>/dev/null
