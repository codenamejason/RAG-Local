"""Example usage of the RAG pipeline."""

import os
from pathlib import Path
import logging
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Demonstrate RAG pipeline usage."""
    
    # Initialize RAG pipeline
    logger.info("Initializing RAG pipeline...")
    rag = RAGPipeline(
        model="claude-3-haiku-20240307",  # Fast and cost-effective
        chunk_size=512,
        chunk_overlap=50
    )
    
    # Clear any existing data (for demo purposes)
    rag.clear_knowledge_base()
    
    # Example documents about AI and ML
    documents = [
        """
        # Introduction to Machine Learning
        
        Machine learning is a subset of artificial intelligence (AI) that provides systems 
        the ability to automatically learn and improve from experience without being 
        explicitly programmed. Machine learning focuses on the development of computer 
        programs that can access data and use it to learn for themselves.
        
        ## Types of Machine Learning
        
        There are three main types of machine learning:
        
        1. **Supervised Learning**: The algorithm learns from labeled training data, 
        helping you predict outcomes for unforeseen data. Examples include classification 
        and regression problems.
        
        2. **Unsupervised Learning**: The algorithm learns from unlabeled data and finds 
        hidden patterns or intrinsic structures in input data. Examples include clustering 
        and dimensionality reduction.
        
        3. **Reinforcement Learning**: The algorithm learns by interacting with an 
        environment, receiving rewards or penalties based on its actions. It's commonly 
        used in robotics, gaming, and navigation.
        """,
        
        """
        # Neural Networks and Deep Learning
        
        Neural networks are a set of algorithms, modeled loosely after the human brain, 
        that are designed to recognize patterns. They interpret sensory data through a 
        kind of machine perception, labeling or clustering raw input.
        
        ## Architecture of Neural Networks
        
        A typical neural network consists of:
        
        - **Input Layer**: Receives the initial data for processing
        - **Hidden Layers**: Perform computations and feature extraction
        - **Output Layer**: Produces the final prediction or classification
        
        Deep learning refers to neural networks with multiple hidden layers. These deep 
        neural networks have revolutionized fields like computer vision, natural language 
        processing, and speech recognition.
        
        ## Applications
        
        Deep learning powers many modern AI applications:
        - Image and video recognition
        - Natural language processing and translation
        - Autonomous vehicles
        - Medical diagnosis
        - Game playing (like AlphaGo)
        """,
        
        """
        # Retrieval-Augmented Generation (RAG)
        
        RAG is an AI framework that combines the power of retrieval-based and generative 
        AI models. It enhances the capabilities of large language models by providing them 
        with access to external knowledge sources.
        
        ## How RAG Works
        
        The RAG process involves several steps:
        
        1. **Document Processing**: External documents are chunked and embedded into vectors
        2. **Storage**: Vector embeddings are stored in a vector database
        3. **Retrieval**: When a query comes in, relevant documents are retrieved based on 
           semantic similarity
        4. **Augmentation**: Retrieved context is combined with the original query
        5. **Generation**: An LLM generates a response using both the query and context
        
        ## Benefits of RAG
        
        - **Reduced Hallucinations**: By grounding responses in retrieved documents
        - **Up-to-date Information**: Can access information beyond the LLM's training cutoff
        - **Domain Specificity**: Can be specialized for specific domains or organizations
        - **Transparency**: Sources can be cited for verification
        
        RAG is particularly useful for enterprise applications where accuracy and 
        reliability are crucial.
        """
    ]
    
    # Add documents to the knowledge base
    logger.info("Adding documents to knowledge base...")
    num_chunks = rag.add_documents(
        documents=documents,
        metadatas=[
            {"title": "Introduction to Machine Learning", "category": "ML Basics"},
            {"title": "Neural Networks and Deep Learning", "category": "Deep Learning"},
            {"title": "Retrieval-Augmented Generation", "category": "RAG"}
        ],
        document_type="markdown"
    )
    
    logger.info(f"Added {num_chunks} chunks to the knowledge base")
    
    # Example queries
    queries = [
        "What are the three main types of machine learning?",
        "How does RAG help reduce hallucinations in LLMs?",
        "What are the components of a neural network architecture?",
        "What is reinforcement learning and where is it used?",
        "Explain the process of how RAG works step by step."
    ]
    
    # Process each query
    for query in queries:
        print("\n" + "="*80)
        print(f"QUERY: {query}")
        print("="*80)
        
        # Get response
        response = rag.query(query, top_k=3)
        
        print(f"\nANSWER:\n{response.answer}")
        
        print(f"\nSOURCES (Top {len(response.sources)}):")
        for i, (source, score) in enumerate(response.sources, 1):
            print(f"{i}. [Score: {score:.3f}] {source}")
    
    # Print statistics
    print("\n" + "="*80)
    print("RAG SYSTEM STATISTICS")
    print("="*80)
    stats = rag.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
