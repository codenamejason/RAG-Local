# Local RAG Quick Start - 5 Minutes to Zero-Cost RAG (Cross-Platform)

## The 5-Minute Setup

### Prerequisites Check (30 seconds)

#### All Platforms
```bash
# Check Python
python --version  # Need 3.9+
# or
python3 --version
```

#### Check RAM
**Windows (PowerShell)**
```powershell
(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
```

**Mac**
```bash
echo $(($(sysctl -n hw.memsize) / 1073741824)) GB
```

**Linux**
```bash
echo $(($(grep MemTotal /proc/meminfo | awk '{print $2}') / 1048576)) GB
```

Need 8GB minimum, 16GB recommended

### Step 1: One-Click Setup (2 minutes)

**Windows (PowerShell)**
```powershell
.\setup_complete.ps1
```

**Mac/Linux (Bash)**
```bash
chmod +x setup_complete.sh
./setup_complete.sh
```

This will:
- Install UV package manager
- Check Ollama installation
- Start Ollama service
- Download AI models
- Install Python packages

### Step 2: Manual Ollama Install (if needed) (1 minute)

**Windows**
1. Download: https://ollama.com/download/windows
2. Run the installer
3. Re-run `.\setup_complete.ps1`

**Mac**
```bash
brew install ollama
# or
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 3: Test Everything (1 minute)
```powershell
# Quick test
python -c "from config.settings import settings; print(settings.get_status())"

# Full test
python test_local_rag.py
```

### Step 4: Your First Query (30 seconds)
```python
# test_query.py
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize
rag = LocalRAGPipeline()

# Add a document
rag.add_documents([
    "The Earth orbits the Sun once every 365.25 days. "
    "This orbital period defines one year."
])

# Query it - ZERO COST!
response = rag.query("How long does Earth take to orbit the Sun?")
print(f"Answer: {response.answer}")
print(f"Cost: ${response.cost}")  # Always $0.00!
```

## If Something Goes Wrong

### "Ollama not found"

**Windows**
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

**Mac/Linux**
```bash
ollama serve
# or check common locations
/usr/local/bin/ollama serve
```

### "Model not found"

**All Platforms**
```bash
ollama pull nomic-embed-text
ollama pull mistral
```

**Windows (if not in PATH)**
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull nomic-embed-text
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull mistral
```

### "Module not found"
```powershell
# Install with UV (fast)
uv pip install lancedb pyarrow sentence-transformers

# Or regular pip
pip install lancedb pyarrow sentence-transformers
```

## What You Get

✅ **Embeddings**: FREE (vs $0.13/million tokens)  
✅ **LLM**: FREE (vs $0.25-1.25/million tokens)  
✅ **Vector DB**: LanceDB (10x faster than ChromaDB)  
✅ **Privacy**: 100% local, no data leaves your machine  
✅ **No limits**: No rate limits, no quotas  

## Models by RAM

| Your RAM | Embedding Model | LLM Model | Quality |
|----------|----------------|-----------|---------|
| 8GB | nomic-embed-text | mistral:7b | Good |
| 16GB | nomic-embed-text | llama2:13b | Better |
| 32GB+ | nomic-embed-text | mixtral | Best |

## Next Steps

1. **Read the full docs**: `LOCAL_RAG_SETUP.md`
2. **Check configuration**: `config/settings.py`
3. **Customize models**: Edit `config/local_rag_config.yaml`
4. **Build something**: Stop reading, start coding!

## The Bottom Line

You now have the same capabilities as $500/month cloud services, running for $0/month on your machine.

**Time to build.**
