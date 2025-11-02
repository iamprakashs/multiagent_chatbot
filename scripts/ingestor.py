import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.processing import DataProcessor
from qdrant.ingestion import DataIngestion
from qdrant.client import QdrantVectorClient
from settings import settings
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logger = logging.getLogger(__name__)
    
    if not settings.validate():
        return
    
    logger.info("Starting property data ingestion")
    
    try:
        logger.info("Processing first 1000 rows of property_data.csv")
        processor = DataProcessor()
        df = processor.prepare_property_data(settings.PROPERTY_DATA_FILE, max_rows=1000)
        dataframe_count = len(df)
        logger.info(f"Processed {dataframe_count} rows from CSV")
        
        logger.info("Ingesting data into Qdrant")
        ingestion = DataIngestion(
            qdrant_url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL,
            vector_size=settings.VECTOR_SIZE
        )
        ingestion.ingest_dataframe(df, text_column='text_content')
        
        logger.info("Ingestion completed successfully")
        
        logger.info("Validating ingestion...")
        client = QdrantVectorClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.COLLECTION_NAME,
            vector_size=settings.VECTOR_SIZE
        )
        collection_count = client.count_documents()
        
        if dataframe_count == collection_count:
            logger.info(f"✅ Validation successful: {dataframe_count} rows processed = {collection_count} documents in collection")
        else:
            logger.warning(f"⚠️ Validation mismatch: {dataframe_count} rows processed ≠ {collection_count} documents in collection")
        
    except FileNotFoundError:
        logger.error(f"File not found: {settings.PROPERTY_DATA_FILE}")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")


if __name__ == "__main__":
    main()