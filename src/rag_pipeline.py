"""Main RAG pipeline using Anthropic Claude and OpenAI embeddings."""

import os
from typing import List, Dict, Any, Optional, Tuple
import anthropic
from anthropic import Anthropic
import logging
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential

from src.embeddings import OpenAIEmbeddings
from src.vector_store import VectorStore
from src.chunking import TextChunker, MarkdownChunker, Chunk

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    """Response from RAG pipeline."""
    answer: str
    sources: List[Tuple[str, float]]  # (text, relevance_score)
    query: str
    model_used: str
    context_used: str


class RAGPipeline:
    """Complete RAG pipeline with Anthropic and OpenAI."""
    
    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        model: str = "claude-3-haiku-20240307",
        collection_name: str = "rag_documents",
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            anthropic_api_key: Anthropic API key.
            openai_api_key: OpenAI API key.
            model: Claude model to use.
            collection_name: Name for vector store collection.
            chunk_size: Size of text chunks.
            chunk_overlap: Overlap between chunks.
        """
        # API keys
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.anthropic_api_key:
            raise ValueError("Anthropic API key not provided. Set ANTHROPIC_API_KEY.")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY.")
        
        # Initialize components
        self.anthropic = Anthropic(api_key=self.anthropic_api_key)
        self.model = model
        
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        self.vector_store = VectorStore(
            collection_name=collection_name,
            embeddings=self.embeddings
        )
        
        self.text_chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.markdown_chunker = MarkdownChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info(f"Initialized RAG pipeline with model: {model}")
    
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
        
        # Add to vector store
        self.vector_store.add_documents(
            texts=chunk_texts,
            metadatas=chunk_metadatas
        )
        
        logger.info(f"Added {len(all_chunks)} chunks from {len(documents)} documents")
        return len(all_chunks)
    
    def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None,
        document_type: str = "text"
    ) -> int:
        """
        Add a single document to the RAG system.
        
        Args:
            document: Document text.
            metadata: Optional metadata.
            document_type: Type of document.
            
        Returns:
            Number of chunks created.
        """
        return self.add_documents(
            documents=[document],
            metadatas=[metadata] if metadata else None,
            document_type=document_type
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def query(
        self,
        query: str,
        top_k: int = 5,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> RAGResponse:
        """
        Query the RAG system.
        
        Args:
            query: User query.
            top_k: Number of context chunks to retrieve.
            max_tokens: Maximum tokens in response.
            temperature: Generation temperature.
            system_prompt: Optional custom system prompt.
            
        Returns:
            RAGResponse object.
        """
        logger.info(f"Processing query: {query[:100]}...")
        
        # Retrieve relevant context
        search_results = self.vector_store.search(query, top_k=top_k)
        
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
        
        # Prepare system prompt
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant with access to a knowledge base. 
            Use the provided context to answer questions accurately. 
            If the context doesn't contain relevant information, say so clearly.
            Always cite which context section(s) you're using in your answer."""
        
        # Prepare the prompt
        user_prompt = f"""Based on the following context, please answer this question: {query}

Context:
{context}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information, acknowledge this limitation."""
        
        # Generate response using Claude
        logger.info("Generating response with Claude...")
        response = self.anthropic.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        answer = response.content[0].text
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            query=query,
            model_used=self.model,
            context_used=context
        )
    
    def clear_knowledge_base(self):
        """Clear all documents from the knowledge base."""
        self.vector_store.clear()
        logger.info("Knowledge base cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system."""
        stats = {
            "total_documents": self.vector_store.get_document_count(),
            "model": self.model,
            "chunk_size": self.text_chunker.chunk_size,
            "chunk_overlap": self.text_chunker.chunk_overlap,
            "embedding_model": self.embeddings.model,
            "vector_store_type": type(self.vector_store).__name__
        }
        
        # Add vector store specific stats
        if hasattr(self.vector_store, 'get_stats'):
            vector_stats = self.vector_store.get_stats()
            stats.update(vector_stats)
            
        return stats
