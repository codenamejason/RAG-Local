# Quick Start Guide

## 5-Minute Setup

### 0. Choose Your Terminal (IMPORTANT!)

**Windows Users: You have 2 options - pick ONE and stick with it:**

| Terminal | When to Use | Setup Script |
|----------|-------------|--------------|
| **PowerShell** | Windows default, system admin tasks | `.\setup_uv.ps1` |
| **Git Bash** | Unix commands, familiar Linux-style | `./setup_uv.sh` |

**Mac Users: You're lucky - just one option:**
| Terminal | When to Use | Setup Script |
|----------|-------------|--------------|
| **Terminal/iTerm** | Unix-based, everything just works | `./setup_uv.sh` |

**💡 Pro Tip:** If you're unsure which terminal you're in, look at your prompt:
- `PS C:\...>` = PowerShell → Use `.\setup_uv.ps1`
- `user@machine MINGW64` = Git Bash → Use `./setup_uv.sh`
- `username@MacBook-Pro` = Mac Terminal → Use `./setup_uv.sh`

**⚠️ Don't mix terminals during setup - pick one and use it consistently!**

### 1. Clone and Setup (30 seconds)

**PowerShell:**
```powershell
git clone <repo-url>
cd rag-pipeline
.\setup_uv.ps1
```

**Git Bash:**
```bash
git clone <repo-url>
cd rag-pipeline
./setup_uv.sh
```

**Mac Terminal:**
```bash
git clone <repo-url>
cd rag-pipeline
./setup_uv.sh
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

**PowerShell:**
```powershell
uv run rag-example
```

**Git Bash:**
```bash
uv run rag-example
```

**Mac Terminal:**
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

**PowerShell:**
```powershell
uv run rag-cli
```

**Git Bash:**
```bash
uv run rag-cli
```

**Mac Terminal:**
```bash
uv run rag-cli
```

**Example session:**
```
> add Machine learning is a subset of AI
✅ Added document (3 chunks created)

> query What is machine learning?
💬 Answer: Machine learning is a subset of artificial intelligence...
```

### Jupyter Notebook

**PowerShell:**
```powershell
uv run jupyter notebook rag_example.ipynb
```

**Git Bash:**
```bash
uv run jupyter notebook rag_example.ipynb
```

**Mac Terminal:**
```bash
uv run jupyter notebook rag_example.ipynb
```

## Common Commands

### PowerShell Users
| Command | Description |
|---------|-------------|
| `.\run_with_uv.ps1 example` | Run the example with sample data |
| `.\run_with_uv.ps1 cli` | Start interactive CLI |
| `.\run_with_uv.ps1 notebook` | Open Jupyter notebook |
| `.\run_with_uv.ps1 test` | Run tests |
| `.\run_with_uv.ps1 install` | Update dependencies |

### Git Bash Users
| Command | Description |
|---------|-------------|
| `uv run python -m src.example_usage` | Run the example |
| `uv run python -m src.cli` | Start interactive CLI |
| `uv run jupyter notebook rag_example.ipynb` | Open Jupyter notebook |
| `uv run pytest` | Run tests |
| `uv pip sync pyproject.toml` | Update dependencies |

### Mac Terminal Users
| Command | Description |
|---------|-------------|
| `uv run python -m src.example_usage` | Run the example |
| `uv run python -m src.cli` | Start interactive CLI |
| `uv run jupyter notebook rag_example.ipynb` | Open Jupyter notebook |
| `uv run pytest` | Run tests |
| `uv pip sync pyproject.toml` | Update dependencies |

## Troubleshooting

### "uv: command not found"
**You haven't run the setup script yet!**
- **PowerShell**: Run `.\setup_uv.ps1`
- **Git Bash**: Run `./setup_uv.sh`
- **Mac Terminal**: Run `./setup_uv.sh`

**💡 After running setup, UV will be permanently added to your PATH!**

### "UV worked yesterday but not today"
**This is a PATH persistence issue. The setup script now fixes this automatically, but if you're still having problems:**

**PowerShell:**
```powershell
# Add UV to current session PATH
$env:PATH += ";$env:USERPROFILE\.local\bin"

# Verify it works
uv --version
```

**Git Bash/Mac:**
```bash
# Add UV to current session PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Verify it works
uv --version
```

**The setup scripts now automatically add UV to your permanent PATH so this won't happen again.**

### "Import anthropic could not be resolved"
```bash
uv pip sync pyproject.toml
```

### "Dimension mismatch" error
**PowerShell:**
```powershell
Remove-Item -Recurse -Force "data\chroma"
```

**Git Bash:**
```bash
rm -rf data/chroma
```

**Mac Terminal:**
```bash
rm -rf data/chroma
```

### PowerShell execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### "Wrong terminal" confusion
**If you're in PowerShell but want to use Git Bash:**
1. Open Git Bash
2. Navigate to your project: `cd /c/Users/username/Projects/RAG\ Shit`
3. Run: `./setup_uv.sh`

**If you're in Git Bash but want to use PowerShell:**
1. Open PowerShell
2. Navigate to your project: `cd "C:\Users\username\Projects\RAG Shit"`
3. Run: `.\setup_uv.ps1`

**Mac Users:** You're already in the right terminal - just run `./setup_uv.sh` and you're good to go!

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

**💡 Remember**: Pick your terminal, run the right setup script, and stick with it!
