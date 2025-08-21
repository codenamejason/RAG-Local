#!/bin/bash
# Shell script to set up the project with uv (for Linux/Mac users)
# UV is 10-100x faster than pip - because life is too short for slow package managers

echo -e "\033[36m🚀 Setting up RAG project with uv (the fast way)\033[0m"
echo -e "\033[36m================================================\033[0m"

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo -e "\033[32m✅ Found uv: $(uv --version)\033[0m"
else
    echo -e "\033[33m📦 Installing uv...\033[0m"
    
    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo -e "\033[32m✅ uv installed successfully!\033[0m"
fi

# Create virtual environment with uv
echo -e "\n\033[33m📦 Creating virtual environment with uv...\033[0m"
uv venv --python 3.11

# Activate virtual environment
echo -e "\033[33m🔄 Activating virtual environment...\033[0m"
source .venv/bin/activate

# Sync dependencies (this installs everything from pyproject.toml)
echo -e "\n\033[33m📦 Installing dependencies with uv (this will be FAST)...\033[0m"
uv pip sync pyproject.toml

# Install dev dependencies
echo -e "\n\033[33m📦 Installing dev dependencies...\033[0m"
uv pip install -e ".[dev]"

# Create necessary directories
echo -e "\n\033[33m📁 Creating project directories...\033[0m"
mkdir -p data models logs

# Check for .env file
if [ ! -f .env ]; then
    echo -e "\n\033[33m⚠️  Creating .env file from template...\033[0m"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "\033[33m📝 Created .env file. Please add your API keys:\033[0m"
        echo -e "\033[36m   - ANTHROPIC_API_KEY\033[0m"
        echo -e "\033[36m   - VOYAGE_API_KEY\033[0m"
    fi
else
    echo -e "\n\033[32m✅ .env file already exists\033[0m"
fi

echo -e "\n\033[32m🎉 Setup complete!\033[0m"
echo -e "\033[32m================================================\033[0m"
echo -e "\n\033[36mNext steps:\033[0m"
echo -e "1. Add your API keys to .env"
echo -e "2. Run: uv run rag-example"
echo -e "3. Or run: uv run rag-cli"
echo -e "\n\033[90mTo activate the environment manually:\033[0m"
echo -e "\033[90m   source .venv/bin/activate\033[0m"

# Make the script executable
chmod +x setup_uv.sh
