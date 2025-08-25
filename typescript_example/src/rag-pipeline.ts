/**
 * Local RAG Pipeline
 * 100% local, zero cost, complete privacy
 */

import { OllamaClient } from './ollama-client';
import { VectorStore, Document } from './vector-store';
import { TextChunker, Chunk } from './chunker';

export interface RAGOptions {
  llmModel?: string;
  embeddingModel?: string;
  chunkSize?: number;
  chunkOverlap?: number;
  baseUrl?: string;
}

export interface RAGResponse {
  answer: string;
  sources: Document[];
  scores: number[];
  totalCost: number; // Always 0 for local!
}

export class LocalRAG {
  private ollama: OllamaClient;
  private vectorStore: VectorStore;
  private chunker: TextChunker;
  private llmModel: string;

  constructor(options: RAGOptions = {}) {
    this.llmModel = options.llmModel || 'tinyllama:latest';
    
    this.ollama = new OllamaClient({
      baseUrl: options.baseUrl,
      model: this.llmModel
    });
    
    this.vectorStore = new VectorStore();
    
    this.chunker = new TextChunker({
      chunkSize: options.chunkSize || 500,
      chunkOverlap: options.chunkOverlap || 50
    });
  }

  /**
   * Check if system is ready
   */
  async isReady(): Promise<boolean> {
    const ollamaRunning = await this.ollama.isRunning();
    if (!ollamaRunning) {
      console.error('[FAIL] Ollama is not running. Start it with: ollama serve');
      return false;
    }

    const models = await this.ollama.listModels();
    const hasLLM = models.some(m => m.includes('llama') || m.includes('mistral'));
    const hasEmbedding = models.some(m => m.includes('nomic-embed'));

    if (!hasLLM) {
      console.error('[FAIL] No LLM model found. Run: ollama pull tinyllama');
      return false;
    }

    if (!hasEmbedding) {
      console.error('[FAIL] No embedding model found. Run: ollama pull nomic-embed-text');
      return false;
    }

    console.log('[OK] System ready with models:', models);
    return true;
  }

  /**
   * Add documents to the knowledge base
   */
  async addDocuments(texts: string[]): Promise<number> {
    console.log(`Adding ${texts.length} documents...`);
    
    // Chunk the texts
    const chunks = this.chunker.chunkTexts(texts);
    console.log(`Created ${chunks.length} chunks`);
    
    // Generate embeddings for each chunk
    const documents: Document[] = [];
    
    for (const chunk of chunks) {
      try {
        const embedding = await this.ollama.embed(chunk.text);
        documents.push({
          id: `doc_${Date.now()}_${chunk.index}`,
          text: chunk.text,
          embedding,
          metadata: chunk.metadata
        });
      } catch (error) {
        console.error(`Failed to embed chunk ${chunk.index}:`, error);
      }
    }
    
    // Add to vector store
    this.vectorStore.addDocuments(documents);
    console.log(`[OK] Added ${documents.length} documents to vector store`);
    
    return documents.length;
  }

  /**
   * Query the RAG system
   */
  async query(question: string, topK: number = 3): Promise<RAGResponse> {
    console.log(`Query: ${question}`);
    
    // Generate embedding for the question
    const queryEmbedding = await this.ollama.embed(question);
    
    // Search for relevant documents
    const searchResults = this.vectorStore.search(queryEmbedding, topK);
    console.log(`Found ${searchResults.length} relevant documents`);
    
    // Build context from search results
    const context = searchResults
      .map(r => r.document.text)
      .join('\n\n');
    
    // Generate answer using LLM
    const prompt = `Based on the following context, answer the question.
    
Context:
${context}

Question: ${question}

Answer:`;

    const answer = await this.ollama.generate(prompt);
    
    return {
      answer,
      sources: searchResults.map(r => r.document),
      scores: searchResults.map(r => r.score),
      totalCost: 0.00 // Always free!
    };
  }

  /**
   * Clear the knowledge base
   */
  clear(): void {
    this.vectorStore.clear();
    console.log('[OK] Knowledge base cleared');
  }

  /**
   * Get statistics
   */
  getStats(): Record<string, any> {
    return {
      documentCount: this.vectorStore.count(),
      model: this.llmModel,
      cost: '$0.00',
      status: 'ready'
    };
  }
}
