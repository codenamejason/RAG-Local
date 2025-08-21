"""Vector store for semantic search using ChromaDB."""

import os
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
import logging
from pathlib import Path
import uuid

from src.embeddings import VoyageEmbeddings

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for RAG."""
    
    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: Optional[str] = None,
        embeddings: Optional[VoyageEmbeddings] = None
    ):
        """
        Initialize vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection.
            persist_directory: Directory to persist the database.
            embeddings: Embeddings instance to use.
        """
        self.embeddings = embeddings or VoyageEmbeddings()
        
        # Set up persistence directory
        if persist_directory is None:
            persist_directory = str(Path(__file__).parent.parent / "data" / "chroma")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "RAG document collection"}
        )
        
        logger.info(f"Initialized vector store with collection: {collection_name}")
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            texts: List of document texts.
            metadatas: Optional metadata for each document.
            ids: Optional IDs for documents.
            
        Returns:
            List of document IDs.
        """
        if not texts:
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} documents...")
        embeddings = self.embeddings.embed_documents(texts)
        
        # Prepare metadata
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(texts)} documents to vector store")
        return ids
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for similar documents.
        
        Args:
            query: Search query.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
            
        Returns:
            List of tuples (document, score, metadata).
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        # Convert distances to similarity scores (1 - normalized_distance)
        # ChromaDB uses L2 distance by default
        formatted_results = []
        for doc, dist, meta in zip(documents, distances, metadatas):
            score = 1 / (1 + dist)  # Convert distance to similarity
            formatted_results.append((doc, score, meta))
        
        logger.debug(f"Found {len(formatted_results)} results for query")
        return formatted_results
    
    def delete_collection(self):
        """Delete the entire collection."""
        self.client.delete_collection(name=self.collection.name)
        logger.info(f"Deleted collection: {self.collection.name}")
    
    def get_document_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
    
    def clear(self):
        """Clear all documents from the collection."""
        # Get all IDs and delete them
        all_ids = self.collection.get()['ids']
        if all_ids:
            self.collection.delete(ids=all_ids)
            logger.info(f"Cleared {len(all_ids)} documents from collection")
