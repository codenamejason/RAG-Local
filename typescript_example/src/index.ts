/**
 * Local RAG for TypeScript
 * 100% local, zero cost, complete privacy
 */

export { LocalRAG, RAGOptions, RAGResponse } from "./rag-pipeline";
export { OllamaClient, OllamaOptions } from "./ollama-client";
export { VectorStore, Document, SearchResult } from "./vector-store";
export { TextChunker, Chunk, ChunkOptions } from "./chunker";

// Re-export as default
import { LocalRAG } from "./rag-pipeline";
export default LocalRAG;
