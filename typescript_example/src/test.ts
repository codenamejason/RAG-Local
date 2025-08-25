/**
 * Test Local RAG System
 * Run with: npm test
 */

import { OllamaClient } from "./ollama-client";
import { VectorStore } from "./vector-store";
import { TextChunker } from "./chunker";
import { LocalRAG } from "./rag-pipeline";

async function testOllama() {
  console.log("\n>>> Testing Ollama Connection...");
  const client = new OllamaClient();

  const running = await client.isRunning();
  if (!running) {
    console.log("[FAIL] Ollama not running");
    return false;
  }

  const models = await client.listModels();
  console.log(`[OK] Ollama running with ${models.length} models`);
  models.forEach((m) => console.log(`  - ${m}`));

  return true;
}

function testVectorStore() {
  console.log("\n>>> Testing Vector Store...");
  const store = new VectorStore();

  // Add test documents
  store.addDocuments([
    { id: "1", text: "Hello world", embedding: [0.1, 0.2, 0.3] },
    { id: "2", text: "Test document", embedding: [0.2, 0.3, 0.4] },
    { id: "3", text: "Another test", embedding: [0.3, 0.4, 0.5] },
  ]);

  // Test search
  const results = store.search([0.15, 0.25, 0.35], 2);

  if (results.length === 2) {
    console.log("[OK] Vector store working");
    console.log(`  Found ${results.length} results`);
    return true;
  } else {
    console.log("[FAIL] Vector store search failed");
    return false;
  }
}

function testChunker() {
  console.log("\n>>> Testing Text Chunker...");
  const chunker = new TextChunker({ chunkSize: 10, chunkOverlap: 2 });

  const text = "This is a test document with multiple words that should be chunked properly";
  const chunks = chunker.chunk(text);

  if (chunks.length > 0) {
    console.log("[OK] Chunker working");
    console.log(`  Created ${chunks.length} chunks`);
    return true;
  } else {
    console.log("[FAIL] Chunker failed");
    return false;
  }
}

async function testRAGPipeline() {
  console.log("\n>>> Testing Full RAG Pipeline...");
  const rag = new LocalRAG();

  const ready = await rag.isReady();
  if (!ready) {
    console.log("[FAIL] RAG system not ready");
    return false;
  }

  // Add a document
  const docs = ["TypeScript is a typed superset of JavaScript"];
  const numChunks = await rag.addDocuments(docs);

  if (numChunks > 0) {
    // Query
    const response = await rag.query("What is TypeScript?");

    if (response.answer && response.totalCost === 0) {
      console.log("[OK] RAG pipeline working");
      console.log(`  Answer: ${response.answer.substring(0, 50)}...`);
      console.log(`  Cost: $${response.totalCost} (FREE!)`);
      return true;
    }
  }

  console.log("[FAIL] RAG pipeline failed");
  return false;
}

async function runAllTests() {
  console.log("=".repeat(60));
  console.log("TYPESCRIPT LOCAL RAG TEST SUITE");
  console.log("=".repeat(60));

  const tests = [
    { name: "Ollama", fn: testOllama },
    { name: "Vector Store", fn: () => Promise.resolve(testVectorStore()) },
    { name: "Chunker", fn: () => Promise.resolve(testChunker()) },
    { name: "RAG Pipeline", fn: testRAGPipeline },
  ];

  const results: boolean[] = [];

  for (const test of tests) {
    try {
      const passed = await test.fn();
      results.push(passed);
    } catch (error) {
      console.log(`[FAIL] ${test.name} threw error:`, error);
      results.push(false);
    }
  }

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("TEST SUMMARY");
  console.log("=".repeat(60));

  const passed = results.filter((r) => r).length;
  const failed = results.filter((r) => !r).length;

  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log("Total Cost: $0.00 (ALWAYS FREE!)");

  if (failed === 0) {
    console.log("\n*** ALL TESTS PASSED! ***");
    console.log("Your TypeScript RAG is ready!");
  } else {
    console.log("\n[WARNING] Some tests failed");
    console.log("Make sure Ollama is running with models installed");
  }

  process.exit(failed === 0 ? 0 : 1);
}

// Run tests
runAllTests().catch(console.error);
