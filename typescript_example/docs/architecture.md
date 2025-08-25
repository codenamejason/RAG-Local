# TypeScript RAG Architecture

## Overview

This TypeScript implementation provides a 100% local, zero-cost Retrieval-Augmented Generation (RAG) system with complete privacy. Built with modern TypeScript and Node.js, it offers type safety and excellent developer experience.

## Core Components

### 1. Ollama Client (`src/ollama-client.ts`)
- **Purpose**: Interface with local Ollama instance for LLM and embeddings
- **Key Features**:
  - Health checks for Ollama service
  - Model listing and validation
  - Text generation with streaming support
  - Embedding generation for single and batch texts
- **Models Used**:
  - LLM: `tinyllama:latest` (default, 1.1B parameters)
  - Embeddings: `nomic-embed-text:latest` (768 dimensions)

### 2. Vector Store (`src/vector-store.ts`)
- **Purpose**: In-memory vector database for document storage and retrieval
- **Key Features**:
  - Document storage with embeddings
  - Cosine similarity search
  - Metadata support
  - Collection management
- **Design Decisions**:
  - In-memory for simplicity and speed
  - No external dependencies
  - Easy to extend to persistent storage

### 3. Text Chunker (`src/chunker.ts`)
- **Purpose**: Split documents into manageable chunks for embedding
- **Key Features**:
  - Configurable chunk size (default: 500 chars)
  - Overlapping chunks (default: 50 chars)
  - Metadata preservation
  - Word boundary respect

### 4. RAG Pipeline (`src/rag-pipeline.ts`)
- **Purpose**: Orchestrate the complete RAG workflow
- **Key Features**:
  - System health checks
  - Document ingestion pipeline
  - Query processing with context retrieval
  - Response generation with source tracking

## Data Flow

```
1. Document Ingestion:
   Documents → Chunker → Embeddings → Vector Store

2. Query Processing:
   Query → Embedding → Vector Search → Context Retrieval

3. Response Generation:
   Context + Query → LLM → Response
```

## Architecture Patterns

### Type Safety
- Strict TypeScript with no implicit `any`
- Interface-based design for extensibility
- Generic types for flexibility

### Async/Await
- All I/O operations are async
- Proper error handling with try/catch
- Promise-based API

### Modular Design
- Each component is independent
- Easy to swap implementations
- Clear interfaces between modules

## Configuration

### Environment Variables
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_LLM_MODEL=tinyllama:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest
VECTOR_STORE_COLLECTION=local_rag
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### TypeScript Configuration
- Target: ES2022
- Module: CommonJS
- Strict mode enabled
- Source maps for debugging

## Performance Characteristics

### Memory Usage
- **Embeddings**: ~3KB per document chunk
- **Vector Store**: O(n) where n = number of documents
- **LLM Context**: Limited by model (2048 tokens for TinyLlama)

### Speed
- **Embedding Generation**: ~100ms per chunk
- **Vector Search**: O(n) linear scan (can be optimized)
- **LLM Generation**: ~2-5 seconds per response

### Scalability
- **Current**: Suitable for up to 10,000 documents
- **Future**: Can add persistent storage and indexing

## Development Tools

### Linting & Formatting
- ESLint with TypeScript plugin
- Prettier for code formatting
- Husky for pre-commit hooks (optional)

### Testing
- Comprehensive test suite (`src/test.ts`)
- Unit tests for each component
- Integration tests for full pipeline

### Build System
- TypeScript compiler for production builds
- tsx for development (no compilation needed)
- npm scripts for common tasks

## Deployment Options

### 1. Local Development
```bash
npm install
npm run dev
```

### 2. Production Build
```bash
npm run build
npm start
```

### 3. Docker Container
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY dist ./dist
CMD ["node", "dist/index.js"]
```

## Extension Points

### Custom Embeddings
Implement the embedding interface:
```typescript
interface EmbeddingProvider {
  embed(text: string): Promise<number[]>;
  embedBatch(texts: string[]): Promise<number[][]>;
}
```

### Custom Vector Store
Implement the vector store interface:
```typescript
interface VectorStore {
  addDocuments(documents: Document[]): Promise<void>;
  search(query: number[], k: number): Promise<SearchResult[]>;
  clear(): void;
}
```

### Custom LLM
Implement the LLM interface:
```typescript
interface LLMProvider {
  generate(prompt: string, options?: any): Promise<string>;
}
```

## Security Considerations

### Data Privacy
- 100% local processing
- No data leaves your machine
- No API keys required
- No telemetry or tracking

### Input Validation
- Sanitize user inputs
- Limit chunk sizes
- Validate embeddings dimensions

### Resource Limits
- Memory limits for vector store
- Token limits for LLM context
- Rate limiting for Ollama calls

## Monitoring & Debugging

### Logging
- Console logging for development
- Structured logging ready (winston/pino)
- Debug mode with verbose output

### Metrics
- Document count tracking
- Query performance timing
- Memory usage monitoring

### Health Checks
- Ollama service status
- Model availability
- Vector store capacity

## Comparison with Python Version

### Advantages
- Type safety catches errors at compile time
- Better IDE support with IntelliSense
- Faster startup time
- Native async/await support
- npm ecosystem

### Trade-offs
- Smaller ML ecosystem than Python
- Less mature vector store options
- Requires Node.js runtime

## Future Enhancements

### Planned Features
1. Persistent vector storage (LanceDB/SQLite)
2. Streaming responses
3. Multi-modal support (images)
4. Web UI with React/Next.js
5. REST API with Express/Fastify

### Performance Optimizations
1. Vector indexing (HNSW, IVF)
2. Caching layer for embeddings
3. Batch processing for large datasets
4. Worker threads for parallel processing

### Integration Options
1. Browser extension
2. VS Code extension
3. CLI tool with npm global install
4. Electron desktop app

## Contributing

### Code Style
- Follow ESLint rules
- Write tests for new features
- Document public APIs with JSDoc
- Keep functions small and focused

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Write tests
4. Update documentation
5. Submit PR with description

## License

MIT License - Use freely in your projects!

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [RAG Paper](https://arxiv.org/abs/2005.11401)
