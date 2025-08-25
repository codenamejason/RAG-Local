# Learning RAG with TypeScript

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that enhances Large Language Models (LLMs) by providing them with relevant context from your own documents. Think of it as giving the LLM a reference book to look up information before answering questions.

## Core Concepts

### 1. The RAG Pipeline

```typescript
// The three-step RAG process:
async function ragProcess(question: string) {
  // Step 1: Convert question to embedding
  const questionEmbedding = await embed(question);
  
  // Step 2: Find relevant documents
  const relevantDocs = await vectorStore.search(questionEmbedding);
  
  // Step 3: Generate answer with context
  const answer = await llm.generate(
    `Context: ${relevantDocs}
     Question: ${question}
     Answer:`
  );
  
  return answer;
}
```

### 2. Embeddings

Embeddings are numerical representations of text that capture semantic meaning:

```typescript
// Text to vector conversion
const text = "TypeScript is a typed superset of JavaScript";
const embedding = await ollama.embed(text);
// Result: [0.123, -0.456, 0.789, ...] (768 dimensions)
```

**Key Properties:**
- Similar texts have similar embeddings
- Can be compared using cosine similarity
- Enable semantic search beyond keyword matching

### 3. Vector Storage

Vector stores index and search embeddings efficiently:

```typescript
interface VectorStore {
  // Store document with its embedding
  addDocument(doc: Document): Promise<void>;
  
  // Find k most similar documents
  search(query: number[], k: number): Promise<Document[]>;
}
```

**Our Implementation:**
- In-memory storage for simplicity
- Cosine similarity for matching
- Can be extended to persistent databases

### 4. Text Chunking

Large documents are split into manageable chunks:

```typescript
const chunker = new TextChunker({
  chunkSize: 500,      // Characters per chunk
  chunkOverlap: 50     // Overlap between chunks
});

const chunks = chunker.chunk(longDocument);
```

**Why Chunk?**
- LLMs have token limits
- Smaller chunks = more precise retrieval
- Overlap preserves context at boundaries

### 5. Local LLMs with Ollama

Ollama runs LLMs locally on your machine:

```typescript
const ollama = new OllamaClient({
  model: "tinyllama:latest"
});

// Generate text
const response = await ollama.generate("Explain TypeScript");

// Create embeddings
const embedding = await ollama.embed("Some text");
```

## TypeScript RAG Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Documents  │────▶│   Chunker    │────▶│  Embeddings │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    Query    │────▶│   Embedding  │────▶│Vector Search│
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Context   │────▶│     LLM      │────▶│   Answer    │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Practical Example

Let's build a simple Q&A system:

```typescript
import { LocalRAGPipeline } from "./rag-pipeline";

async function buildQASystem() {
  const rag = new LocalRAGPipeline();
  
  // Add your knowledge base
  const documents = [
    "TypeScript was created by Microsoft in 2012.",
    "TypeScript adds static typing to JavaScript.",
    "TypeScript compiles to plain JavaScript.",
    "TypeScript supports modern ECMAScript features."
  ];
  
  await rag.addDocuments(documents);
  
  // Ask questions
  const questions = [
    "When was TypeScript created?",
    "What does TypeScript add to JavaScript?",
    "What does TypeScript compile to?"
  ];
  
  for (const question of questions) {
    const result = await rag.query(question);
    console.log(`Q: ${question}`);
    console.log(`A: ${result.answer}\n`);
  }
}
```

## Advanced Concepts

### 1. Hybrid Search

Combine vector search with keyword search:

```typescript
class HybridSearch {
  async search(query: string, k: number) {
    // Semantic search
    const vectorResults = await this.vectorSearch(query);
    
    // Keyword search
    const keywordResults = await this.keywordSearch(query);
    
    // Combine and rerank
    return this.rerank([...vectorResults, ...keywordResults]);
  }
}
```

### 2. Streaming Responses

Stream LLM responses for better UX:

```typescript
async function* streamQuery(question: string) {
  const context = await findContext(question);
  
  const stream = await ollama.generateStream(
    `Context: ${context}\nQuestion: ${question}`
  );
  
  for await (const chunk of stream) {
    yield chunk;
  }
}
```

### 3. Caching Strategies

Cache embeddings to improve performance:

