#!/usr/bin/env python3
"""
Test runner for the pure local RAG system.
100% local, zero-cost operation with Ollama + LanceDB.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def check_environment():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, len(models)
    except:
        return False, 0
    return False, 0


def main():
    """Main test runner for pure local RAG."""
    print("=" * 60)
    print(">>> PURE LOCAL RAG TEST RUNNER")
    print(">>> 100% Local | Zero Cost | No API Keys Required")
    print("=" * 60)
    
    # Check environment
    print("\n=== Environment Check:")
    ollama_running, model_count = check_environment()
    
    if ollama_running:
        print(f"  [OK] Ollama is running with {model_count} models")
    else:
        print("  [FAIL] Ollama is not running")
        print("\n  To start Ollama:")
        print("  1. Windows: Run 'ollama serve' in a terminal")
        print("  2. Mac/Linux: Run 'ollama serve' in a terminal")
        print("\n  To install models:")
        print("  - ollama pull tinyllama      # Fast, lightweight (637MB)")
        print("  - ollama pull nomic-embed-text  # Embeddings (274MB)")
        return 1
    
    # Run the local test
    print("\n" + "=" * 60)
    print(">>> Running Local RAG Tests")
    print("=" * 60)
    
    test_file = Path(__file__).parent / "test_local_rag.py"
    
    if not test_file.exists():
        print(f"[ERROR] Test file not found: {test_file}")
        return 1
    
    start_time = time.time()
    
    # Run the test with proper encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [sys.executable, str(test_file)],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env=env
    )
    
    duration = time.time() - start_time
    
    # Print the output
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    # Check if tests passed
    output = result.stdout + result.stderr
    all_passed = "ALL TESTS PASSED" in output
    
    # Print summary
    print("\n" + "=" * 60)
    print("=== TEST SUMMARY")
    print("=" * 60)
    
    if all_passed:
        print(f"[OK] All tests passed in {duration:.1f}s")
        print("[OK] Your local RAG is ready!")
        print("[OK] Total cost: $0.00 (ALWAYS FREE)")
        print("\n>>> Next steps:")
        print("  1. Add your documents: rag.add_documents(['your_text.txt'])")
        print("  2. Query your knowledge: rag.query('Your question?')")
        print("  3. Save money: You're already doing it!")
        return 0
    else:
        print(f"[FAIL] Some tests failed after {duration:.1f}s")
        print("\n>>> Troubleshooting:")
        print("  1. Check Ollama is running: ollama list")
        print("  2. Install required models:")
        print("     - ollama pull tinyllama")
        print("     - ollama pull nomic-embed-text")
        print("  3. Install Python deps: uv pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())