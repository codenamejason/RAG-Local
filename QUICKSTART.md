# Quick Start Guide

## 5-Minute Setup

### 1. Clone and Setup (30 seconds)
```bash
git clone <repo-url>
cd rag-pipeline
.\setup_uv.ps1  # Windows (or ./setup_uv.sh for Linux/Mac)
```

### 2. Configure API Keys (1 minute)
Create a `.env` file with your keys:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
```

Get your keys:
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com/) → API Keys
- **OpenAI**: [platform.openai.com](https://platform.openai.com/api-keys) → Create new secret key

### 3. Test the System (30 seconds)
```bash
uv run rag-example
```

## What You Get

A complete RAG system with:
- ✅ **Document chunking** - Smart text splitting with overlap
- ✅ **Semantic search** - OpenAI embeddings for accurate retrieval  
- ✅ **Context-aware generation** - Claude generates answers from your data
- ✅ **Local storage** - ChromaDB keeps everything on your machine
- ✅ **Production ready** - Error handling, logging, and retry logic

## Usage Examples

### Basic Usage
```python
from src.rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline()

# Add documents
rag.add_document("Your document text here")

# Query
response = rag.query("Your question?")
print(response.answer)
```

### Interactive CLI
```bash
uv run rag-cli

> add Machine learning is a subset of AI
✅ Added document (3 chunks created)

> query What is machine learning?
💬 Answer: Machine learning is a subset of artificial intelligence...
```

### Jupyter Notebook
```bash
uv run jupyter notebook rag_example.ipynb
```

## Common Commands

| Command | Description |
|---------|-------------|
| `.\run_with_uv.ps1 example` | Run the example with sample data |
| `.\run_with_uv.ps1 cli` | Start interactive CLI |
| `.\run_with_uv.ps1 notebook` | Open Jupyter notebook |
| `.\run_with_uv.ps1 test` | Run tests |
| `.\run_with_uv.ps1 install` | Update dependencies |

## Troubleshooting

### "Import anthropic could not be resolved"
```bash
uv pip sync pyproject.toml
```

### "Dimension mismatch" error
```bash
# Clear ChromaDB data
Remove-Item -Recurse -Force "data\chroma"
```

### PowerShell execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

## Cost Estimates

| Component | Cost | Notes |
|-----------|------|-------|
| OpenAI Embeddings | $0.0001 per 1K tokens | ~750 words |
| Claude 3 Haiku | $0.25 per 1M input tokens | Fast & cheap |
| ChromaDB | Free | Runs locally |

**Typical usage**: ~$0.01-0.05 per conversation

## Next Steps

1. **Add your data**: Replace example documents with your content
2. **Customize chunking**: Adjust `chunk_size` and `chunk_overlap`
3. **Try different models**: Use Claude Sonnet/Opus for better quality
4. **Build an API**: Wrap in FastAPI for production use
5. **Add a UI**: Use Gradio or Streamlit for web interface

## Learn More

- Read [LEARN.md](LEARN.md) for deep-dive exercises
- Check [src/](src/) for implementation details
- Run tests with `uv run pytest`

---

**Built with UV** - Because life's too short for slow package managers 🚀
