"""Main entry point for the application."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function to run the application."""
    logger.info("Starting RAG application...")
    
    try:
        # Import and run the example
        from src.example_usage import main as run_example
        run_example()
    except Exception as e:
        logger.error(f"Error running application: {e}")
        print("\n" + "="*80)
        print("ERROR: Failed to run RAG example")
        print("="*80)
        print("\nMake sure you have:")
        print("1. Created a .env file with your API keys")
        print("2. Set ANTHROPIC_API_KEY in your .env file")
        print("3. Set VOYAGE_API_KEY in your .env file")
        print("\nYou can get these keys from:")
        print("- Anthropic: https://console.anthropic.com/")
        print("- Voyage AI: https://www.voyageai.com/")
        raise
    
    logger.info("Application finished.")


if __name__ == "__main__":
    main()
