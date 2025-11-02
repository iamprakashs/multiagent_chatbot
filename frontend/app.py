import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask, render_template, request, jsonify
from qdrant.client import QdrantVectorClient
from multiagentic.conversational_agent import make_search_conversational
from settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/search-ui')
def search_ui():
    return render_template('index.html')

@app.route('/chat-ui')
def chat_ui():
    return render_template('chat.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = data.get('limit', 5)
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        client = QdrantVectorClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        
        results = client.search(query, limit=limit)
        logger.info(f"Search for '{query}' returned {results}")
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500

    
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = data.get('limit', 5)

        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400

        client = QdrantVectorClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )

        results = client.search(query, limit=limit)
        conversational_response = make_search_conversational(query, results)

        return jsonify({
            'query': query,
            'response': conversational_response,
            'total': len(results)
        })

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status():
    try:
        client = QdrantVectorClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        
        count = client.count_documents()
        
        return jsonify({
            'status': 'healthy',
            'collection': settings.COLLECTION_NAME,
            'document_count': count
        })
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)