# Property Search with Qdrant Vector Database

A modern property search system using **Qdrant vector database** with **sentence transformers** for semantic search capabilities.

## ✨ Features

- 🏠 **Property Data Processing** - Intelligent text extraction and preprocessing
- 🔍 **Semantic Search** - Natural language queries using sentence transformers
- � **Vector Database** - Fast similarity search with Qdrant
- 🌐 **Web Interface** - Clean, responsive search frontend
- � **Real-time Status** - Collection health and document count monitoring
- ⚡ **No Training Required** - Pre-trained embeddings, ready to use

## �️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Layer    │────│  Vector Engine   │────│   Frontend      │
│                 │    │                  │    │                 │
│ • CSV Loading   │    │ • Qdrant DB     │    │ • Flask API     │
│ • Text Processing│    │ • Sentence Trans │    │ • Search UI     │
│ • Data Cleaning │    │ • 384-dim vectors│    │ • Status Check  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
multiagent/
├── data/
│   ├── loader.py          # CSV data loading utilities
│   └── processing.py      # Data preprocessing and text preparation
├── qdrant/
│   ├── client.py          # Qdrant vector database client
│   └── ingestion.py       # High-level ingestion interface
├── frontend/
│   ├── app.py            # Flask web application
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JavaScript assets
├── scripts/
│   └── ingestor.py       # Data ingestion script
├── settings.py           # Configuration management
├── .env                  # Environment variables
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker (for Qdrant)
- Virtual environment (recommended)

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Qdrant Database

```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant:v1.15.5

# Or using Docker Compose
docker-compose up -d
```

### 3. Configure Environment

Create `.env` file:

```env
# Embedding Model (Sentence Transformers)
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_SIZE=384

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=property_data

# Data Configuration
PROPERTY_DATA_FILE=property_data.csv
```

### 4. Ingest Data

```bash
# Run data ingestion
python scripts/ingestor.py
```

### 5. Start Web Interface

```bash
# Start Flask application
cd frontend
python app.py
```

Open http://localhost:5000 in your browser.

## 🔧 Configuration

### Embedding Models

The system uses **sentence-transformers** for semantic embeddings:

- **Default**: `all-MiniLM-L6-v2` (384 dimensions)
- **Alternative**: `all-mpnet-base-v2` (768 dimensions, better quality)
- **Lightweight**: `paraphrase-MiniLM-L3-v2` (384 dimensions, faster)

### Data Processing

- **Automatic text detection** from CSV columns
- **Content combination** for rich search context
- **Batch processing** for efficient ingestion
- **Memory-optimized** workflow

## 🎯 Usage Examples

### Search Queries

```bash
# Natural language search
"luxury apartment with pool downtown"
"commercial office space for rent"
"family house with garden near school"
"modern condo with parking"
```

### API Endpoints

```python
# Search properties
POST /search
{
    "query": "luxury apartment",
    "limit": 10
}

# Check system status
GET /status
```

### Programmatic Usage

```python
from qdrant.client import QdrantVectorClient

# Initialize client
client = QdrantVectorClient(
    collection_name="property_data",
    embedding_model="all-MiniLM-L6-v2"
)

# Search properties
results = client.search("downtown apartment", limit=5)
```

## 📊 Performance

- **Search Speed**: < 100ms for typical queries
- **Embedding Generation**: Real-time with sentence transformers
- **Scalability**: Handles 10K+ documents efficiently
- **Memory Usage**: ~2GB for model + data

## 🛠️ Development

### Adding New Data Sources

1. Extend `DataLoader` class in `data/loader.py`
2. Update `DataProcessor` for new data formats
3. Configure field mappings in `settings.py`

### Custom Embedding Models

```python
# Update client initialization
client = QdrantVectorClient(
    embedding_model="your-custom-model",
    collection_name="your_collection"
)
```

### Frontend Customization

- **Templates**: Modify `frontend/templates/index.html`
- **Styling**: Update `frontend/static/style.css`
- **Behavior**: Extend `frontend/static/script.js`

## 📝 Dependencies

### Core Libraries

```
qdrant-client>=1.7.1    # Vector database client
sentence-transformers   # Pre-trained embeddings
pandas>=2.1.4          # Data manipulation
flask>=2.3.0           # Web framework
python-dotenv>=1.0.0   # Environment configuration
```

### Optional

```
torch                  # Deep learning backend
transformers          # Model infrastructure
scikit-learn          # Additional ML utilities
```

## 🐳 Docker Deployment

```dockerfile
# Build application image
docker build -t property-search .

# Run with Docker Compose
docker-compose up
```

## 🔍 Troubleshooting

### Common Issues

**Qdrant Connection Error**
```bash
# Check if Qdrant is running
curl http://localhost:6333/health
```

**Model Download Issues**
```bash
# Pre-download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**Memory Issues**
```bash
# Use lighter model
EMBEDDING_MODEL=paraphrase-MiniLM-L3-v2
```

## 📈 Monitoring

- **Health Check**: `/status` endpoint
- **Document Count**: Automatic validation
- **Search Performance**: Built-in timing
- **Error Logging**: Comprehensive logging system

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Qdrant** - Vector database engine
- **Sentence Transformers** - Pre-trained embedding models
- **Hugging Face** - Model infrastructure
- **Flask** - Web framework