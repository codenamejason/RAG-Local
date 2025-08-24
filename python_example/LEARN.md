# 📚 Learn: Building a Local RAG System

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is an AI architecture that combines:
1. **Information Retrieval**: Finding relevant documents from a knowledge base
2. **Augmented Context**: Using retrieved information to enhance prompts
3. **Generation**: Producing accurate, contextual responses using LLMs

## Why Local RAG?

### Traditional Cloud-Based RAG
- ❌ Costs money for every API call
- ❌ Your data leaves your machine
- ❌ Rate limits and quotas
- ❌ Internet dependency
- ❌ Privacy concerns

### Our Local RAG System
- ✅ **Zero cost** after initial setup
- ✅ **100% private** - data never leaves your machine
- ✅ **No rate limits** - unlimited queries
- ✅ **Works offline** - no internet needed
- ✅ **Full control** - customize everything

## Core Components

### 1. Document Processing (`src/chunking.py`)
Documents are split into manageable chunks for processing:
- **Chunk Size**: 512 characters (configurable)
- **Overlap**: 50 characters to maintain context
- **Smart Splitting**: Respects paragraphs, sentences, and markdown structure

### 2. Embeddings (`src/embeddings_local.py`)
Convert text into numerical vectors for similarity search:

#### Option A: Ollama Embeddings
```python
from src.embeddings_local import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
```
- Model: `nomic-embed-text` (768 dimensions)
- Speed: ~0.2s per document
- Quality: Excellent for most use cases

#### Option B: Sentence Transformers
```python
from src.embeddings_local import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
```
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Speed: ~0.1s per document
- Quality: Good, slightly lower than Ollama

### 3. Vector Store (`src/vector_store_lancedb.py`)
Store and search embeddings efficiently:

**LanceDB** - Our choice over ChromaDB:
- 10x faster for large datasets
- Zero-copy data access
- Native hybrid search (vector + keyword)
- Automatic versioning
- Better memory efficiency

```python
from src.vector_store_lancedb import LanceDBVectorStore
store = LanceDBVectorStore(
    collection_name="documents",
    embedding_dim=768
)
```

### 4. Local LLM (`src/llm_local.py`)
Generate responses using Ollama:

```python
from src.llm_local import OllamaLLM
llm = OllamaLLM(model="mistral:latest")
```

Model recommendations by RAM:
- **8GB**: `mistral:7b` - Good balance
- **16GB**: `llama2:13b` - Better quality
- **32GB+**: `mixtral:8x7b` - Best quality

### 5. RAG Pipeline (`src/rag_pipeline_local.py`)
Orchestrates the entire process:

```python
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize
rag = LocalRAGPipeline()

# Add documents
rag.add_documents(["Document text..."])

# Query
response = rag.query("Your question")
```

## How It Works

### Step 1: Document Ingestion
```
Documents → Chunking → Embeddings → Vector Store
```
1. Documents are split into chunks
2. Each chunk is converted to an embedding vector
3. Vectors are stored in LanceDB with metadata

### Step 2: Query Processing
```
Query → Embedding → Vector Search → Context Retrieval
```
1. User query is converted to an embedding
2. Similar vectors are found in the database
3. Original text chunks are retrieved

### Step 3: Response Generation
```
Context + Query → LLM → Response
```
1. Retrieved context is combined with the query
2. LLM generates a response using the context
3. Response includes source references

## Performance Optimization

### 1. Caching
Embeddings are automatically cached to avoid recomputation:
```python
# Cache location: ./data/embedding_cache/
# Cache key: MD5 hash of model:text
```

### 2. Batching
Documents are processed in batches for efficiency:
```python
# Default batch size: 100 documents
# Configurable in vector_store_lancedb.py
```

### 3. Index Creation
Create an ANN index for faster search:
```python
store.create_index(metric="L2", nprobes=20)
```

## Cost Analysis

### Traditional Setup (Cloud APIs)
- OpenAI Embeddings: $0.13 per million tokens
- Anthropic Claude: $0.25-1.25 per million tokens
- **Monthly cost**: $10-1000+ depending on usage

### Our Local Setup
- Initial setup: ~1 hour
- Model downloads: ~5-30GB storage
- **Running cost**: $0.00 forever

### Break-even Analysis
At just 100 queries/day, you save ~$11/month.
**Break-even time**: Less than 3 months!

## Advanced Features

### 1. Hybrid Search
Combine vector similarity with keyword matching:
```python
results = store.search(
    query="Python programming",
    hybrid_search=True,
    top_k=5
)
```

### 2. Metadata Filtering
Filter results by metadata:
```python
results = store.search(
    query="Your query",
    filter_metadata={"source": "documentation"}
)
```

### 3. Custom Prompts
Customize system prompts for different use cases:
```python
response = rag.query(
    query="Explain this code",
    system_prompt="You are a code tutor..."
)
```

## Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Solution: Install Ollama from https://ollama.ai
   - Start service: `ollama serve`

2. **"Model not found"**
   - Solution: Pull models
   ```bash
   ollama pull nomic-embed-text:latest
   ollama pull mistral:latest
   ```

3. **"Out of memory"**
   - Solution: Use smaller models
   - `phi` instead of `mistral`
   - Reduce batch size

4. **"Slow performance"**
   - Solution: Create index
   - Use SSD for data directory
   - Enable caching

## Learning Resources

### Understanding RAG
- [What is RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Building RAG Systems](https://www.llamaindex.ai/blog/building-production-ready-rag-applications)

### Vector Databases
- [LanceDB Documentation](https://lancedb.github.io/lancedb/)
- [Vector Search Explained](https://www.pinecone.io/learn/vector-search/)

### Local LLMs
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Model Selection Guide](https://ollama.ai/library)

### Embeddings
- [Sentence Transformers](https://www.sbert.net/)
- [Understanding Embeddings](https://www.pinecone.io/learn/embeddings/)

## Next Steps

1. **Experiment with Models**: Try different models for your use case
2. **Add Your Data**: Index your own documents
3. **Customize Chunking**: Adjust chunk size for your content
4. **Build Applications**: Create chatbots, Q&A systems, etc.
5. **Optimize Performance**: Fine-tune for your hardware

## Key Takeaways

- **Local RAG is production-ready**: This isn't a toy - it's real, usable technology
- **Cost savings are massive**: Literally $0 to run after setup
- **Privacy is absolute**: Your data never leaves your machine
- **Performance is excellent**: Often faster than cloud APIs
- **Customization is unlimited**: You control every aspect

---

**Remember**: The best RAG system is the one that costs nothing to run and keeps your data private. That's what we've built here.