```typescript
class EmbeddingCache {
  private cache = new Map<string, number[]>();
  
  async getEmbedding(text: string): Promise<number[]> {
    const hash = createHash(text);
    
    if (!this.cache.has(hash)) {
      const embedding = await ollama.embed(text);
      this.cache.set(hash, embedding);
    }
    
    return this.cache.get(hash)!;
  }
}
```

### 4. Custom Prompts

Optimize prompts for your use case:

```typescript
const prompts = {
  qa: (context: string, question: string) => `
    Answer based only on the context provided.
    Context: ${context}
    Question: ${question}
    Answer:`,
    
  summary: (text: string) => `
    Summarize the following text concisely:
    ${text}
    Summary:`,
    
  extraction: (text: string, fields: string[]) => `
    Extract these fields from the text:
    Fields: ${fields.join(", ")}
    Text: ${text}
    Extracted data:`
};
```

## Performance Tips

### 1. Batch Processing

Process multiple documents at once:

```typescript
async function batchEmbed(texts: string[]) {
  // Process in batches of 10
  const batchSize = 10;
  const embeddings: number[][] = [];
  
  for (let i = 0; i < texts.length; i += batchSize) {
    const batch = texts.slice(i, i + batchSize);
    const batchEmbeddings = await Promise.all(
      batch.map(text => ollama.embed(text))
    );
    embeddings.push(...batchEmbeddings);
  }
  
  return embeddings;
}
```

### 2. Async Operations

Use async/await effectively:

```typescript
// Good: Parallel processing
const [embeddings, chunks] = await Promise.all([
  embedDocuments(documents),
  chunkDocuments(documents)
]);

// Bad: Sequential processing
const embeddings = await embedDocuments(documents);
const chunks = await chunkDocuments(documents);
```

### 3. Memory Management

Monitor and optimize memory usage:

```typescript
class VectorStore {
  private maxDocuments = 10000;
  
  async addDocument(doc: Document) {
    if (this.documents.length >= this.maxDocuments) {
      // Implement cleanup strategy
      this.removeOldestDocuments(100);
    }
    
    this.documents.push(doc);
  }
}
```

## Testing RAG Systems

### 1. Unit Tests

Test individual components:

```typescript
describe("Chunker", () => {
  it("should split text into chunks", () => {
    const chunker = new TextChunker({ chunkSize: 10 });
    const chunks = chunker.chunk("This is a long text");
    expect(chunks).toHaveLength(2);
  });
});
```

### 2. Integration Tests

Test the full pipeline:

```typescript
describe("RAG Pipeline", () => {
  it("should answer questions", async () => {
    const rag = new LocalRAGPipeline();
    await rag.addDocuments(["TypeScript is great"]);
    
    const result = await rag.query("What is TypeScript?");
    expect(result.answer).toContain("TypeScript");
  });
});
```

### 3. Evaluation Metrics

Measure RAG performance:

```typescript
interface RAGMetrics {
  relevance: number;      // How relevant are retrieved docs
  accuracy: number;       // How accurate are answers
  latency: number;        // Response time
  cost: number;          // Computational cost
}
```

## Common Patterns

### 1. Document Preprocessing

Clean and prepare documents:

```typescript
function preprocessDocument(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, " ")      // Normalize whitespace
    .replace(/[^\w\s]/g, "")   // Remove special chars
    .trim();
}
```

### 2. Context Window Management

Handle LLM token limits:

```typescript
function fitToContext(
  docs: Document[], 
  maxTokens: number = 2000
): string {
  let context = "";
  let tokens = 0;
  
  for (const doc of docs) {
    const docTokens = estimateTokens(doc.text);
    if (tokens + docTokens > maxTokens) break;
    
    context += doc.text + "\n\n";
    tokens += docTokens;
  }
  
  return context;
}
```

### 3. Answer Validation

Validate LLM responses:

```typescript
function validateAnswer(answer: string): boolean {
  // Check for hallucination indicators
  const invalidPhrases = [
    "I don't have information",
    "not mentioned in the context"
  ];
  
  return !invalidPhrases.some(phrase => 
    answer.toLowerCase().includes(phrase)
  );
}
```

## Next Steps

1. **Experiment**: Try different models and parameters
2. **Optimize**: Profile and improve performance
3. **Extend**: Add persistence, caching, or UI
4. **Deploy**: Package as API or desktop app
5. **Share**: Contribute improvements back

## Resources

- [Ollama Models](https://ollama.ai/library)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [Vector Similarity](https://www.pinecone.io/learn/vector-similarity/)

---

Happy learning! 🚀
