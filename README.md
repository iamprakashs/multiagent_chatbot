# Multiagent Qdrant Vector Database

A property data ingestion system using Qdrant vector database with TF-IDF embeddings.

## Features

- 🏠 Property data processing and ingestion
- 🔍 Vector-based similarity search
- ⚡ Lightweight TF-IDF embeddings (no heavy ML dependencies)
- 🐳 Docker-based Qdrant deployment
- 📊 Automatic data validation
- 🎯 Object-oriented Python architecture

## Project Structure

```
multiagent/
├── data/
│   ├── loader.py          # CSV data loading utilities
│   └── processing.py      # Data preprocessing and text preparation
├── qdrant/
│   ├── client.py          # Qdrant vector database client
│   └── ingestion.py       # High-level ingestion interface
├── scripts/
│   └── ingestor.py        # Main ingestion script with validation
├── settings.py            # Configuration management
├── .env.example          # Environment variables template
└── README.md
```

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install qdrant-client pandas scikit-learn python-dotenv
```

### 2. Start Qdrant Database

```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant:v1.15.5
```

### 3. Configure Environment

Copy `.env.example` to `.env` and adjust settings:

```properties
EMBEDDING_MODEL=tfidf
VECTOR_SIZE=100
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=property_data
PROPERTY_DATA_FILE=property_data.csv
```

### 4. Run Ingestion

```bash
python scripts/ingestor.py
```

## Configuration

- **Embedding Model**: TF-IDF (lightweight, no GPU required)
- **Vector Size**: 100 dimensions
- **Batch Size**: 100 documents per batch
- **Data Limit**: First 1000 rows (configurable)

## Dependencies

- `qdrant-client`: Vector database client
- `pandas`: Data manipulation
- `scikit-learn`: TF-IDF vectorization
- `python-dotenv`: Environment configuration

## Architecture

- **Object-Oriented Design**: Clean separation of concerns
- **In-Memory Processing**: No intermediate file creation
- **Batch Processing**: Efficient large dataset handling
- **Automatic Validation**: Compares processed vs ingested counts

## Usage Examples

```python
from qdrant.client import QdrantVectorClient

# Initialize client
client = QdrantVectorClient(collection_name="property_data")

# Search for similar properties
results = client.search("commercial property downtown", limit=5)

# Check collection size
count = client.count_documents()
```

## License

MIT License