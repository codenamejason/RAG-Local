#!/usr/bin/env python3
"""
Quick Start Script for Local RAG System
Run this to see the system in action immediately!
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 60)
    print("🚀 LOCAL RAG SYSTEM - QUICK START DEMO")
    print("=" * 60)
    print()
    
    # Check Ollama
    print("1️⃣ Checking Ollama connection...")
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"   ✅ Ollama is running with {len(models)} models")
            
            # Check for required models
            model_names = [m["name"] for m in models]
            has_embed = any("nomic-embed-text" in m for m in model_names)
            has_llm = any(m for m in model_names if any(llm in m for llm in ["mistral", "llama", "phi"]))
            
            if not has_embed:
                print("   ⚠️  Missing embedding model. Run: ollama pull nomic-embed-text:latest")
                return
            if not has_llm:
                print("   ⚠️  Missing LLM model. Run: ollama pull mistral:latest")
                return
        else:
            raise Exception("Ollama not responding")
    except:
        print("   ❌ Ollama is not running!")
        print("   👉 Start it with: ollama serve")
        return
    
    print()
    print("2️⃣ Initializing Local RAG Pipeline...")
    
    try:
        from src.rag_pipeline_local import LocalRAGPipeline
        
        # Initialize with default settings
        rag = LocalRAGPipeline()
        print("   ✅ Pipeline initialized")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        print("   👉 Run: pip install -r requirements.txt")
        return
    
    print()
    print("3️⃣ Adding sample documents...")
    
    # Sample documents about different topics
    documents = [
        """Python is a high-level, interpreted programming language known for its 
        simplicity and readability. Created by Guido van Rossum and first released 
        in 1991, Python emphasizes code readability with its notable use of 
        significant whitespace. It supports multiple programming paradigms including 
        procedural, object-oriented, and functional programming.""",
        
        """Machine learning is a subset of artificial intelligence that enables 
        systems to learn and improve from experience without being explicitly 
        programmed. It focuses on developing computer programs that can access 
        data and use it to learn for themselves. The process begins with observations 
        or data, such as examples, direct experience, or instruction.""",
        
        """RAG (Retrieval-Augmented Generation) is an AI framework that combines 
        the benefits of retrieval-based and generative AI models. It works by first 
        retrieving relevant information from a knowledge base, then using that 
        context to generate more accurate and informed responses. This approach 
        reduces hallucinations and improves factual accuracy."""
    ]
    
    num_chunks = rag.add_documents(documents)
    print(f"   ✅ Added {len(documents)} documents ({num_chunks} chunks)")
    
    print()
    print("4️⃣ Testing queries...")
    print()
    
    # Test queries
    queries = [
        "What is Python and when was it created?",
        "How does machine learning work?",
        "What are the benefits of RAG?",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 50)
        
        start = time.time()
        response = rag.query(query, top_k=2, max_tokens=150)
        elapsed = time.time() - start
        
        print(f"Answer: {response.answer[:200]}...")
        print(f"Time: {elapsed:.2f}s")
        print(f"Cost: ${response.cost} (Always FREE!)")
        print(f"Sources: {len(response.sources)} documents retrieved")
        print()
    
    print("=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("=" * 60)
    print()
    print("What you just saw:")
    print("  ✅ Documents indexed locally")
    print("  ✅ Embeddings generated locally")
    print("  ✅ Semantic search working")
    print("  ✅ LLM generation working")
    print("  ✅ Zero API calls made")
    print("  ✅ Zero dollars spent")
    print()
    print("Next steps:")
    print("  1. Add your own documents")
    print("  2. Customize the models")
    print("  3. Build your application")
    print()
    print("Check out src/example_usage.py for more examples!")
    
    # Show stats
    print()
    print("System Stats:")
    stats = rag.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
