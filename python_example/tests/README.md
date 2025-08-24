# Pure Local RAG Tests

This directory contains tests for the 100% local RAG system.

## Test Files

### `test_local_rag.py`
Comprehensive test suite that validates:
- Ollama connectivity
- Local embeddings (Ollama/SentenceTransformers)
- Local LLM generation
- LanceDB vector store operations
- Full RAG pipeline integration
- Performance benchmarks
- Cost verification ($0.00)

### `run_all_tests.py`
Simple test runner that:
- Checks if Ollama is running
- Runs the local RAG tests
- Provides clear pass/fail status
- Shows troubleshooting tips if needed

## Running Tests

### Quick Test
```bash
python tests/run_all_tests.py
```

### Detailed Test
```bash
python tests/test_local_rag.py
```

### With Custom Models
```bash
# Set environment variables
export OLLAMA_LLM_MODEL=mistral:latest
export OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# Run tests
python tests/test_local_rag.py
```

## Expected Output

When all tests pass:
```
[OK] Ollama is running with 2 models installed
[OK] Embeddings working!
[OK] LLM working!
[OK] Vector store working!
[OK] Full pipeline working!

*** ALL TESTS PASSED! Your local RAG is ready! ***

COST COMPARISON:
Your setup: $0.00/month (ALWAYS FREE)
Cloud setup: $13.68/year (SAVED)
```

## Troubleshooting

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Verify it's running
ollama list
```

### Models Not Found
```bash
# Install required models
ollama pull tinyllama
ollama pull nomic-embed-text
```

### Import Errors
```bash
# Activate virtual environment
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
uv pip install -r requirements.txt
```

## Test Coverage

- **Unit Tests**: Each component tested individually
- **Integration Tests**: Full pipeline validation
- **Performance Tests**: Speed benchmarks
- **Cost Tests**: Verifies $0.00 operation

## No API Tests

This is a pure local system. We don't test:
- OpenAI APIs (not needed)
- Anthropic APIs (not needed)
- Any cloud services (not needed)

Everything runs on your machine, costs nothing, and keeps your data private.