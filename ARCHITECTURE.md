# Architecture Overview

## System Components

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   User      │────▶│  RAG Pipeline │────▶│   Response  │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Chunking │  │Embeddings│  │Generation│
        └──────────┘  └──────────┘  └──────────┘
                │           │           │
                ▼           ▼           ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │Documents │  │ OpenAI   │  │ Claude   │
        └──────────┘  └──────────┘  └──────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  ChromaDB    │
                    │Vector Store  │
                    └──────────────┘
```

## Core Modules

### 1. RAG Pipeline (`src/rag_pipeline.py`)
**Purpose**: Main orchestrator that coordinates all components

**Key Methods**:
- `add_documents()`: Process and store documents
- `query()`: Retrieve context and generate answers
- `clear_knowledge_base()`: Reset the system

**Configuration**:
```python
RAGPipeline(
    model="claude-3-haiku-20240307",  # Generation model
    collection_name="rag_documents",   # ChromaDB collection
    chunk_size=512,                    # Characters per chunk
    chunk_overlap=50                   # Overlap for context
)
```

### 2. Embeddings (`src/embeddings.py`)
**Purpose**: Convert text to vectors for semantic search

**Provider**: OpenAI
- Model: `text-embedding-ada-002`
- Dimensions: 1536
- Batch size: 100 texts

**Key Features**:
- Automatic retry with exponential backoff
- Batch processing for efficiency
- Separate methods for documents vs queries

### 3. Vector Store (`src/vector_store.py`)
**Purpose**: Store and search document embeddings

**Backend**: ChromaDB
- Local storage in `data/chroma/`
- Persistent across sessions
- Metadata filtering support

**Operations**:
- Add documents with metadata
- Similarity search with scores
- Collection management

### 4. Chunking (`src/chunking.py`)
**Purpose**: Split documents into searchable chunks

**Strategies**:
- `TextChunker`: Generic text splitting
- `MarkdownChunker`: Respects markdown structure

**Algorithm**:
1. Split by separators (paragraphs → sentences → words)
2. Respect chunk size limits
3. Apply overlap for context preservation
4. Preserve metadata

## Data Flow

### Document Ingestion
```
Document → Chunking → Embedding → Vector Store
   │          │           │            │
   │       Split      Generate      Store
   │       into       vectors      with
   │       chunks                metadata
   │
   └─ Metadata preserved throughout
```

### Query Processing
```
Query → Embedding → Vector Search → Context Retrieval → Generation
  │         │             │              │                  │
User    Convert to    Find similar   Get relevant     Claude
input    vector       chunks         documents       response
```

## API Structure

### Request Flow
1. **User Query** → RAGPipeline.query()
2. **Embedding** → OpenAIEmbeddings.embed_query()
3. **Search** → VectorStore.search()
4. **Generation** → Anthropic.messages.create()
5. **Response** → RAGResponse object

### Response Object
```python
@dataclass
class RAGResponse:
    answer: str                        # Generated answer
    sources: List[Tuple[str, float]]   # (text, relevance_score)
    query: str                         # Original query
    model_used: str                    # Claude model name
    context_used: str                  # Retrieved context
```

## Configuration

### Environment Variables
```env
ANTHROPIC_API_KEY=sk-ant-...  # Claude API
OPENAI_API_KEY=sk-...         # Embeddings
DEBUG=True                     # Enable debug logging
LOG_LEVEL=INFO                 # Logging verbosity
```

### Project Configuration (`pyproject.toml`)
- Package management with UV
- Dependency specification
- Tool configurations (black, mypy, pytest)

## Error Handling

### Retry Logic
- API calls: 3 attempts with exponential backoff
- Network errors: Automatic retry
- Rate limits: Backoff and retry

### Logging
- Structured logging throughout
- Configurable log levels
- Performance metrics

## Performance Optimizations

### Caching
- ChromaDB persists embeddings
- No re-embedding of existing documents
- Local storage for fast retrieval

### Batching
- Embed multiple texts in single API call
- Batch size optimization for OpenAI
- Chunking processes documents in parallel

### Cost Optimization
- Use Haiku for fast, cheap generation
- Ada-002 for cost-effective embeddings
- Local ChromaDB eliminates database costs

## Security Considerations

### API Key Management
- Environment variables for secrets
- `.env` file excluded from git
- No hardcoded credentials

### Data Privacy
- All data stored locally
- No automatic cloud uploads
- User controls all data flow

## Scalability

### Current Limits
- ChromaDB: ~1M vectors locally
- OpenAI: 2048 texts per batch
- Claude: 200K token context window

### Scaling Options
1. **Vertical**: Increase chunk size, batch size
2. **Storage**: Move ChromaDB to server
3. **Model**: Upgrade to Claude Opus
4. **Caching**: Add Redis for query cache

## Testing Strategy

### Unit Tests (`tests/`)
- Module isolation
- Mock external APIs
- Edge case coverage

### Integration Tests
- End-to-end pipeline
- Real API calls (with limits)
- Performance benchmarks

### Manual Testing
- Jupyter notebook examples
- CLI interactive testing
- Example scripts

## Deployment Options

### Local Development
```bash
uv run rag-cli
```

### API Server
```python
# Wrap in FastAPI
from fastapi import FastAPI
app = FastAPI()
rag = RAGPipeline()

@app.post("/query")
async def query(text: str):
    return rag.query(text)
```

### Docker Container
```dockerfile
FROM python:3.11
COPY . /app
RUN uv pip install -r pyproject.toml
CMD ["python", "-m", "src.main"]
```

### Cloud Deployment
- AWS Lambda for serverless
- Google Cloud Run for containers
- Heroku for quick prototypes

## Future Enhancements

### Planned Features
- [ ] Streaming responses
- [ ] Multi-modal support (images)
- [ ] Query caching
- [ ] User feedback loop
- [ ] A/B testing framework

### Potential Integrations
- PDF processing
- Web scraping
- Database connectors
- Slack/Discord bots
- API endpoints

---

**Architecture Philosophy**: Simple, modular, and extensible. Each component does one thing well.
