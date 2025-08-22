"""Embeddings module using OpenAI."""

import os
from typing import List, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

class OpenAIEmbeddings:
    """Wrapper for OpenAI embeddings."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        """
        Initialize OpenAI embeddings.
        
        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.
            model: Model to use for embeddings (text-embedding-3-small, text-embedding-3-small, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        logger.info(f"Initialized OpenAI embeddings with model: {model}")
    
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
        
        # OpenAI can handle batches efficiently
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        
        embeddings = [data.embedding for data in response.data]
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
        
        response = self.client.embeddings.create(
            input=[query],
            model=self.model
        )
        
        return response.data[0].embedding
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Embed texts in batches to handle large datasets.
        
        Args:
            texts: List of texts to embed.
            batch_size: Number of texts to embed at once (OpenAI allows up to 2048).
            
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
