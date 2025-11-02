import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Any
from .client import QdrantVectorClient


class DataIngestion:
    """Simple data ingestion class for CSV/Excel files"""
    
    def __init__(self, qdrant_url: str = "http://localhost:6333", api_key: str = None, collection_name: str = "documents", embedding_model: str = "all-MiniLM-L6-v2", vector_size: int = None):
        self.client = QdrantVectorClient(url=qdrant_url, api_key=api_key, collection_name=collection_name, embedding_model=embedding_model, vector_size=vector_size)
        self.supported_formats = ['.csv', '.xlsx', '.xls']
    
    def load_file(self, file_path: str, text_column: str = 'text') -> List[Dict[str, Any]]:
        """Load data from CSV or Excel file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format. Supported: {self.supported_formats}")
        
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in file")
        
        documents = []
        for idx, row in df.iterrows():
            doc = {
                'text': str(row[text_column]),
                'id': idx,
                'source_file': str(file_path),
            }
            
            for col in df.columns:
                if col != text_column:
                    doc[col] = row[col]
            
            documents.append(doc)
        
        return documents
    
    def ingest_dataframe(self, df: pd.DataFrame, text_column: str = 'text_content', recreate_collection: bool = True):
        """Ingest DataFrame directly into Qdrant"""
        documents = []
        for idx, row in df.iterrows():
            doc = {
                'text': str(row[text_column]),
                'id': idx,
                'metadata': {}
            }
            
            for col in df.columns:
                if col != text_column:
                    doc['metadata'][col] = row[col]
            
            documents.append(doc)
        
        if recreate_collection:
            self.client.create_collection()
        
        self.client.insert_documents(documents)
        print(f"Successfully ingested {len(documents)} documents from DataFrame")
    
    def ingest_multiple_files(self, file_paths: List[str], text_column: str = 'text', recreate_collection: bool = True):
        """Ingest data from multiple files"""
        all_documents = []
        
        for file_path in file_paths:
            documents = self.load_file(file_path, text_column)
            all_documents.extend(documents)
        
        if recreate_collection:
            self.client.create_collection()
        
        self.client.insert_documents(all_documents)
        print(f"Successfully ingested {len(all_documents)} documents from {len(file_paths)} files")
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar documents"""
        return self.client.search(query, limit)