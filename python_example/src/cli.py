"""Interactive CLI for the RAG system."""

import os
import sys
from pathlib import Path
from typing import Optional
import logging
from dotenv import load_dotenv

from src.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors in CLI
    format="%(message)s"
)

class RAGCLI:
    """Interactive command-line interface for RAG system."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.rag: Optional[RAGPipeline] = None
        self.commands = {
            "help": self.show_help,
            "init": self.init_rag,
            "add": self.add_document,
            "addfile": self.add_file,
            "query": self.query,  
            "ask": self.query,  # alias
            "stats": self.show_stats,
            "clear": self.clear_kb,
            "exit": self.exit_cli,
            "quit": self.exit_cli,  # alias
        }
    
    def run(self):
        """Run the interactive CLI."""
        print("="*60)
        print("🤖 RAG System Interactive CLI")
        print("="*60)
        print("Type 'help' for commands or 'init' to start")
        print("💡 You can also ask questions directly!")
        print()
        
        # Auto-initialize if API keys are available
        if os.getenv("ANTHROPIC_API_KEY") and os.getenv("OPENAI_API_KEY"):
            self.init_rag()
        else:
            print("⚠️  API keys not found. Use 'init' to configure.")
            print("   Required: ANTHROPIC_API_KEY and OPENAI_API_KEY")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                # Check if it's a command first
                if user_input.lower() in self.commands:
                    self.commands[user_input.lower()]("")
                    continue
                
                # Check if it starts with a command
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Execute command if recognized
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    # If no command recognized, treat as a natural language query
                    if self.rag:
                        print("🤔 I'll treat that as a question. Let me search the knowledge base...")
                        self.query(user_input)
                    else:
                        print("❌ RAG system not initialized. Use 'init' first.")
                        print("💡 Or type 'help' to see available commands.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self, args=""):
        """Show available commands."""
        help_text = """
📚 Available Commands:
---------------------
  init          - Initialize RAG system
  add <text>    - Add a document to knowledge base
  addfile <path>- Add document from file
  query <text>  - Query the knowledge base (alias: ask)
  stats         - Show system statistics
  clear         - Clear all documents
  help          - Show this help message
  exit          - Exit the CLI (alias: quit)

💡 Natural Language:
  You can also just type questions directly!
  Examples:
  > What is machine learning?
  > Tell me about RAG systems
  > How does this work?

📁 File Commands:
  > add Machine learning is a subset of AI
  > addfile documents/info.txt
  > query What is RAG?
        """
        print(help_text)
    
    def init_rag(self, args=""):
        """Initialize the RAG system."""
        try:
            print("🔄 Initializing RAG system...")
            
            # Check for API keys
            if not os.getenv("ANTHROPIC_API_KEY"):
                print("❌ ANTHROPIC_API_KEY not found in environment")
                print("   Get it from: https://console.anthropic.com/")
                return
            if not os.getenv("OPENAI_API_KEY"):
                print("❌ OPENAI_API_KEY not found in environment")
                print("   Get it from: https://platform.openai.com/api-keys")
                return
            
            self.rag = RAGPipeline(
                model="claude-3-haiku-20240307",
                collection_name="cli_collection"
            )
            
            stats = self.rag.get_stats()
            print(f"✅ RAG system initialized!")
            print(f"   Model: {stats['model']}")
            print(f"   Documents: {stats['total_documents']}")
            
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
    
    def add_document(self, text: str):
        """Add a document to the knowledge base."""
        if not self.rag:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        if not text:
            print("❌ Please provide text to add. Example: add Your text here")
            return
        
        try:
            chunks = self.rag.add_document(text, metadata={"source": "cli"})
            print(f"✅ Added document ({chunks} chunks created)")
        except Exception as e:
            print(f"❌ Failed to add document: {e}")
    
    def add_file(self, filepath: str):
        """Add document from a file."""
        if not self.rag:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        if not filepath:
            print("❌ Please provide a file path. Example: addfile document.txt")
            return
        
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"❌ File not found: {filepath}")
                return
            
            text = path.read_text(encoding='utf-8')
            doc_type = "markdown" if path.suffix in ['.md', '.markdown'] else "text"
            
            chunks = self.rag.add_document(
                text,
                metadata={"source": "file", "filename": path.name},
                document_type=doc_type
            )
            
            print(f"✅ Added {path.name} ({chunks} chunks created)")
            
        except Exception as e:
            print(f"❌ Failed to add file: {e}")
    
    def query(self, question: str):
        """Query the knowledge base."""
        if not self.rag:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        if not question:
            print("❌ Please provide a question. Example: query What is RAG?")
            return
        
        try:
            print("🔍 Searching knowledge base...")
            response = self.rag.query(question, top_k=3)
            
            print("\n" + "="*60)
            print("💬 Answer:")
            print("="*60)
            print(response.answer)
            
            if response.sources:
                print("\n📚 Sources:")
                for i, (source, score) in enumerate(response.sources, 1):
                    preview = source[:100] + "..." if len(source) > 100 else source
                    print(f"  {i}. [{score:.2f}] {preview}")
                    
        except Exception as e:
            print(f"❌ Query failed: {e}")
    
    def show_stats(self, args=""):
        """Show system statistics."""
        if not self.rag:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        stats = self.rag.get_stats()
        print("\n📊 System Statistics:")
        print("-" * 30)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    def clear_kb(self, args=""):
        """Clear the knowledge base."""
        if not self.rag:
            print("❌ RAG system not initialized. Use 'init' first.")
            return
        
        confirm = input("⚠️  Clear all documents? (y/n): ").lower()
        if confirm == 'y':
            self.rag.clear_knowledge_base()
            print("✅ Knowledge base cleared")
        else:
            print("❌ Cancelled")
    
    def exit_cli(self, args=""):
        """Exit the CLI."""
        print("👋 Goodbye!")
        sys.exit(0)


def main():
    """Entry point for the CLI."""
    cli = RAGCLI()
    cli.run()


if __name__ == "__main__":
    main()
