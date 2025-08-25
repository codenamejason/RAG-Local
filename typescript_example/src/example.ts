/**
 * Example usage of Local RAG
 * Run with: npm run dev
 */

import { LocalRAG } from "./rag-pipeline";

async function main() {
  console.log("=".repeat(60));
  console.log("LOCAL RAG DEMO - 100% Local, Zero Cost");
  console.log("=".repeat(60));

  // Initialize RAG
  const rag = new LocalRAG({
    llmModel: "tinyllama:latest",
    chunkSize: 500,
    chunkOverlap: 50,
  });

  // Check if system is ready
  const ready = await rag.isReady();
  if (!ready) {
    console.error("\n[ERROR] System not ready. Please:");
    console.error("1. Start Ollama: ollama serve");
    console.error("2. Pull models: ollama pull tinyllama && ollama pull nomic-embed-text");
    process.exit(1);
  }

  // Add some documents
  console.log("\n>>> Adding documents to knowledge base...");
  const documents = [
    `TypeScript is a strongly typed programming language that builds on JavaScript. 
     It adds static type definitions, making code more robust and maintainable. 
     TypeScript code compiles to plain JavaScript and runs anywhere JavaScript runs.`,

    `Local RAG systems run entirely on your machine without sending data to cloud services.
     This ensures complete privacy and zero API costs. You own your data and your AI.
     Local models like TinyLlama and Mistral provide good quality at no cost.`,

    `Ollama makes it easy to run large language models locally. It handles model management,
     provides a simple API, and supports many open-source models. With Ollama, you can
     run models like Llama 2, Mistral, and Mixtral on your own hardware.`,
  ];

  const numChunks = await rag.addDocuments(documents);
  console.log(`[OK] Added ${numChunks} chunks`);

  // Query the system
  console.log("\n>>> Querying the RAG system...\n");

  const queries = ["What is TypeScript?", "Why use local RAG?", "How does Ollama help?"];

  for (const query of queries) {
    console.log("-".repeat(60));
    const response = await rag.query(query);

    console.log(`Q: ${query}`);
    console.log(`A: ${response.answer}`);
    console.log(`Sources: ${response.sources.length} chunks used`);
    console.log(`Cost: $${response.totalCost.toFixed(2)} (always free!)\n`);
  }

  // Show stats
  console.log("=".repeat(60));
  console.log("Stats:", rag.getStats());
  console.log("\n[OK] Demo complete! Total cost: $0.00");
}

// Run the demo
main().catch(console.error);
