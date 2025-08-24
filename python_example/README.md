# Pure Local RAG System

**100% Local | Zero Cost | No API Keys | Your Data Stays Private**

A production-ready RAG (Retrieval-Augmented Generation) system that runs entirely on your machine. No cloud dependencies, no API costs, complete data privacy.

## Features

- **Completely Local**: Everything runs on your hardware
- **Zero Cost**: No API fees, ever
- **Private**: Your data never leaves your machine
- **Fast**: Optimized for speed with TinyLlama and LanceDB
- **Simple**: One command setup, minimal configuration

## Tech Stack

- **LLM**: Ollama (TinyLlama by default - 637MB)
- **Embeddings**: Ollama (nomic-embed-text - 274MB)
- **Vector Store**: LanceDB (embedded, no server needed)
- **Framework**: Pure Python, no complex dependencies

## Quick Start

### 1. Install Ollama

**Windows:**
```powershell
# Download from https://ollama.ai/download/windows
# Or use our script:
.\scripts\windows\install_ollama_windows.ps1
```

**Mac/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Install Python Dependencies

```bash
# Using uv (recommended - fast)
uv venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### 3. Download Models

```bash
# Minimal setup (< 1GB total)
ollama pull tinyllama
ollama pull nomic-embed-text

# Better quality (if you have more RAM)
ollama pull mistral  # 4.4GB, needs 8GB RAM
ollama pull llama2    # 7.4GB, needs 16GB RAM
```

### 4. Run Tests

```bash
python tests/run_all_tests.py
```

## Usage

```python
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize (zero config needed)
rag = LocalRAGPipeline()

# Add documents
rag.add_documents([
    "path/to/document.txt",
    "path/to/knowledge.md"
])

# Query
response = rag.query("What does the document say about X?")
print(response.answer)
print(f"Cost: ${response.total_cost}")  # Always $0.00!
```

## System Requirements

### Minimum (will work)
- 4GB RAM
- 2GB disk space
- Any CPU from last 10 years

### Recommended (smooth experience)
- 8GB RAM  
- 10GB disk space
- 4+ CPU cores

### Optimal (best performance)
- 16GB RAM
- 20GB disk space
- Modern CPU with 8+ cores
- GPU (optional, for faster inference)

## Model Recommendations by RAM

| RAM | Embedding Model | LLM Model | Performance |
|-----|----------------|-----------|-------------|
| 4GB | nomic-embed-text | tinyllama | Fast, basic quality |
| 8GB | nomic-embed-text | mistral | Good balance |
| 16GB | nomic-embed-text | llama2:13b | High quality |
| 32GB+ | nomic-embed-text | mixtral | Best quality |

## Project Structure

```
python_example/
├── src/
│   ├── rag_pipeline_local.py  # Main pipeline
│   ├── llm_local.py           # Ollama LLM wrapper
│   ├── embeddings_local.py    # Local embeddings
│   ├── vector_store_lancedb.py # LanceDB store
│   └── chunking.py            # Text chunking
├── tests/
│   ├── test_local_rag.py     # Comprehensive tests
│   └── run_all_tests.py      # Test runner
├── scripts/
│   ├── windows/              # Windows setup scripts
│   └── unix/                 # Mac/Linux setup scripts
└── data/
    └── lancedb/              # Vector database (auto-created)
```

## Configuration

Optional `.env` file (not required for basic usage):

```env
# Model Configuration
OLLAMA_LLM_MODEL=tinyllama:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# Advanced Settings
CHUNK_SIZE=512
CHUNK_OVERLAP=50
```

## Troubleshooting

### Ollama not running
```bash
# Start Ollama service
ollama serve

# Check if running
ollama list
```

### Models not found
```bash
# List available models
ollama list

# Pull required models
ollama pull tinyllama
ollama pull nomic-embed-text
```

### Python import errors
```bash
# Ensure you're in the virtual environment
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall dependencies
uv pip install -r requirements.txt
```

## Performance Tips

1. **Use TinyLlama for development** - It's fast and good enough for testing
2. **Batch your documents** - Add multiple documents at once
3. **Enable caching** - Embeddings are cached automatically
4. **Use SSD storage** - LanceDB performs better on SSDs
5. **Close other apps** - Free up RAM for better performance

## Cost Comparison

| Component | Cloud Services | Our System |
|-----------|---------------|------------|
| Embeddings | $0.10/million tokens | $0.00 |
| LLM | $1-3/million tokens | $0.00 |
| Vector DB | $10-100/month | $0.00 |
| **Total Monthly** | $50-500+ | **$0.00** |

## Privacy & Security

- **No data leaves your machine** - Everything is processed locally
- **No API keys needed** - No risk of key exposure
- **No usage tracking** - Your queries are private
- **Full control** - You own your data and models

## Contributing

This is a pure local system. When contributing:
- Don't add cloud service dependencies
- Keep the zero-cost principle
- Maintain simplicity
- Test on minimal hardware

## License

MIT - Use it, modify it, ship it. Just keep it local and free.

## Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Start a discussion for questions
- **Philosophy**: If it costs money or needs internet, we don't want it

---

**Remember**: Every query you run locally is money saved and privacy preserved. Welcome to true independence from cloud services.