/**
 * Ollama Client - Interface with local Ollama instance
 * Zero cost LLM and embeddings
 */

export interface OllamaOptions {
  baseUrl?: string;
  model?: string;
}

export interface GenerateResponse {
  response: string;
  model: string;
  done: boolean;
  context?: number[];
  total_duration?: number;
  eval_count?: number;
}

export interface EmbeddingResponse {
  embedding: number[];
}

export class OllamaClient {
  private baseUrl: string;
  private model: string;

  constructor(options: OllamaOptions = {}) {
    this.baseUrl = options.baseUrl || "http://localhost:11434";
    this.model = options.model || "tinyllama:latest";
  }

  /**
   * Check if Ollama is running
   */
  async isRunning(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * List available models
   */
  async listModels(): Promise<string[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      const data = (await response.json()) as { models?: { name: string }[] };
      return data.models?.map((m) => m.name) || [];
    } catch {
      return [];
    }
  }

  /**
   * Generate text with LLM
   */
  async generate(prompt: string, options: Record<string, unknown> = {}): Promise<string> {
    const response = await fetch(`${this.baseUrl}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: this.model,
        prompt,
        stream: false,
        ...options,
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama generate failed: ${response.statusText}`);
    }

    const data = (await response.json()) as GenerateResponse;
    return data.response;
  }

  /**
   * Generate embeddings for text
   */
  async embed(text: string): Promise<number[]> {
    const response = await fetch(`${this.baseUrl}/api/embeddings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "nomic-embed-text:latest",
        prompt: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama embed failed: ${response.statusText}`);
    }

    const data = (await response.json()) as EmbeddingResponse;
    return data.embedding;
  }

  /**
   * Generate embeddings for multiple texts
   */
  async embedBatch(texts: string[]): Promise<number[][]> {
    const embeddings = await Promise.all(texts.map((text) => this.embed(text)));
    return embeddings;
  }
}
