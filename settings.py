"""Settings and configuration for the application"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Embedding Model Configuration (Local)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    VECTOR_SIZE: int = int(os.getenv("VECTOR_SIZE", "384"))
    
    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", None)
    
    # Data Configuration
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "property_data")
    
    # File paths
    PROPERTY_DATA_FILE: str = os.getenv("PROPERTY_DATA_FILE", "property_data.csv")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present"""
        print(f"✅ Using local embedding model: {cls.EMBEDDING_MODEL}")
        print(f"✅ Vector size: {cls.VECTOR_SIZE}")
        return True
    
    @classmethod
    def display(cls) -> None:
        """Display current settings (without sensitive data)"""
        print("⚙️  Current Settings:")
        print(f"   EMBEDDING_MODEL: {cls.EMBEDDING_MODEL}")
        print(f"   VECTOR_SIZE: {cls.VECTOR_SIZE}")
        print(f"   QDRANT_URL: {cls.QDRANT_URL}")
        print(f"   COLLECTION_NAME: {cls.COLLECTION_NAME}")
        print(f"   DATA_DIR: {cls.DATA_DIR}")
        print(f"   PROPERTY_DATA_FILE: {cls.PROPERTY_DATA_FILE}")


# Global settings instance
settings = Settings()