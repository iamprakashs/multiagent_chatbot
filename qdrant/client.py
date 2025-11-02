from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import os


class QdrantParams:
    VECTORIZER: str = "text2vec_openai"


class QdrantVectorClient:
    """Simple Qdrant client for vector search operations"""
    
    def __init__(self, url: str = "http://localhost:6333", api_key: str = None, collection_name: str = "documents", embedding_model: str = "all-MiniLM-L6-v2", vector_size: int = None):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self.model = SentenceTransformer(embedding_model)
        self.vector_size = self.model.get_sentence_embedding_dimension()
        print(f"Initialized with model: {embedding_model}, vector size: {self.vector_size}")
    
    def create_collection(self):
        """Create a new collection with vector configuration"""
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            return True
        except Exception as e:
            print(f"Error creating collection: {e}")
            return False
    
    def get_embeddings(self, text: str) -> List[float]:
        """Convert text to vector embedding using sentence transformers - no fitting needed!"""
        return self.model.encode(text).tolist()
    
    def insert_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100):
        """Insert documents with their embeddings into the collection in batches"""
        total_docs = len(documents)
        print(f"Inserting {total_docs} documents in batches of {batch_size}...")
        
        for i in range(0, total_docs, batch_size):
            batch = documents[i:i + batch_size]
            points = []
            
            for j, doc in enumerate(batch):
                text_content = doc.get('text', '')
                vector = self.get_embeddings(text_content)
                
                point = models.PointStruct(
                    id=i + j,
                    vector=vector,
                    payload=doc
                )
                points.append(point)
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            print(f"Processed batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}")
        
        print(f"Successfully inserted all {total_docs} documents!")
    
    def get_collection_info(self):
        """Get collection information including document count"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status,
                "optimizer_status": info.optimizer_status
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return None
    
    def count_documents(self):
        """Get the number of documents in the collection"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return info.points_count
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar documents based on query"""
        query_vector = self.get_embeddings(query)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        
        return [{"score": hit.score, "data": hit.payload} for hit in results]
    
    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False