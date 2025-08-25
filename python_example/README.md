# Python Local RAG System

**100% Local • Zero Cost • Complete Privacy**

A pure Python implementation of Retrieval-Augmented Generation (RAG) that runs entirely on your machine. No API keys, no cloud services, no data leaving your computer.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- 4GB+ RAM (8GB recommended)
- Windows, macOS, or Linux

### One-Line Setup

**Windows (PowerShell):**
```powershell
.\scripts\windows\setup_complete.ps1
```

**macOS/Linux:**
```bash
./scripts/unix/setup_complete.sh
```

This will:
1. Install Ollama (local LLM server)
2. Download TinyLlama model (1.1B parameters, runs on any machine)
3. Download Nomic embedding model
4. Set up Python environment
5. Install all dependencies

### Manual Setup

1. **Install Ollama:**
   - Download from [ollama.ai](https://ollama.ai)
   - Or use scripts: `.\scripts\windows\install_ollama_windows.ps1`

2. **Pull Models:**
   ```bash
   ollama pull tinyllama
   ollama pull nomic-embed-text
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Interactive CLI
```bash
python src/cli.py
```

### Python Script
```python
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize
rag = LocalRAGPipeline()

# Add documents
rag.add_documents([
    "Python is a versatile programming language.",
    "RAG combines retrieval and generation."
])

# Query
response = rag.query("What is Python?")
print(response['answer'])
```

### Jupyter Notebook
```bash
jupyter notebook rag_example.ipynb
```

## 📁 Project Structure

```
python_example/
├── src/                    # Core RAG implementation
│   ├── rag_pipeline_local.py  # Main pipeline
│   ├── llm_local.py           # Ollama LLM wrapper
│   ├── embeddings_local.py    # Local embeddings
│   ├── vector_store_lancedb.py # Vector storage
│   ├── chunking.py            # Text chunking
│   └── cli.py                 # Interactive CLI
├── scripts/               # Setup & utility scripts
│   ├── windows/          # Windows scripts
│   └── unix/            # macOS/Linux scripts
├── tests/                # Test suite
├── docs/                 # Detailed documentation
├── config/              # Configuration files
└── requirements.txt     # Python dependencies
```

## 🎯 Features

- **100% Local**: Everything runs on your machine
- **Zero Cost**: No API fees, ever
- **Private**: Your data never leaves your computer
- **Fast**: Optimized for local inference
- **Simple**: Clean API, easy to understand
- **Extensible**: Modular design for customization

## 🔧 Configuration

Create a `.env` file (optional):
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=tinyllama:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## 📊 Model Options

| RAM | Model | Quality | Speed |
|-----|-------|---------|-------|
| 4GB | tinyllama | Good | Fast |
| 8GB | mistral | Better | Good |
| 16GB | llama2:13b | Great | Moderate |
| 32GB+ | mixtral | Best | Slower |

## 🧪 Testing

Run the test suite:
```bash
python tests/test_local_rag.py
```

## 📚 Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Setup Guide](docs/setup.md) - Detailed installation instructions
- [Learning RAG](docs/learn.md) - Understanding RAG concepts
- [Migration Guide](docs/migration.md) - Upgrading from older versions

## 🛠️ Development

### Using UV (Recommended)
UV is a fast Python package manager:
```bash
# Install uv
.\scripts\windows\setup_uv.ps1  # Windows
./scripts/unix/setup_uv.sh      # Unix

# Run with uv
uv run python src/cli.py
```

### Code Quality
```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
pylint src/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - Use freely in your projects!

## 🆘 Troubleshooting

### Ollama not running?
```bash
# Start Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Model not found?
```bash
# List models
ollama list

# Pull missing model
ollama pull tinyllama
```

### Out of memory?
- Use smaller models (tinyllama instead of llama2)
- Reduce chunk_size in config
- Close other applications

## 🌟 Why Local RAG?

- **Privacy First**: Your documents, your queries, your hardware
- **No Vendor Lock-in**: Not dependent on any cloud service
- **Cost Effective**: One-time setup, unlimited usage
- **Fast Iteration**: No network latency
- **Full Control**: Customize everything

---

Built with ❤️ for the local-first community