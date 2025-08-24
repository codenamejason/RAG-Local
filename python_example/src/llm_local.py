"""Local LLM using Ollama - ZERO COST alternative to Claude/GPT."""

import os
from typing import List, Dict, Any, Optional
import requests
import logging
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class LocalLLMResponse:
    """Response from local LLM."""
    answer: str
    model_used: str
    tokens_generated: int
    time_taken: float


class OllamaLLM:
    """Local LLM using Ollama - completely free, runs on your hardware.
    
    Recommended models for RAG (in order of quality/speed tradeoff):
    
    1. mixtral:8x7b - Best quality, needs 48GB RAM
    2. llama2:13b - Great quality, needs 16GB RAM  
    3. mistral:7b - Good quality, needs 8GB RAM
    4. tinyllama - Fast & lightweight, needs 2GB RAM (default)
    5. phi-2 - Decent quality, needs 4GB RAM
    6. deepseek-coder:6.7b - For code-heavy RAG
    """
    
    def __init__(
        self,
        model: str = "tinyllama:latest",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        Initialize Ollama LLM.
        
        Args:
            model: Ollama model to use.
            base_url: Ollama API base URL.
            temperature: Generation temperature.
            max_tokens: Maximum tokens to generate.
        """
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Test connection
        self._test_connection()
        
        logger.info(f"Initialized Ollama LLM with model: {model}")
    
    def _test_connection(self):
        """Test if Ollama is running and model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                raise ConnectionError(f"Ollama not responding at {self.base_url}")
            
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if not any(self.model.startswith(m["name"].split(":")[0]) for m in models):
                logger.warning(f"Model {self.model} not found. Available models: {model_names}")
                logger.info(f"Pull the model with: ollama pull {self.model}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Ollama is not running. Start it with: ollama serve\n"
                "Install from: https://ollama.ai"
            )
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> LocalLLMResponse:
        """
        Generate response from local LLM.
        
        Args:
            prompt: User prompt.
            system_prompt: System prompt.
            temperature: Override default temperature.
            max_tokens: Override default max tokens.
            stream: Whether to stream the response.
            
        Returns:
            LocalLLMResponse object.
        """
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        # Format the full prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        else:
            full_prompt = prompt
        
        logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "stream": stream
                },
                stream=stream
            )
            
            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            full_response += chunk["response"]
                            if chunk.get("done", False):
                                return LocalLLMResponse(
                                    answer=full_response,
                                    model_used=self.model,
                                    tokens_generated=chunk.get("eval_count", 0),
                                    time_taken=chunk.get("total_duration", 0) / 1e9
                                )
            else:
                # Handle non-streaming response
                if response.status_code == 200:
                    data = response.json()
                    return LocalLLMResponse(
                        answer=data["response"],
                        model_used=self.model,
                        tokens_generated=data.get("eval_count", 0),
                        time_taken=data.get("total_duration", 0) / 1e9
                    )
                else:
                    logger.error(f"Failed to generate response: {response.text}")
                    return LocalLLMResponse(
                        answer="Error generating response",
                        model_used=self.model,
                        tokens_generated=0,
                        time_taken=0
                    )
                    
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return LocalLLMResponse(
                answer=f"Error: {str(e)}",
                model_used=self.model,
                tokens_generated=0,
                time_taken=0
            )
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> LocalLLMResponse:
        """
        Generate response with RAG context.
        
        Args:
            query: User query.
            context: Retrieved context.
            system_prompt: Optional system prompt.
            
        Returns:
            LocalLLMResponse object.
        """
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant with access to a document knowledge base. 
            Use the provided context to answer questions accurately. 
            If the context doesn't contain relevant information, say so clearly."""
        
        prompt = f"""Based on the following context, please answer this question: {query}

Context:
{context}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information, acknowledge this limitation."""
        
        return self.generate(prompt, system_prompt)


class LlamaCppLLM:
    """Alternative: Use llama.cpp directly for maximum performance.
    
    This gives you more control and better performance than Ollama.
    """
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_threads: int = 4,
        n_gpu_layers: int = 0  # Set > 0 if you have GPU
    ):
        """
        Initialize llama.cpp model.
        
        Args:
            model_path: Path to GGUF model file.
            n_ctx: Context window size.
            n_threads: Number of CPU threads.
            n_gpu_layers: Number of layers to offload to GPU.
        """
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError(
                "llama-cpp-python not installed. Run:\n"
                "pip install llama-cpp-python\n"
                "For GPU support: CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" pip install llama-cpp-python"
            )
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            verbose=False
        )
        
        logger.info(f"Loaded llama.cpp model from {model_path}")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.95
    ) -> LocalLLMResponse:
        """Generate response."""
        import time
        start = time.time()
        
        response = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=False
        )
        
        return LocalLLMResponse(
            answer=response["choices"][0]["text"],
            model_used="llama.cpp",
            tokens_generated=response["usage"]["completion_tokens"],
            time_taken=time.time() - start
        )
