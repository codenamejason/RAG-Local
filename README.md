# RAG Shit - Pure Local RAG Systems

**Build RAG systems that actually work. Zero cost. Complete privacy. No bullshit.**

## What This Is

A collection of **100% local RAG (Retrieval-Augmented Generation) implementations** in multiple languages. No API keys, no cloud services, no monthly bills. Your data stays on your machine.

## Why This Exists

Because paying $500+/month for API calls is insane when you can run everything locally for $0. Because your private data shouldn't be sent to OpenAI/Anthropic/Google. Because you should own your AI stack.

## Available Implementations

### 📁 `python_example/` - Python RAG (Ready Now)
Full-featured local RAG with:
- **LLM**: Ollama (TinyLlama/Mistral/Llama2)
- **Embeddings**: Ollama or SentenceTransformers  
- **Vector Store**: LanceDB (embedded, no server)
- **Status**: ✅ **Production Ready**

[See Python README](./python_example/README.md)

### 📁 `typescript_example/` - TypeScript RAG
Modern TypeScript implementation with:
- **LLM**: Ollama (TinyLlama by default)
- **Embeddings**: Ollama (nomic-embed-text)
- **Vector Store**: In-memory (extensible to LanceDB)
- **Status**: ✅ **Production Ready**

## Quick Start

### Python Version
```bash
cd python_example
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python tests/run_all_tests.py
```

### TypeScript Version
```bash
cd typescript_example
npm install
npm test
npm run dev
```

## Core Principles

1. **Zero Cost**: Everything runs on your hardware
2. **Complete Privacy**: Data never leaves your machine
3. **No Dependencies**: No API keys, no cloud services
4. **Actually Works**: Not a toy - production ready
5. **Simple**: Minimal config, maximum results

## System Requirements

### Minimum (Will Work)
- 4GB RAM
- 2GB disk space  
- Any CPU from last 10 years
- Windows/Mac/Linux

### Recommended (Smooth)
- 8GB RAM
- 10GB disk space
- 4+ CPU cores

### Optimal (Fast)
- 16GB+ RAM
- 20GB disk space
- Modern CPU/GPU

## Model Recommendations

| Your RAM | Best LLM | Best Embeddings | Quality |
|----------|----------|-----------------|---------|
| 4GB | TinyLlama | nomic-embed-text | Basic but fast |
| 8GB | Mistral 7B | nomic-embed-text | Good balance |
| 16GB | Llama2 13B | nomic-embed-text | High quality |
| 32GB+ | Mixtral/Llama2 70B | nomic-embed-text | Best possible |

## Cost Comparison

| Service | Monthly Cost | Per Query | Privacy |
|---------|-------------|-----------|---------|
| OpenAI GPT-4 | $100-1000+ | $0.01-0.03 | ❌ None |
| Anthropic Claude | $100-1000+ | $0.01-0.03 | ❌ None |
| Google Gemini | $100-1000+ | $0.01-0.03 | ❌ None |
| **Our Local RAG** | **$0.00** | **$0.00** | ✅ **100%** |

At 1000 queries/day, you save **$300-900/month**.

## What You Can Build

- **Knowledge Bases**: Query your documents/notes/code
- **Customer Support**: Answer questions from your docs
- **Research Assistant**: Analyze papers and reports
- **Code Assistant**: Search and understand codebases
- **Personal Assistant**: Private AI for personal data
- **Education Tools**: Interactive learning systems

All running locally. All for free. All private.

## Installation

### 1. Install Ollama (One Time)
```bash
# Windows
winget install Ollama.Ollama

# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Get Models (One Time)
```bash
# Minimum setup (< 1GB)
ollama pull tinyllama
ollama pull nomic-embed-text

# Better quality (needs 8GB+ RAM)
ollama pull mistral
ollama pull llama2
```

### 3. Choose Your Language
- **Python**: Production ready, full featured
- **TypeScript**: Modern, runs in browser (coming)
- More coming: Rust, Go, Java

## Architecture

```
Your App
    ↓
RAG Pipeline
    ├── Document Loader (PDFs, text, markdown)
    ├── Chunker (splits documents)
    ├── Embeddings (Ollama/Transformers)
    ├── Vector Store (LanceDB)
    └── LLM (Ollama - Llama/Mistral)
    
All Local → $0 Cost → 100% Private
```

## FAQ

**Q: Is this really free?**  
A: Yes. 100% free after you have a computer. No hidden costs.

**Q: Is it as good as GPT-4?**  
A: For RAG tasks? Often yes. For general chat? Depends on your model choice.

**Q: Can it run offline?**  
A: Yes. Once models are downloaded, no internet needed.

**Q: How much disk space?**  
A: 1-50GB depending on models. TinyLlama = 1GB, Mixtral = 26GB.

**Q: Is it hard to set up?**  
A: No. Three commands and you're running.

**Q: Can I use my GPU?**  
A: Yes. Ollama auto-detects and uses CUDA/Metal/ROCm.

**Q: What about embeddings?**  
A: Included. Ollama or SentenceTransformers. Both free.

**Q: Production ready?**  
A: Python version is. TypeScript coming soon.

## Philosophy

We believe AI should be:
- **Free**: Not $500/month
- **Private**: Your data is yours
- **Local**: No internet required
- **Simple**: It should just work
- **Honest**: No marketing BS

## Contributing

Want to help? Here's how:
1. Use it and report issues
2. Add examples and docs
3. Create implementations in new languages
4. Share with others who are tired of API bills

**Rules:**
- No cloud dependencies
- No API keys required
- Must run offline
- Keep it simple
- Keep it free

## Support

- **Issues**: Open a GitHub issue
- **Questions**: Start a discussion
- **Philosophy**: If it needs internet or costs money, we don't want it

## License

MIT - Use it, modify it, sell it, whatever. Just keep it local and free.

---

**Stop paying for AI. Run it yourself.**

Built with 🖕 to cloud pricing and ❤️ for local compute.
