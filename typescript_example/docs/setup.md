# TypeScript RAG Setup Guide

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Setup](#quick-setup)
- [Detailed Installation](#detailed-installation)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Node.js**: 18.0.0 or higher
- **CPU**: x64 architecture

### Recommended Specs by Model
| Model | RAM | Storage | Use Case |
|-------|-----|---------|----------|
| TinyLlama | 4GB | 1GB | Basic Q&A, testing |
| Mistral 7B | 8GB | 4GB | Production use |
| Llama2 13B | 16GB | 8GB | Advanced tasks |
| Mixtral | 32GB+ | 20GB | Best quality |

## Quick Setup

### One-Command Setup (All Platforms)

```bash
# Clone and setup
git clone <your-repo>
cd typescript_example
npm install
npm run setup  # Installs Ollama and pulls models
```

## Detailed Installation

### Step 1: Install Node.js

#### Windows
1. Download from [nodejs.org](https://nodejs.org/)
2. Run installer (use LTS version)
3. Verify: `node --version`

#### macOS
```bash
# Using Homebrew
brew install node

# Or download from nodejs.org
```

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Fedora
sudo dnf install nodejs
```

### Step 2: Install Ollama

#### Windows
```powershell
# Download installer
Invoke-WebRequest -Uri "https://ollama.ai/download/OllamaSetup.exe" -OutFile "OllamaSetup.exe"

# Run installer
.\OllamaSetup.exe

# Or use winget
winget install Ollama.Ollama
```

#### macOS
```bash
# Using curl
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai/download
```

#### Linux
```bash
# Official script
curl -fsSL https://ollama.ai/install.sh | sh

# Manual installation
wget https://github.com/ollama/ollama/releases/latest/download/ollama-linux-amd64
chmod +x ollama-linux-amd64
sudo mv ollama-linux-amd64 /usr/local/bin/ollama
```

### Step 3: Start Ollama Service

#### Windows
```powershell
# Ollama runs automatically after installation
# To check:
ollama --version

# If not running:
ollama serve
```

#### macOS/Linux
```bash
# Start service
ollama serve

# Or run in background
nohup ollama serve > /dev/null 2>&1 &
```

### Step 4: Pull Required Models

```bash
# Essential models
ollama pull tinyllama        # 1.1B params, 638MB
ollama pull nomic-embed-text # Embedding model, 274MB

# Optional larger models
ollama pull mistral          # 7B params, 4.1GB
ollama pull llama2:13b       # 13B params, 7.3GB
```

### Step 5: Setup TypeScript Project

```bash
# Clone repository
git clone <your-repo>
cd typescript_example

# Install dependencies
npm install

# Run tests to verify
npm test
```

## Platform-Specific Instructions

### Windows PowerShell Setup

```powershell
# Set execution policy (admin required)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Node.js via Chocolatey
choco install nodejs

# Install Ollama
winget install Ollama.Ollama

# Start Ollama
Start-Process ollama -ArgumentList "serve"

# Pull models
ollama pull tinyllama
ollama pull nomic-embed-text

# Setup project
npm install
npm test
```

### macOS Terminal Setup

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve &

# Pull models
ollama pull tinyllama
ollama pull nomic-embed-text

# Setup project
npm install
npm test
```

### Linux (Ubuntu/Debian) Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install build tools
sudo apt-get install -y build-essential

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama as service
sudo systemctl start ollama
sudo systemctl enable ollama

# Pull models
ollama pull tinyllama
ollama pull nomic-embed-text

# Setup project
npm install
npm test
```

### Docker Setup

```dockerfile
# Dockerfile
FROM node:20-alpine

# Install Ollama
RUN apk add --no-cache curl bash
RUN curl -fsSL https://ollama.ai/install.sh | sh

WORKDIR /app

# Copy project
COPY package*.json ./
RUN npm ci --production

COPY . .

# Start services
CMD ["sh", "-c", "ollama serve & npm start"]
```

```bash
# Build and run
docker build -t typescript-rag .
docker run -p 3000:3000 -p 11434:11434 typescript-rag
```

## Configuration

### Environment Variables

Create `.env` file:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=tinyllama:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# RAG Configuration
VECTOR_STORE_COLLECTION=local_rag
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_SEARCH_RESULTS=5

# Development
NODE_ENV=development
LOG_LEVEL=info
```

### TypeScript Configuration

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### VS Code Settings

`.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "files.exclude": {
    "dist": true,
    "node_modules": true
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Ollama Not Found

```bash
# Check if installed
which ollama  # Unix
where ollama  # Windows

# Add to PATH if needed
export PATH=$PATH:/usr/local/bin  # Unix
$env:Path += ";C:\Program Files\Ollama"  # Windows
```

#### 2. Port Already in Use

```bash
# Find process using port 11434
lsof -i :11434  # Unix
netstat -ano | findstr :11434  # Windows

# Kill process
kill -9 <PID>  # Unix
taskkill /PID <PID> /F  # Windows
```

#### 3. Model Download Fails

```bash
# Check available space
df -h  # Unix
Get-PSDrive  # Windows

# Clear Ollama cache
rm -rf ~/.ollama/models  # Unix
Remove-Item -Recurse $env:USERPROFILE\.ollama\models  # Windows

# Retry with specific version
ollama pull tinyllama:1.1b
```

#### 4. TypeScript Compilation Errors

```bash
# Clear cache and reinstall
rm -rf node_modules dist
npm cache clean --force
npm install

# Check TypeScript version
npx tsc --version

# Compile with verbose output
npx tsc --listFiles
```

#### 5. Memory Issues

```bash
# Increase Node.js memory
export NODE_OPTIONS="--max-old-space-size=4096"  # Unix
$env:NODE_OPTIONS="--max-old-space-size=4096"  # Windows

# Use smaller model
ollama pull tinyllama  # Instead of larger models
```

### Performance Optimization

#### 1. GPU Acceleration (NVIDIA)

```bash
# Check CUDA support
nvidia-smi

# Install CUDA-enabled Ollama
# Follow instructions at https://ollama.ai/docs/gpu
```

#### 2. CPU Optimization

```bash
# Set thread count
export OLLAMA_NUM_THREADS=4

# Enable AVX2 (if supported)
export OLLAMA_USE_AVX2=1
```

#### 3. Network Configuration

```bash
# Change Ollama host
export OLLAMA_HOST=0.0.0.0:11434

# Proxy configuration
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

## Development Setup

### IDE Setup

#### VS Code Extensions
- TypeScript and JavaScript Language Features
- ESLint
- Prettier - Code formatter
- GitLens
- REST Client (for testing APIs)

#### WebStorm/IntelliJ
- Enable TypeScript service
- Configure ESLint
- Set up Prettier

### Git Hooks

```bash
# Install husky
npm install --save-dev husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm test"
```

### Debugging

#### VS Code Launch Configuration

`.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug TypeScript",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/src/example.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "sourceMaps": true
    }
  ]
}
```

#### Chrome DevTools

```bash
# Run with inspector
node --inspect-brk dist/example.js

# Open chrome://inspect in Chrome
```

### Testing Setup

```bash
# Install test dependencies
npm install --save-dev jest @types/jest ts-jest

# Configure Jest
npx ts-jest config:init

# Run tests with coverage
npm test -- --coverage
```

## Next Steps

1. ✅ Verify installation: `npm test`
2. 📚 Read the [Learning Guide](learn.md)
3. 🏗️ Check the [Architecture](architecture.md)
4. 🚀 Run the example: `npm run dev`
5. 💡 Build something amazing!

## Getting Help

- Check [Troubleshooting](#troubleshooting) section
- Review [Ollama Documentation](https://ollama.ai/docs)
- Open an issue on GitHub
- Ask in discussions

---

Happy coding! 🎉
