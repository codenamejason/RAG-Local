/**
 * Text chunking utilities
 */

export interface ChunkOptions {
  chunkSize?: number;
  chunkOverlap?: number;
}

export interface Chunk {
  text: string;
  index: number;
  metadata?: Record<string, any>;
}

export class TextChunker {
  private chunkSize: number;
  private chunkOverlap: number;

  constructor(options: ChunkOptions = {}) {
    this.chunkSize = options.chunkSize || 500;
    this.chunkOverlap = options.chunkOverlap || 50;
  }

  /**
   * Split text into overlapping chunks
   */
  chunk(text: string): Chunk[] {
    const chunks: Chunk[] = [];
    const words = text.split(/\s+/);
    
    for (let i = 0; i < words.length; i += this.chunkSize - this.chunkOverlap) {
      const chunkWords = words.slice(i, i + this.chunkSize);
      if (chunkWords.length > 0) {
        chunks.push({
          text: chunkWords.join(' '),
          index: chunks.length,
          metadata: {
            startIndex: i,
            wordCount: chunkWords.length
          }
        });
      }
      
      // Stop if we've processed all words
      if (i + this.chunkSize >= words.length) break;
    }
    
    return chunks;
  }

  /**
   * Split multiple texts into chunks
   */
  chunkTexts(texts: string[]): Chunk[] {
    const allChunks: Chunk[] = [];
    
    for (let i = 0; i < texts.length; i++) {
      const chunks = this.chunk(texts[i]);
      chunks.forEach(chunk => {
        chunk.metadata = {
          ...chunk.metadata,
          documentIndex: i
        };
        allChunks.push(chunk);
      });
    }
    
    return allChunks;
  }
}
