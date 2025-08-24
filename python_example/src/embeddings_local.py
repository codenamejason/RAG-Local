"""Local embeddings using Ollama - ZERO COST, runs on your machine."""

import os
from typing import List, Optional
import requests
import numpy as np
import logging
from functools import lru_cache
import hashlib
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class OllamaEmbeddings:
    """Local embeddings using Ollama - completely free, runs on your hardware.
    
    Models to consider:
    - nomic-embed-text (768 dim) - Best quality/size ratio
    - all-minilm (384 dim) - Fastest, good enough for most
    - mxbai-embed-large (1024 dim) - Best quality, slower
    """
    
    def __init__(
        self,
        model: str = "nomic-embed-text:latest",
        base_url: str = "http://localhost:11434",
        cache_dir: Optional[str] = None
    ):
        """
        Initialize Ollama embeddings.
        
        Args:
            model: Ollama model to use for embeddings.
            base_url: Ollama API base URL.
            cache_dir: Directory to cache embeddings (saves recomputation).
        """
        self.model = model
        self.base_url = base_url
        
        # Set up caching to avoid recomputing embeddings
        if cache_dir is None:
            cache_dir = str(Path(__file__).parent.parent / "data" / "embedding_cache")
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        self.cache_dir = cache_dir
        
        # Test connection
        self._test_connection()
        
        logger.info(f"Initialized Ollama embeddings with model: {model}")
    
    def _test_connection(self):
        """Test if Ollama is running and model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                raise ConnectionError(f"Ollama not responding at {self.base_url}")
            
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if self.model not in model_names:
                logger.warning(f"Model {self.model} not found. Available models: {model_names}")
                logger.info(f"Pull the model with: ollama pull {self.model}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Ollama is not running. Start it with: ollama serve\n"
                "Install from: https://ollama.ai"
            )
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.md5(f"{self.model}:{text}".encode()).hexdigest()
    
    def _load_from_cache(self, cache_key: str) -> Optional[List[float]]:
        """Load embedding from cache if exists."""
        cache_file = Path(self.cache_dir) / f"{cache_key}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def _save_to_cache(self, cache_key: str, embedding: List[float]):
        """Save embedding to cache."""
        cache_file = Path(self.cache_dir) / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(embedding, f)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents with caching and batching.
        
        Args:
            texts: List of text documents to embed.
            
        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []
        
        embeddings = []
        uncached_texts = []
        uncached_indices = []
        
        # Check cache first
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text)
            cached = self._load_from_cache(cache_key)
            if cached:
                embeddings.append(cached)
            else:
                embeddings.append(None)  # Placeholder
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # Generate embeddings for uncached texts
        if uncached_texts:
            logger.info(f"Generating {len(uncached_texts)} embeddings (cached: {len(texts) - len(uncached_texts)})")
            
            for text, idx in zip(uncached_texts, uncached_indices):
                try:
                    response = requests.post(
                        f"{self.base_url}/api/embeddings",
                        json={
                            "model": self.model,
                            "prompt": text
                        }
                    )
                    
                    if response.status_code == 200:
                        embedding = response.json()["embedding"]
                        embeddings[idx] = embedding
                        
                        # Cache the result
                        cache_key = self._get_cache_key(text)
                        self._save_to_cache(cache_key, embedding)
                    else:
                        logger.error(f"Failed to generate embedding: {response.text}")
                        # Fallback to zero embedding with correct dimension
                        embeddings[idx] = [0.0] * 768  # nomic-embed-text dimension
                        
                except Exception as e:
                    logger.error(f"Error generating embedding: {e}")
                    embeddings[idx] = [0.0] * 768  # nomic-embed-text dimension
        
        logger.debug(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query with caching.
        
        Args:
            query: Query text to embed.
            
        Returns:
            Embedding vector for the query.
        """
        # Check cache
        cache_key = self._get_cache_key(query)
        cached = self._load_from_cache(cache_key)
        if cached:
            logger.debug(f"Using cached embedding for query")
            return cached
        
        logger.debug(f"Embedding query: {query[:100]}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": query
                }
            )
            
            if response.status_code == 200:
                embedding = response.json()["embedding"]
                # Cache the result
                self._save_to_cache(cache_key, embedding)
                return embedding
            else:
                logger.error(f"Failed to generate query embedding: {response.text}")
                return [0.0] * 768  # nomic-embed-text dimension
                
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return [0.0] * 768  # nomic-embed-text dimension


class SentenceTransformerEmbeddings:
    """Alternative: Use sentence-transformers locally (no Ollama needed).
    
    This is even simpler - pure Python, no external services.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize sentence-transformer embeddings.
        
        Args:
            model_name: HuggingFace model name.
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. Run:\n"
                "pip install sentence-transformers"
            )
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        logger.info(f"Loaded sentence-transformer model: {model_name}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, query: str) -> List[float]:
        """Embed query."""
        embedding = self.model.encode([query], convert_to_numpy=True)[0]
        return embedding.tolist()
