"""Test script to verify your local RAG setup is working - ZERO COST!"""

import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_ollama_connection():
    """Test if Ollama is running."""
    import requests
    
    print("Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"[OK] Ollama is running with {len(models)} models installed")
            for model in models:
                print(f"  - {model['name']} ({model['size'] / 1e9:.1f}GB)")
            return True
        else:
            print("[FAIL] Ollama responded but with error")
            return False
    except requests.exceptions.ConnectionError:
        print("[FAIL] Ollama is not running!")
        print("  Fix: Open new PowerShell and run: ollama serve")
        return False

def test_embeddings():
    """Test local embeddings."""
    print("\nTesting local embeddings...")
    
    try:
        from src.embeddings_local import OllamaEmbeddings
        
        embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        
        # Test single embedding
        test_text = "This is a test document about RAG systems."
        start = time.time()
        vector = embeddings.embed_query(test_text)
        elapsed = time.time() - start
        
        print(f"[OK] Embeddings working!")
        print(f"  - Vector dimension: {len(vector)}")
        print(f"  - Time taken: {elapsed:.2f}s")
        print(f"  - Cost: $0.00 (FREE!)")
        
        return True
    except Exception as e:
        print(f"[FAIL] Embedding test failed: {e}")
        return False

def test_llm():
    """Test local LLM generation."""
    print("\nTesting local LLM...")
    
    try:
        from src.llm_local import OllamaLLM
        
        # Try different models in order of preference
        models_to_try = ["mistral", "phi", "llama2", "mistral:7b"]
        llm = None
        
        for model in models_to_try:
            try:
                llm = OllamaLLM(model=model)
                print(f"  Using model: {model}")
                break
            except:
                continue
        
        if not llm:
            print("[FAIL] No LLM models available. Run: ollama pull mistral")
            return False
        
        # Test generation
        start = time.time()
        response = llm.generate(
            prompt="What is RAG in 20 words or less?",
            max_tokens=50
        )
        elapsed = time.time() - start
        
        print(f"[OK] LLM working!")
        print(f"  - Response: {response.answer[:100]}...")
        print(f"  - Tokens generated: {response.tokens_generated}")
        print(f"  - Time taken: {elapsed:.2f}s")
        print(f"  - Cost: $0.00 (FREE!)")
        
        return True
    except Exception as e:
        print(f"[FAIL] LLM test failed: {e}")
        return False

def test_vector_store():
    """Test LanceDB vector store."""
    print("\nTesting LanceDB vector store...")
    
    try:
        from src.vector_store_lancedb import LanceDBVectorStore
        from src.embeddings_local import OllamaEmbeddings
        
        embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
        store = LanceDBVectorStore(
            collection_name="test_collection",
            embeddings=embeddings
        )
        
        # Add test documents
        test_docs = [
            "RAG stands for Retrieval-Augmented Generation.",
            "Vector databases store embeddings for similarity search.",
            "Local models provide privacy and cost savings."
        ]
        
        ids = store.add_documents(test_docs)
        print(f"[OK] Added {len(ids)} documents to vector store")
        
        # Test search
        results = store.search("What is RAG?", top_k=2)
        print(f"[OK] Search returned {len(results)} results")
        
        # Clean up
        store.clear()
        print("[OK] Vector store working!")
        print(f"  - Cost: $0.00 (FREE!)")
        
        return True
    except Exception as e:
        print(f"[FAIL] Vector store test failed: {e}")
        print(f"  You may need to: pip install lancedb pyarrow")
        return False

def test_full_pipeline():
    """Test the complete local RAG pipeline."""
    print("\nTesting complete RAG pipeline...")
    
    try:
        from src.rag_pipeline_local import LocalRAGPipeline
        
        # Initialize pipeline
        print("  Initializing pipeline...")
        rag = LocalRAGPipeline(
            llm_model="mistral",  # or whatever you have
            embedding_model="nomic-embed-text",
            use_sentence_transformers=False  # Use Ollama
        )
        
        # Add test documents
        print("  Adding documents...")
        docs = [
            "Python is a high-level programming language known for its simplicity.",
            "Machine learning models can be trained on local hardware for privacy.",
            "RAG systems combine retrieval with generation for better answers."
        ]
        
        num_chunks = rag.add_documents(docs)
        print(f"  Added {num_chunks} chunks")
        
        # Test query
        print("  Running query...")
        start = time.time()
        response = rag.query("What is Python known for?")
        elapsed = time.time() - start
        
        print(f"[OK] Full pipeline working!")
        print(f"  - Answer: {response.answer[:150]}...")
        print(f"  - Sources found: {len(response.sources)}")
        print(f"  - Time taken: {elapsed:.2f}s")
        print(f"  - Cost: ${response.cost} (ALWAYS ZERO!)")
        
        # Benchmark
        print("\n  Running benchmark...")
        metrics = rag.benchmark()
        print(f"  - Embedding speed: {metrics['embedding_time']:.3f}s")
        print(f"  - Search speed: {metrics['search_time']:.3f}s")
        print(f"  - Generation speed: {metrics['generation_time']:.3f}s")
        print(f"  - Total: {metrics['total_time']:.3f}s")
        
        # Clean up
        rag.clear_knowledge_base()
        
        return True
    except Exception as e:
        print(f"[FAIL] Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_costs():
    """Show cost comparison."""
    print("\n" + "="*60)
    print("COST COMPARISON")
    print("="*60)
    
    queries_per_day = 100
    tokens_per_query = 1000
    days_per_month = 30
    
    # Old costs (OpenAI + Anthropic)
    openai_embedding_cost = 0.00013  # per 1K tokens
    claude_generation_cost = 0.00025  # per 1K tokens (Haiku)
    
    monthly_tokens = queries_per_day * tokens_per_query * days_per_month
    
    old_embedding_cost = (monthly_tokens / 1000) * openai_embedding_cost
    old_generation_cost = (monthly_tokens / 1000) * claude_generation_cost
    old_total = old_embedding_cost + old_generation_cost
    
    print(f"Your OLD setup (OpenAI + Anthropic):")
    print(f"  Embeddings: ${old_embedding_cost:.2f}/month")
    print(f"  Generation: ${old_generation_cost:.2f}/month")
    print(f"  TOTAL: ${old_total:.2f}/month (${old_total * 12:.2f}/year)")
    
    print(f"\nYour NEW setup (Local):")
    print(f"  Embeddings: $0.00/month")
    print(f"  Generation: $0.00/month")
    print(f"  TOTAL: $0.00/month ($0.00/year)")
    
    print(f"\nSAVINGS: ${old_total:.2f}/month (${old_total * 12:.2f}/year)")
    print(f"That's a {100:.0f}% reduction!")

def main():
    """Run all tests."""
    print("="*60)
    print("LOCAL RAG SYSTEM TEST")
    print("="*60)
    
    # Check Ollama first
    if not test_ollama_connection():
        print("\n[WARNING] CRITICAL: Ollama is not running!")
        print("\nTo fix:")
        print("1. Run: .\\install_ollama_windows.ps1")
        print("2. Run: ollama serve (in new window)")
        print("3. Run: .\\setup_ollama_models.ps1")
        print("4. Try this test again")
        return
    
    # Run tests
    tests = [
        ("Embeddings", test_embeddings),
        ("LLM", test_llm),
        ("Vector Store", test_vector_store),
        ("Full Pipeline", test_full_pipeline)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"[FAIL] {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, success in results:
        status = "[OK] PASS" if success else "[FAIL] FAIL"
        print(f"{name:20} {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n*** ALL TESTS PASSED! Your local RAG is ready!")
        compare_costs()
    else:
        print("\n[WARNING] Some tests failed. Check the errors above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install lancedb pyarrow sentence-transformers")
        print("2. Pull models: ollama pull nomic-embed-text && ollama pull mistral")
        print("3. Ensure Ollama is running: ollama serve")

if __name__ == "__main__":
    main()
