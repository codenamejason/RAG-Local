# RAG Pipeline with Anthropic Claude & OpenAI

A production-ready Retrieval-Augmented Generation (RAG) system using Anthropic's Claude for generation and OpenAI for semantic embeddings.

## Overview

This project implements a complete RAG pipeline that allows you to:
- Build a searchable knowledge base from your documents
- Use semantic search to find relevant information
- Generate accurate, context-aware responses using Claude
- Reduce hallucinations by grounding responses in your data

## Setup

### Prerequisites
- Python 3.9+ (3.11 recommended)
- [uv](https://github.com/astral-sh/uv) - The fast Python package manager (10-100x faster than pip)

### Installation with UV (Recommended - FAST!)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <project-directory>
```

2. Run the setup script:
```bash
# Windows PowerShell
.\setup_uv.ps1

# Linux/Mac
chmod +x setup_uv.sh
./setup_uv.sh
```

This will:
- Install `uv` if not present
- Create a virtual environment
- Install all dependencies (FAST!)
- Set up your project structure

3. Add your API keys to `.env`:
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Alternative: Manual UV Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# or
irm https://astral.sh/uv/install.ps1 | iex  # Windows PowerShell

# Create venv and install deps
uv venv
source .venv/bin/activate  # Linux/Mac
# or
.\.venv\Scripts\activate  # Windows

uv pip sync pyproject.toml
uv pip install -e ".[dev]"
```

## Usage

### Quick Start with UV

1. **Run the example:**
```bash
uv run rag-example
# or use the helper script
.\run_with_uv.ps1 example  # Windows
```

2. **Interactive CLI:**
```bash
uv run rag-cli
# or
.\run_with_uv.ps1 cli  # Windows
```

3. **Jupyter notebook:**
```bash
uv run jupyter notebook rag_example.ipynb
# or
.\run_with_uv.ps1 notebook  # Windows
```

### Python API

```python
from src.rag_pipeline import RAGPipeline

# Initialize
rag = RAGPipeline()

# Add documents
rag.add_document("Your document text here", metadata={"source": "example"})

# Query
response = rag.query("Your question here")
print(response.answer)
```

## Testing

Run tests with coverage:
```bash
uv run pytest
# or
.\run_with_uv.ps1 test  # Windows
```

Run code quality checks:
```bash
uv run black src tests
uv run flake8 src tests
uv run mypy src
```

## Project Structure

```
.
├── src/                 # Source code
│   ├── __init__.py
│   ├── main.py         # Entry point
│   └── config.py       # Configuration
├── tests/              # Test files
│   ├── __init__.py
│   └── test_main.py
├── data/               # Data files (gitignored)
├── models/             # Model files (gitignored)
├── logs/               # Log files (gitignored)
├── .gitignore
├── pyproject.toml     # All dependencies & config (uv-compatible)
├── setup_uv.ps1       # Fast setup with uv (Windows)
├── setup_uv.sh        # Fast setup with uv (Linux/Mac)
├── run_with_uv.ps1    # Helper script for uv commands
└── README.md          # This file
```

## Features

- 🚀 **Fast & Scalable**: Uses ChromaDB for efficient vector storage
- 🎯 **Accurate**: OpenAI embeddings for precise semantic search
- 💬 **Intelligent**: Claude 3 for high-quality response generation
- 📚 **Flexible**: Support for text and markdown documents
- 🔧 **Configurable**: Adjustable chunk sizes, overlap, and retrieval settings
- 📊 **Observable**: Built-in logging and performance metrics

## API Keys Required

1. **Anthropic API Key**: Get it at [console.anthropic.com](https://console.anthropic.com/)
2. **OpenAI API Key**: Get it at [platform.openai.com](https://platform.openai.com/)

## Next Steps

- [ ] Add PDF and web scraping support
- [ ] Implement streaming responses
- [ ] Add FastAPI REST endpoint
- [ ] Build Gradio/Streamlit UI
- [ ] Add evaluation metrics
- [ ] Deploy to production
