"""Embeddings module using Voyage AI."""

import os
from typing import List, Optional
import voyageai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class VoyageEmbeddings:
    """Wrapper for Voyage AI embeddings."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "voyage-2"):
        """
        Initialize Voyage AI embeddings.
        
        Args:
            api_key: Voyage AI API key. If None, reads from VOYAGE_API_KEY env var.
            model: Model to use for embeddings (voyage-2, voyage-large-2, etc.)
        """
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Voyage API key not provided. Set VOYAGE_API_KEY environment variable.")
        
        self.client = voyageai.Client(api_key=self.api_key)
        self.model = model
        logger.info(f"Initialized Voyage embeddings with model: {model}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text documents to embed.
            
        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []
        
        logger.debug(f"Embedding {len(texts)} documents")
        
        # Voyage AI can handle batches efficiently
        result = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="document"  # Optimized for document storage
        )
        
        embeddings = result.embeddings
        logger.debug(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query.
        
        Args:
            query: Query text to embed.
            
        Returns:
            Embedding vector for the query.
        """
        logger.debug(f"Embedding query: {query[:100]}...")
        
        result = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="query"  # Optimized for search queries
        )
        
        return result.embeddings[0]
    
    def embed_batch(self, texts: List[str], batch_size: int = 8) -> List[List[float]]:
        """
        Embed texts in batches to handle large datasets.
        
        Args:
            texts: List of texts to embed.
            batch_size: Number of texts to embed at once.
            
        Returns:
            List of embedding vectors.
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embeddings = self.embed_documents(batch)
            all_embeddings.extend(embeddings)
            logger.info(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} documents")
        
        return all_embeddings
