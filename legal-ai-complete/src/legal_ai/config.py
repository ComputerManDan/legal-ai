"""
Configuration management for legal-ai project.
Loads and validates all environment variables.
"""

import logging
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class Config:
    """Centralized configuration class."""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    CONTRACTS_DIR = DATA_DIR / "contracts"
    OUTPUTS_DIR = DATA_DIR / "outputs"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # Create directories if they don't exist
    CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    
    # Generation Parameters
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))
    MAX_OUTPUT_TOKENS: int = int(os.getenv("MAX_OUTPUT_TOKENS", "8192"))
    
    # Embedding Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    EMBEDDING_CACHE_FILE: str = os.getenv("EMBEDDING_CACHE_FILE", "embeddings_cache.pkl")
    EMBEDDING_CACHE_PATH = DATA_DIR / "embeddings" / EMBEDDING_CACHE_FILE
    
    # Retrieval Configuration
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", "2"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    
    # Other Configuration
    JURISDICTION: str = os.getenv("JURISDICTION", "England and Wales")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        Returns True if valid, raises ValueError if not.
        """
        required = ["GEMINI_API_KEY", "GEMINI_MODEL"]
        missing = [var for var in required if not getattr(cls, var, None)]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                f"Please set these in your .env file."
            )
        
        logger.info("Configuration validated successfully")
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Return configuration as dictionary (for logging)."""
        return {
            "GEMINI_MODEL": cls.GEMINI_MODEL,
            "TEMPERATURE": cls.TEMPERATURE,
            "MAX_OUTPUT_TOKENS": cls.MAX_OUTPUT_TOKENS,
            "EMBEDDING_MODEL": cls.EMBEDDING_MODEL,
            "CHUNK_SIZE": cls.CHUNK_SIZE,
            "RETRIEVAL_TOP_K": cls.RETRIEVAL_TOP_K,
            "JURISDICTION": cls.JURISDICTION,
            "DEBUG": cls.DEBUG,
        }


# Export for convenience
config = Config()
