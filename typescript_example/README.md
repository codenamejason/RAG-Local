# TypeScript Local RAG System

**100% Local • Zero Cost • Complete Privacy • Type Safe**

A modern TypeScript implementation of Retrieval-Augmented Generation (RAG) that runs entirely on your machine. Built with type safety and developer experience in mind.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- 4GB+ RAM (8GB recommended)
- Windows, macOS, or Linux

### Setup

1. **Install Ollama:**
   ```bash
   # Download from https://ollama.ai
   # Or use: curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull Models:**
   ```bash
   ollama pull tinyllama
   ollama pull nomic-embed-text
   ```

3. **Install & Run:**
   ```bash
   npm install
   npm test     # Run tests
   npm run dev  # Run example
   ```

That's it! No API keys needed.

## 💻 Usage

### Basic Example
```typescript
import { LocalRAGPipeline } from "./src/rag-pipeline";

// Initialize
const rag = new LocalRAGPipeline();

// Check system
if (!await rag.checkSystem()) {
  console.error("Ollama not running!");
  process.exit(1);
}

// Add documents
await rag.addDocuments([
  "TypeScript adds static typing to JavaScript.",
  "RAG combines retrieval with generation."
]);

// Query
const response = await rag.query("What is TypeScript?");
console.log(response.answer);
```

### Interactive Demo
```bash
npm run dev
```

## 📁 Project Structure

```
typescript_example/
├── src/                   # Core implementation
│   ├── rag-pipeline.ts   # Main RAG orchestration
│   ├── ollama-client.ts  # Ollama API client
│   ├── vector-store.ts   # In-memory vector DB
│   ├── chunker.ts        # Text chunking
│   ├── example.ts        # Usage example
│   ├── test.ts          # Test suite
│   └── index.ts         # Package exports
├── docs/                 # Documentation
│   └── architecture.md   # System design
├── package.json         # Dependencies
├── tsconfig.json       # TypeScript config
├── .eslintrc.js       # Linting rules
└── .prettierrc        # Code formatting
```

## 🎯 Features

- **Type Safe**: Full TypeScript with strict mode
- **Zero Dependencies**: Only dev dependencies for tooling
- **Fast**: Optimized for local inference
- **Clean API**: Simple, intuitive interfaces
- **Well Tested**: Comprehensive test coverage
- **Modern**: ES2022, async/await, latest Node.js

## 🔧 Configuration

Optional `.env` file:
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

## 🧪 Development

### Scripts
```bash
npm run dev      # Run with hot reload
npm test         # Run tests
npm run build    # Build to JavaScript
npm start        # Run production build
npm run lint     # Check code quality
npm run lint:fix # Auto-fix issues
npm run format   # Format with Prettier
npm run check    # Lint, build, and test
```

### Code Quality
- ESLint for linting
- Prettier for formatting
- TypeScript strict mode
- No `any` types

## 📚 API Reference

### LocalRAGPipeline
```typescript
class LocalRAGPipeline {
  constructor(options?: RAGOptions);
  checkSystem(): Promise<boolean>;
  addDocuments(documents: string[]): Promise<void>;
  query(question: string, k?: number): Promise<QueryResult>;
  clear(): void;
  getStats(): Record<string, string | number>;
}
```

### OllamaClient
```typescript
class OllamaClient {
  constructor(options?: OllamaOptions);
  isRunning(): Promise<boolean>;
  listModels(): Promise<string[]>;
  generate(prompt: string): Promise<string>;
  embed(text: string): Promise<number[]>;
}
```

### VectorStore
```typescript
class VectorStore {
  addDocuments(documents: Document[]): Promise<void>;
  search(embedding: number[], k: number): Promise<SearchResult[]>;
  clear(): void;
  count(): number;
}
```

## 🛠️ Extending

### Custom Embeddings
```typescript
interface EmbeddingProvider {
  embed(text: string): Promise<number[]>;
  embedBatch(texts: string[]): Promise<number[][]>;
}
```

### Custom Vector Store
```typescript
interface VectorStore {
  addDocuments(docs: Document[]): Promise<void>;
  search(query: number[], k: number): Promise<SearchResult[]>;
}
```

## 🆘 Troubleshooting

### Ollama not running?
```bash
# Start Ollama
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

### TypeScript errors?
```bash
# Check types
npx tsc --noEmit

# Fix linting
npm run lint:fix
```

## 📄 License

MIT License - Use freely in your projects!

## 🌟 Why TypeScript RAG?

- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: IntelliSense, refactoring
- **Modern JavaScript**: Latest ES features
- **Clean Architecture**: Interfaces and modules
- **Fast Development**: Hot reload with tsx

## 📖 Documentation

- [Architecture](docs/architecture.md) - System design and patterns

---

Built with 🚀 TypeScript for the modern developer