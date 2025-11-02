"""Simple Qdrant client and ingestion package for CSV/Excel files"""

from .client import QdrantVectorClient
from .ingestion import DataIngestion

__all__ = ['QdrantVectorClient', 'DataIngestion']