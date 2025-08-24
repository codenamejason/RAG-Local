#!/bin/bash
# Setup Ollama Models for Local RAG - Unix/Linux/Mac

echo "=== Setting Up Ollama for Local RAG ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to check if Ollama is running
check_ollama_service() {
    curl -s http://localhost:11434/api/tags >/dev/null 2>&1
    return $?
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Ollama is installed
echo "Checking Ollama installation..."
if command_exists ollama; then
    echo -e "  ${GREEN}[OK]${NC} Ollama found: $(ollama --version)"
else
    echo -e "  ${RED}[FAIL]${NC} Ollama not found!"
    echo -e "  Run: ${CYAN}./install_ollama_unix.sh${NC} first"
    exit 1
fi

# Check if Ollama service is running
echo ""
echo "Checking Ollama service..."
if check_ollama_service; then
    echo -e "  ${GREEN}[OK]${NC} Ollama service is running"
else
    echo -e "  ${RED}[FAIL]${NC} Ollama service not running"
    echo "  Starting Ollama service in background..."
    
    # Start Ollama in background
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    OLLAMA_PID=$!
    
    echo "  Waiting for service to start..."
    sleep 3
    
    if check_ollama_service; then
        echo -e "  ${GREEN}[OK]${NC} Ollama service started (PID: $OLLAMA_PID)"
        echo "  Logs at: /tmp/ollama.log"
    else
        echo -e "  ${YELLOW}[WARN]${NC} Service may still be starting"
        echo -e "  Try manually: ${CYAN}ollama serve${NC}"
        echo "  Then run this script again"
        exit 1
    fi
fi

# Function to pull model with progress
install_model() {
    local MODEL_NAME=$1
    local DESCRIPTION=$2
    
    echo ""
    echo -e "Installing: ${CYAN}$MODEL_NAME${NC}"
    echo -e "Purpose: $DESCRIPTION"
    
    # Check if model already exists
    if ollama list | grep -q "$MODEL_NAME"; then
        echo -e "  ${GREEN}[OK]${NC} Model already installed"
        return
    fi
    
    # Pull the model
    echo "  Downloading (this may take a few minutes)..."
    if ollama pull "$MODEL_NAME"; then
        echo -e "  ${GREEN}[OK]${NC} Successfully installed $MODEL_NAME"
    else
        echo -e "  ${RED}[FAIL]${NC} Failed to install $MODEL_NAME"
        return 1
    fi
}

# Get system RAM
echo ""
echo "=== System Information ==="
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    RAM_BYTES=$(sysctl -n hw.memsize)
    RAM_GB=$((RAM_BYTES / 1073741824))
elif [ "$(uname)" = "Linux" ]; then
    # Linux
    RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    RAM_GB=$((RAM_KB / 1048576))
else
    echo -e "  ${YELLOW}[WARN]${NC} Could not detect RAM"
    RAM_GB=8
fi

echo -e "System RAM: ${CYAN}${RAM_GB}GB${NC}"

# Install models based on RAM
echo ""
echo "=== Model Installation ==="

# 1. Always install embedding model
install_model "nomic-embed-text" "Embeddings (768-dim, high quality, 274MB)"

# 2. Install LLM based on RAM
echo ""
echo "Selecting LLM based on your RAM..."

if [ $RAM_GB -lt 8 ]; then
    echo -e "  ${YELLOW}[WARN]${NC} Less than 8GB RAM detected"
    echo "  Installing lightweight model..."
    install_model "phi" "Lightweight LLM (3.8B params, needs 3GB RAM)"
    RECOMMENDED_MODEL="phi"
elif [ $RAM_GB -lt 16 ]; then
    echo -e "  ${GREEN}[OK]${NC} 8-16GB RAM detected"
    echo "  Installing balanced model..."
    install_model "tinyllama" "Fast & lightweight LLM (1.1B params, needs 2GB RAM)"
    RECOMMENDED_MODEL="tinyllama"
elif [ $RAM_GB -lt 32 ]; then
    echo -e "  ${GREEN}[OK]${NC} 16-32GB RAM detected"
    echo "  Installing high-quality model..."
    install_model "llama2:13b" "High-quality LLM (13B params, needs 16GB RAM)"
    RECOMMENDED_MODEL="llama2:13b"
else
    echo -e "  ${GREEN}[OK]${NC} 32GB+ RAM detected"
    echo "  You can handle larger models!"
    install_model "mistral" "Starting with Mistral (upgrade to mixtral if desired)"
    RECOMMENDED_MODEL="mistral"
    echo ""
    echo -e "  ${CYAN}Optional:${NC} For best quality, run: ollama pull mixtral"
fi

# Test the installation
echo ""
echo "=== Testing Installation ==="

echo "Testing embedding model..."
EMBED_TEST=$(echo '{"model":"nomic-embed-text","prompt":"Hello"}' | \
    curl -s -X POST http://localhost:11434/api/embeddings \
    -H "Content-Type: application/json" -d @-)

if echo "$EMBED_TEST" | grep -q "embedding"; then
    DIM_COUNT=$(echo "$EMBED_TEST" | grep -o '\[' | wc -l)
    echo -e "  ${GREEN}[OK]${NC} Embeddings working!"
else
    echo -e "  ${RED}[FAIL]${NC} Embedding test failed"
fi

echo ""
echo "Testing LLM..."
echo "  Generating response (may take 10-30 seconds)..."
GEN_TEST=$(echo "{\"model\":\"$RECOMMENDED_MODEL\",\"prompt\":\"Say hello in 5 words\",\"stream\":false}" | \
    curl -s -X POST http://localhost:11434/api/generate \
    -H "Content-Type: application/json" -d @- \
    --max-time 60)

if echo "$GEN_TEST" | grep -q "response"; then
    RESPONSE=$(echo "$GEN_TEST" | grep -o '"response":"[^"]*"' | cut -d'"' -f4)
    echo -e "  ${GREEN}[OK]${NC} LLM Response: $RESPONSE"
else
    echo -e "  ${YELLOW}[WARN]${NC} LLM test failed (may need more time to load)"
fi

# Generate example code
echo ""
echo "=== Setup Complete! ==="
echo ""
echo -e "Your local RAG configuration:"
echo -e "  Embedding Model: ${CYAN}nomic-embed-text${NC}"
echo -e "  LLM Model: ${CYAN}$RECOMMENDED_MODEL${NC}"
echo -e "  API Endpoint: ${CYAN}http://localhost:11434${NC}"
echo ""
echo "To use in your code:"
echo ""
cat << EOF
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize with your models
rag = LocalRAGPipeline(
    llm_model="$RECOMMENDED_MODEL",
    embedding_model="nomic-embed-text"
)

# Test it
rag.add_documents(["Your document text here"])
response = rag.query("What is this document about?")
print(f"Cost: \${response.cost}")  # Always \$0.00!
EOF

echo ""
echo -e "${YELLOW}IMPORTANT:${NC} Keep Ollama running in the background!"
echo -e "If it stops, run: ${CYAN}ollama serve${NC}"
