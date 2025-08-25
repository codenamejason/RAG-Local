# TypeScript Local RAG

**100% Local | Zero Cost | Complete Privacy | Modern TypeScript**

A pure TypeScript implementation of RAG that runs entirely on your machine. No API keys, no cloud services, no monthly bills.

## Features

- ✅ **Pure TypeScript** - Type-safe, modern, clean
- ✅ **Zero Dependencies** on cloud services
- ✅ **Ollama Integration** - Local LLMs and embeddings
- ✅ **Simple Vector Store** - In-memory for demos (upgrade to VectorDB for production)
- ✅ **Text Chunking** - Smart document splitting
- ✅ **Cost Tracking** - Always shows $0.00

## Quick Start

### 1. Install Ollama

```bash
# Windows
winget install Ollama.Ollama

# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama & Get Models

```bash
# Start Ollama service
ollama serve

# In another terminal, pull models
ollama pull tinyllama        # LLM (637MB)
ollama pull nomic-embed-text  # Embeddings (274MB)
```

### 3. Install & Run

```bash
# Clone and enter directory
cd typescript_example

# Install dependencies
npm install

# Run tests
npm test

# Run demo
npm run dev
```

## Usage

```typescript
import { LocalRAG } from '@local-rag/typescript';

// Initialize
const rag = new LocalRAG({
  llmModel: 'tinyllama:latest',
  chunkSize: 500
});

// Check system
const ready = await rag.isReady();

// Add documents
await rag.addDocuments([
  'Your document text here...',
  'Another document...'
]);

// Query
const response = await rag.query('Your question?');
console.log(response.answer);
console.log(`Cost: $${response.totalCost}`); // Always $0.00!
```

## API

### `LocalRAG`

Main class for the RAG pipeline.

```typescript
const rag = new LocalRAG({
  llmModel?: string,        // Default: 'tinyllama:latest'
  embeddingModel?: string,  // Default: 'nomic-embed-text:latest'
  chunkSize?: number,       // Default: 500
  chunkOverlap?: number,    // Default: 50
  baseUrl?: string         // Default: 'http://localhost:11434'
});
```

### Methods

- `isReady()` - Check if Ollama is running with required models
- `addDocuments(texts: string[])` - Add documents to knowledge base
- `query(question: string, topK?: number)` - Query the RAG system
- `clear()` - Clear the knowledge base
- `getStats()` - Get system statistics

## Architecture

```
Your App
    ↓
LocalRAG
    ├── OllamaClient (LLM + Embeddings)
    ├── TextChunker (Document splitting)
    └── VectorStore (Similarity search)
    
All Local → Zero API Calls → $0.00 Cost
```

## Models

### Recommended by RAM

| RAM | LLM Model | Quality | Speed |
|-----|-----------|---------|-------|
| 4GB | tinyllama | Basic | Fast |
| 8GB | mistral | Good | Good |
| 16GB | llama2:13b | Great | Moderate |
| 32GB+ | mixtral | Best | Slower |

## Project Structure

```
typescript_example/
├── src/
│   ├── index.ts           # Main exports
│   ├── rag-pipeline.ts    # RAG orchestration
│   ├── ollama-client.ts   # Ollama interface
│   ├── vector-store.ts    # Vector storage
│   ├── chunker.ts         # Text chunking
│   ├── example.ts         # Demo script
│   └── test.ts           # Test suite
├── package.json
├── tsconfig.json
└── README.md
```

## Scripts

- `npm run dev` - Run example with hot reload
- `npm test` - Run test suite
- `npm run build` - Build to JavaScript
- `npm start` - Run built version
- `npm run demo` - Run interactive demo

## Environment Variables

Optional `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=tinyllama:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
```

## Troubleshooting

### Ollama not found
```bash
# Check if running
curl http://localhost:11434

# Start it
ollama serve
```

### Models not found
```bash
# List models
ollama list

# Pull required models
ollama pull tinyllama
ollama pull nomic-embed-text
```

### TypeScript errors
```bash
# Clean and rebuild
npm run clean
npm run build
```

## Production Considerations

This is a demo implementation. For production:

1. **Vector Store**: Replace in-memory store with:
   - VectorDB for browser/edge
   - LanceDB for Node.js
   - PostgreSQL with pgvector

2. **Embeddings**: Consider:
   - Transformers.js for browser (ONNX models)
   - Keep Ollama for server-side

3. **Caching**: Add:
   - Embedding cache
   - LLM response cache

4. **Error Handling**: Add:
   - Retry logic
   - Fallback models
   - Better error messages

## Comparison

| Feature | Cloud RAG | Our Local RAG |
|---------|-----------|---------------|
| Cost | $100-1000/mo | $0.00 |
| Privacy | ❌ None | ✅ Complete |
| Internet | Required | Not needed |
| Speed | Variable | Consistent |
| Control | Limited | Total |

## Contributing

Keep it:
- Local (no cloud APIs)
- Free (no paid services)
- Simple (minimal dependencies)
- Type-safe (proper TypeScript)

## License

MIT - Use it, modify it, ship it. Keep it free.

---

**Built with TypeScript and a hatred for API bills.**