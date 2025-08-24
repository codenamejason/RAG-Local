"""LanceDB vector store for local, zero-cost RAG with superior performance."""

import os
from typing import List, Dict, Any, Optional, Tuple
import lancedb
import pyarrow as pa
import numpy as np
from pathlib import Path
import logging
import uuid

logger = logging.getLogger(__name__)


class LanceDBVectorStore:
    """LanceDB-based vector store for high-performance local RAG.
    
    Why LanceDB over ChromaDB:
    - Zero-copy data access (10x faster for large datasets)
    - Native vector + full-text search
    - Serverless/embedded with no dependencies
    - Automatic versioning and time-travel
    - Production-grade performance on local hardware
    """
    
    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: Optional[str] = None,
        embeddings: Optional[Any] = None,
        embedding_dim: int = 384  # For all-MiniLM-L6-v2
    ):
        """
        Initialize LanceDB vector store.
        
        Args:
            collection_name: Name of the collection/table.
            persist_directory: Directory to persist the database.
            embeddings: Embeddings instance (will be Ollama).
            embedding_dim: Dimension of embeddings.
        """
        self.embeddings = embeddings
        self.embedding_dim = embedding_dim
        self.collection_name = collection_name
        
        # Set up persistence directory
        if persist_directory is None:
            persist_directory = str(Path(__file__).parent.parent / "data" / "lancedb")
        
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize LanceDB connection
        self.db = lancedb.connect(persist_directory)
        
        # Store table name for lazy initialization
        self.collection_name = collection_name
        self.table = None
    
    def _ensure_table(self):
        """Ensure table exists, creating if necessary."""
        if self.table is None:
            if self.collection_name in self.db.table_names():
                self.table = self.db.open_table(self.collection_name)
                logger.info(f"Opened existing LanceDB table: {self.collection_name}")
            # Table will be created on first add
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store with batched processing.
        
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
        
        # Prepare metadata
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Batch processing for efficiency
        batch_size = 100
        all_ids = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]
            
            # Generate embeddings for batch
            if self.embeddings:
                logger.info(f"Generating embeddings for batch {i//batch_size + 1}...")
                embeddings = self.embeddings.embed_documents(batch_texts)
            else:
                # Fallback: create fixed-size embeddings
                embeddings = [[0.0] * self.embedding_dim for _ in batch_texts]
            
            # Prepare data for insertion
            import json
            import pandas as pd
            from datetime import datetime
            
            data = []
            for text, embedding, metadata, doc_id in zip(
                batch_texts, embeddings, batch_metadatas, batch_ids
            ):
                data.append({
                    "id": doc_id,
                    "text": text,
                    "vector": embedding,
                    "metadata": json.dumps(metadata),
                    "timestamp": datetime.now()
                })
            
            # Create or add to table
            if self.table is None:
                # Create table with first batch of data
                self.table = self.db.create_table(self.collection_name, data)
                logger.info(f"Created new LanceDB table: {self.collection_name}")
            else:
                # Add to existing table
                self.table.add(data)
            
            all_ids.extend(batch_ids)
            
            logger.info(f"Added batch {i//batch_size + 1} ({len(batch_texts)} documents)")
        
        logger.info(f"Added {len(texts)} documents total to LanceDB")
        return all_ids
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
        hybrid_search: bool = True
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Search for similar documents with optional hybrid search.
        
        Args:
            query: Search query.
            top_k: Number of results to return.
            filter_metadata: Optional metadata filter.
            hybrid_search: Use both vector and full-text search.
            
        Returns:
            List of tuples (document, score, metadata).
        """
        # Ensure table exists
        self._ensure_table()
        if self.table is None:
            logger.warning("No documents in vector store")
            return []
        
        # Generate query embedding
        if self.embeddings:
            query_embedding = self.embeddings.embed_query(query)
        else:
            # Fallback: create fixed-size embedding
            query_embedding = [0.0] * self.embedding_dim
        
        # Vector search
        results = self.table.search(query_embedding).limit(top_k * 2 if hybrid_search else top_k)
        
        if filter_metadata:
            # Apply metadata filtering
            import json
            filtered_results = []
            for result in results.to_pandas().itertuples():
                meta = json.loads(result.metadata)
                if all(meta.get(k) == v for k, v in filter_metadata.items()):
                    filtered_results.append(result)
                if len(filtered_results) >= top_k:
                    break
            results = filtered_results
        else:
            results = results.to_pandas().itertuples()
        
        # If hybrid search, also do full-text search and merge
        if hybrid_search:
            # LanceDB supports full-text search natively
            # This would be implemented with tantivy index
            pass  # TODO: Implement when LanceDB adds FTS support
        
        # Format results
        formatted_results = []
        import json
        for result in list(results)[:top_k]:
            score = 1 / (1 + result._distance) if hasattr(result, '_distance') else 0.5
            metadata = json.loads(result.metadata) if hasattr(result, 'metadata') else {}
            formatted_results.append((result.text, score, metadata))
        
        logger.debug(f"Found {len(formatted_results)} results for query")
        return formatted_results
    
    def delete_collection(self):
        """Delete the entire collection."""
        if self.collection_name in self.db.table_names():
            self.db.drop_table(self.collection_name)
            logger.info(f"Deleted LanceDB table: {self.collection_name}")
        self.table = None
    
    def get_document_count(self) -> int:
        """Get the number of documents in the collection."""
        self._ensure_table()
        return len(self.table) if self.table else 0
    
    def clear(self):
        """Clear all documents from the collection."""
        # Drop table if it exists
        if self.collection_name in self.db.table_names():
            self.db.drop_table(self.collection_name)
            logger.info(f"Cleared all documents from {self.collection_name}")
        self.table = None
    
    def create_index(self, metric: str = "L2", nprobes: int = 20):
        """
        Create an ANN index for faster search.
        
        Args:
            metric: Distance metric (L2 or cosine).
            nprobes: Number of probes for IVF index.
        """
        # Create IVF-PQ index for fast ANN search
        self.table.create_index(
            metric=metric,
            num_partitions=256,  # IVF partitions
            num_sub_vectors=96   # PQ sub-vectors
        )
        logger.info(f"Created ANN index with metric={metric}")
