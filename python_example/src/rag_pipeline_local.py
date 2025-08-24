"""Local RAG pipeline - ZERO COST, runs entirely on your machine."""

import os
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
import time

try:
    # When run as part of package
    from src.embeddings_local import OllamaEmbeddings, SentenceTransformerEmbeddings
    from src.vector_store_lancedb import LanceDBVectorStore
    from src.llm_local import OllamaLLM, LocalLLMResponse
    from src.chunking import TextChunker, MarkdownChunker, Chunk
except ImportError:
    # When imported from tests
    from embeddings_local import OllamaEmbeddings, SentenceTransformerEmbeddings
    from vector_store_lancedb import LanceDBVectorStore
    from llm_local import OllamaLLM, LocalLLMResponse
    from chunking import TextChunker, MarkdownChunker, Chunk

logger = logging.getLogger(__name__)


@dataclass
class LocalRAGResponse:
    """Response from local RAG pipeline."""
    answer: str
    sources: List[Tuple[str, float]]  # (text, relevance_score)
    query: str
    model_used: str
    context_used: str
    time_taken: float
    cost: float = 0.0  # Always zero for local!


class LocalRAGPipeline:
    """Complete local RAG pipeline - ZERO API costs.
    
    This is what you should be using on a tight budget:
    - LanceDB for vectors (faster than ChromaDB)
    - Ollama or SentenceTransformers for embeddings
    - Ollama for LLM generation
    - Smart caching to avoid recomputation
    - Hybrid search for better results
    """
    
    def __init__(
        self,
        llm_model: str = "tinyllama:latest",
        embedding_model: str = "nomic-embed-text:latest",
        collection_name: str = "local_rag_documents",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        use_sentence_transformers: bool = False
    ):
        """
        Initialize local RAG pipeline.
        
        Args:
            llm_model: Ollama model for generation.
            embedding_model: Model for embeddings.
            collection_name: Name for vector store collection.
            chunk_size: Size of text chunks.
            chunk_overlap: Overlap between chunks.
            use_sentence_transformers: Use ST instead of Ollama for embeddings.
        """
        # Initialize embeddings
        if use_sentence_transformers:
            self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
            embedding_dim = 384  # for all-MiniLM-L6-v2
        else:
            self.embeddings = OllamaEmbeddings(model=embedding_model)
            embedding_dim = 768  # for nomic-embed-text
        
        # Initialize vector store with LanceDB
        self.vector_store = LanceDBVectorStore(
            collection_name=collection_name,
            embeddings=self.embeddings,
            embedding_dim=embedding_dim
        )
        
        # Initialize local LLM
        self.llm = OllamaLLM(model=llm_model)
        
        # Initialize chunkers
        self.text_chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.markdown_chunker = MarkdownChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info(f"Initialized LOCAL RAG pipeline - ZERO COST!")
        logger.info(f"LLM: {llm_model}, Embeddings: {embedding_model}")
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        document_type: str = "text"
    ) -> int:
        """
        Add documents to the RAG system.
        
        Args:
            documents: List of document texts.
            metadatas: Optional metadata for each document.
            document_type: Type of documents ('text' or 'markdown').
            
        Returns:
            Number of chunks created.
        """
        if not documents:
            return 0
        
        metadatas = metadatas or [{} for _ in documents]
        all_chunks = []
        
        # Choose appropriate chunker
        chunker = self.markdown_chunker if document_type == "markdown" else self.text_chunker
        
        # Process each document
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            logger.info(f"Processing document {i+1}/{len(documents)}")
            
            # Add document metadata
            doc_metadata = {
                **meta,
                "document_index": i,
                "document_type": document_type
            }
            
            # Chunk the document
            chunks = chunker.chunk_text(doc, doc_metadata)
            all_chunks.extend(chunks)
        
        # Extract texts and metadata from chunks
        chunk_texts = [chunk.text for chunk in all_chunks]
        chunk_metadatas = [chunk.metadata for chunk in all_chunks]
        
        # Add to vector store (embeddings are cached!)
        self.vector_store.add_documents(
            texts=chunk_texts,
            metadatas=chunk_metadatas
        )
        
        logger.info(f"Added {len(all_chunks)} chunks from {len(documents)} documents")
        return len(all_chunks)
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        use_hybrid_search: bool = True
    ) -> LocalRAGResponse:
        """
        Query the RAG system - completely local, zero cost.
        
        Args:
            query: User query.
            top_k: Number of context chunks to retrieve.
            max_tokens: Maximum tokens in response.
            temperature: Generation temperature.
            system_prompt: Optional custom system prompt.
            use_hybrid_search: Use both vector and keyword search.
            
        Returns:
            LocalRAGResponse object.
        """
        start_time = time.time()
        logger.info(f"Processing query locally: {query[:100]}...")
        
        # Retrieve relevant context with hybrid search
        search_results = self.vector_store.search(
            query, 
            top_k=top_k,
            hybrid_search=use_hybrid_search
        )
        
        if not search_results:
            logger.warning("No relevant context found")
            context = "No relevant context found in the knowledge base."
            sources = []
        else:
            # Format context from search results
            context_parts = []
            sources = []
            
            for i, (doc, score, meta) in enumerate(search_results, 1):
                context_parts.append(f"[Context {i}]\n{doc}")
                sources.append((doc[:200] + "..." if len(doc) > 200 else doc, score))
            
            context = "\n\n".join(context_parts)
        
        # Generate response using local LLM
        logger.info("Generating response with local LLM...")
        llm_response = self.llm.generate_with_context(
            query=query,
            context=context,
            system_prompt=system_prompt
        )
        
        total_time = time.time() - start_time
        
        return LocalRAGResponse(
            answer=llm_response.answer,
            sources=sources,
            query=query,
            model_used=llm_response.model_used,
            context_used=context,
            time_taken=total_time,
            cost=0.0  # ZERO COST!
        )
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base."""
        self.vector_store.clear()
        logger.info("Knowledge base cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        stats = {
            "total_documents": self.vector_store.get_document_count(),
            "llm_model": self.llm.model,
            "embedding_model": self.embeddings.model if hasattr(self.embeddings, 'model') else "sentence-transformers",
            "chunk_size": self.text_chunker.chunk_size,
            "chunk_overlap": self.text_chunker.chunk_overlap,
            "vector_store_type": "LanceDB",
            "cost_per_query": 0.0,
            "api_keys_required": 0,
            "fully_local": True
        }
        
        return stats
    
    def optimize_for_performance(self):
        """Optimize the pipeline for better performance."""
        # Create ANN index in LanceDB for faster search
        self.vector_store.create_index(metric="L2", nprobes=20)
        logger.info("Created ANN index for faster search")
    
    def benchmark(self, test_query: str = "What is this document about?") -> Dict[str, float]:
        """
        Benchmark the local pipeline performance.
        
        Args:
            test_query: Query to test with.
            
        Returns:
            Performance metrics.
        """
        import time
        
        # Test embedding speed
        start = time.time()
        self.embeddings.embed_query(test_query)
        embed_time = time.time() - start
        
        # Test search speed
        start = time.time()
        results = self.vector_store.search(test_query, top_k=5)
        search_time = time.time() - start
        
        # Test generation speed
        start = time.time()
        self.llm.generate("Test prompt", max_tokens=100)
        gen_time = time.time() - start
        
        return {
            "embedding_time": embed_time,
            "search_time": search_time,
            "generation_time": gen_time,
            "total_time": embed_time + search_time + gen_time,
            "cost": 0.0
        }
