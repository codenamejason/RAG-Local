"""Settings for Local RAG System - Python configuration."""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import os

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for dir_path in [DATA_DIR, CONFIG_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class OllamaConfig:
    """Ollama service configuration."""
    base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    llm_model: str = "mistral:7b"
    timeout: int = 30
    
    @property
    def is_available(self) -> bool:
        """Check if Ollama service is running."""
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_installed_models(self) -> List[str]:
        """Get list of installed models."""
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
        except:
            pass
        return []


@dataclass
class LanceDBConfig:
    """LanceDB configuration."""
    data_dir: Path = DATA_DIR / "lancedb"
    embedding_dim: int = 768  # Default for nomic-embed-text
    
    # Index configuration
    index_type: str = "IVF_PQ"
    num_partitions: int = 256
    num_sub_vectors: int = 96
    metric: str = "L2"
    nprobes: int = 20
    
    def __post_init__(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class ChunkingConfig:
    """Document chunking configuration."""
    chunk_size: int = 512
    chunk_overlap: int = 50
    separators: List[str] = None
    
    def __post_init__(self):
        if self.separators is None:
            self.separators = ["\n\n", "\n", ". ", ", ", " "]


@dataclass
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    cache_dir: Path = DATA_DIR / "cache"
    embedding_cache_dir: Path = DATA_DIR / "embedding_cache"
    max_cache_size_mb: int = 1000
    ttl_days: int = 30
    
    def __post_init__(self):
        """Create cache directories."""
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.embedding_cache_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class PerformanceConfig:
    """Performance tuning configuration."""
    batch_size: int = 100
    embedding_batch_size: int = 32
    max_workers: int = 4
    search_timeout: int = 5
    generation_timeout: int = 30


@dataclass
class ModelRecommendations:
    """Model recommendations based on system specs."""
    
    @staticmethod
    def get_recommended_models(ram_gb: float) -> Dict[str, str]:
        """Get recommended models based on available RAM."""
        if ram_gb < 4:
            return {
                "embedding": "all-MiniLM-L6-v2",  # Use sentence-transformers
                "llm": None,  # Too little RAM for local LLM
                "warning": "Less than 4GB RAM - consider cloud APIs"
            }
        elif ram_gb < 8:
            return {
                "embedding": "nomic-embed-text",
                "llm": "phi",
                "description": "Lightweight setup for basic tasks"
            }
        elif ram_gb < 16:
            return {
                "embedding": "nomic-embed-text",
                "llm": "mistral:7b",
                "description": "Balanced setup for most use cases"
            }
        elif ram_gb < 32:
            return {
                "embedding": "nomic-embed-text",
                "llm": "llama2:13b",
                "description": "High quality setup"
            }
        else:
            return {
                "embedding": "mxbai-embed-large",
                "llm": "mixtral:8x7b",
                "description": "Maximum quality setup"
            }
    
    @staticmethod
    def get_system_ram() -> float:
        """Get system RAM in GB."""
        import psutil
        return psutil.virtual_memory().total / (1024**3)


class LocalRAGSettings:
    """Main settings class for Local RAG."""
    
    def __init__(
        self,
        ollama_config: Optional[OllamaConfig] = None,
        lancedb_config: Optional[LanceDBConfig] = None,
        chunking_config: Optional[ChunkingConfig] = None,
        cache_config: Optional[CacheConfig] = None,
        performance_config: Optional[PerformanceConfig] = None
    ):
        self.ollama = ollama_config or OllamaConfig()
        self.lancedb = lancedb_config or LanceDBConfig()
        self.chunking = chunking_config or ChunkingConfig()
        self.cache = cache_config or CacheConfig()
        self.performance = performance_config or PerformanceConfig()
        
        # Auto-detect best models if not specified
        self._auto_configure()
    
    def _auto_configure(self):
        """Auto-configure based on system specs."""
        try:
            ram_gb = ModelRecommendations.get_system_ram()
            recommendations = ModelRecommendations.get_recommended_models(ram_gb)
            
            # Check if recommended models are installed
            installed = self.ollama.get_installed_models()
            
            # Use installed models if available
            for model in installed:
                if "embed" in model.lower():
                    self.ollama.embedding_model = model
                    break
            
            for model in installed:
                if any(llm in model for llm in ["mistral", "llama", "phi", "mixtral"]):
                    self.ollama.llm_model = model
                    break
            
            # Update embedding dimensions based on model
            if "nomic-embed-text" in self.ollama.embedding_model:
                self.lancedb.embedding_dim = 768
            elif "all-MiniLM-L6-v2" in self.ollama.embedding_model:
                self.lancedb.embedding_dim = 384
            elif "mxbai-embed-large" in self.ollama.embedding_model:
                self.lancedb.embedding_dim = 1024
                
        except Exception as e:
            print(f"Auto-configuration failed: {e}")
    
    def validate(self) -> Dict[str, bool]:
        """Validate configuration."""
        return {
            "ollama_available": self.ollama.is_available,
            "models_installed": len(self.ollama.get_installed_models()) > 0,
            "directories_exist": all([
                DATA_DIR.exists(),
                self.lancedb.data_dir.exists(),
                self.cache.cache_dir.exists() if self.cache.enabled else True
            ])
        }
    
    def get_status(self) -> str:
        """Get configuration status."""
        validation = self.validate()
        status = []
        
        status.append("LOCAL RAG CONFIGURATION STATUS")
        status.append("=" * 40)
        
        # Ollama status
        if validation["ollama_available"]:
            status.append(f"[OK] Ollama running at {self.ollama.base_url}")
            models = self.ollama.get_installed_models()
            if models:
                status.append(f"[OK] Models installed: {', '.join(models)}")
            else:
                status.append("[WARN] No models installed")
        else:
            status.append("[FAIL] Ollama not running")
        
        # Configuration
        status.append(f"\nCurrent Configuration:")
        status.append(f"  Embedding: {self.ollama.embedding_model} ({self.lancedb.embedding_dim}d)")
        status.append(f"  LLM: {self.ollama.llm_model}")
        status.append(f"  Vector DB: LanceDB at {self.lancedb.data_dir}")
        status.append(f"  Chunk size: {self.chunking.chunk_size}")
        status.append(f"  Cache: {'Enabled' if self.cache.enabled else 'Disabled'}")
        
        # System info
        try:
            ram_gb = ModelRecommendations.get_system_ram()
            status.append(f"\nSystem RAM: {ram_gb:.1f}GB")
            rec = ModelRecommendations.get_recommended_models(ram_gb)
            if "description" in rec:
                status.append(f"Recommendation: {rec['description']}")
        except:
            pass
        
        return "\n".join(status)


# Default settings instance
settings = LocalRAGSettings()

# Export commonly used configs
OLLAMA_BASE_URL = settings.ollama.base_url
EMBEDDING_MODEL = settings.ollama.embedding_model
LLM_MODEL = settings.ollama.llm_model
CHUNK_SIZE = settings.chunking.chunk_size
CHUNK_OVERLAP = settings.chunking.chunk_overlap

if __name__ == "__main__":
    # Print configuration status when run directly
    print(settings.get_status())
