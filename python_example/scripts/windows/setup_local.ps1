# Setup script for local RAG - Windows PowerShell
Write-Host "Setting up LOCAL RAG with ZERO API costs..." -ForegroundColor Green

# Check if Ollama is installed
Write-Host "`nChecking Ollama installation..." -ForegroundColor Yellow
try {
    ollama --version
    Write-Host "✓ Ollama is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama not found. Installing..." -ForegroundColor Red
    Write-Host "Download from: https://ollama.ai/download" -ForegroundColor Cyan
    Start-Process "https://ollama.ai/download"
    Read-Host "Press Enter after installing Ollama"
}

# Start Ollama service
Write-Host "`nStarting Ollama service..." -ForegroundColor Yellow
Start-Process -NoNewWindow ollama serve

# Pull recommended models
Write-Host "`nPulling recommended models..." -ForegroundColor Yellow
Write-Host "This will take a few minutes on first run..." -ForegroundColor Gray

# For embeddings
Write-Host "`n1. Pulling embedding model (nomic-embed-text)..." -ForegroundColor Cyan
ollama pull nomic-embed-text

# For generation - choose based on your RAM
Write-Host "`n2. Choose your LLM based on available RAM:" -ForegroundColor Cyan
Write-Host "  [1] phi-2 (3GB RAM) - Fastest, decent quality" -ForegroundColor White
Write-Host "  [2] mistral:7b (8GB RAM) - Good balance" -ForegroundColor White
Write-Host "  [3] llama2:13b (16GB RAM) - Better quality" -ForegroundColor White
Write-Host "  [4] mixtral:8x7b (48GB RAM) - Best quality" -ForegroundColor White

$choice = Read-Host "Enter choice (1-4)"
switch ($choice) {
    "1" { ollama pull phi }
    "2" { ollama pull mistral }
    "3" { ollama pull llama2:13b }
    "4" { ollama pull mixtral:8x7b }
    default { ollama pull mistral }
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install lancedb pyarrow sentence-transformers

# Optional: Install llama-cpp-python for even more control
Write-Host "`nOptional: Install llama-cpp-python for direct model usage?" -ForegroundColor Yellow
$installLlamaCpp = Read-Host "Install llama-cpp-python? (y/n)"
if ($installLlamaCpp -eq "y") {
    pip install llama-cpp-python
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nYour local RAG is ready with:" -ForegroundColor Cyan
Write-Host "  • LanceDB for vectors (faster than ChromaDB)" -ForegroundColor White
Write-Host "  • Ollama for embeddings and LLM" -ForegroundColor White
Write-Host "  • Smart caching for efficiency" -ForegroundColor White
Write-Host "  • ZERO API costs!" -ForegroundColor Green

Write-Host "`nTo use the local pipeline:" -ForegroundColor Yellow
Write-Host @"
from src.rag_pipeline_local import LocalRAGPipeline

# Initialize
rag = LocalRAGPipeline(
    llm_model="mistral:7b",  # or whatever you pulled
    embedding_model="nomic-embed-text"
)

# Add documents
rag.add_documents(["Your documents here..."])

# Query - ZERO COST!
response = rag.query("Your question")
print(f"Answer: {response.answer}")
print(f"Cost: ${response.cost}")  # Always $0.00!
"@ -ForegroundColor Gray
