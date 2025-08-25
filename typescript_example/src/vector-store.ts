/**
 * Simple in-memory vector store
 * For production, use VectorDB or LanceDB
 */

export interface Document {
  id: string;
  text: string;
  embedding?: number[];
  metadata?: Record<string, any>;
}

export interface SearchResult {
  document: Document;
  score: number;
}

export class VectorStore {
  private documents: Document[] = [];

  /**
   * Add documents to the store
   */
  addDocuments(docs: Document[]): void {
    this.documents.push(...docs);
  }

  /**
   * Clear all documents
   */
  clear(): void {
    this.documents = [];
  }

  /**
   * Get document count
   */
  count(): number {
    return this.documents.length;
  }

  /**
   * Calculate cosine similarity between two vectors
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    if (a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  /**
   * Search for similar documents
   */
  search(queryEmbedding: number[], topK: number = 5): SearchResult[] {
    const results: SearchResult[] = [];
    
    for (const doc of this.documents) {
      if (!doc.embedding) continue;
      
      const score = this.cosineSimilarity(queryEmbedding, doc.embedding);
      results.push({ document: doc, score });
    }
    
    // Sort by score descending and take top K
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }

  /**
   * Get all documents
   */
  getAllDocuments(): Document[] {
    return this.documents;
  }
}
