import os
from groq import Groq
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConversationalAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def make_conversational(self, query: str, data: List[Dict]) -> str:
        prompt = f"""You are a helpful real estate assistant. A user searched for properties with the query: "{query}"

Here are the search results:
{data}

Please provide a friendly, conversational response that:
1. Acknowledges their search query
2. Summarizes the key findings in an easy-to-understand way
3. Highlights the most relevant properties
4. Mentions important details like property type, location, price, and features
5. Uses a warm, professional tone
6. Offers to help with more details if needed

Response:"""
        
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        
        return completion.choices[0].message.content.strip()

def make_search_conversational(query: str, data: List[Dict]) -> str:
    agent = ConversationalAgent()
    return agent.make_conversational(query, data)
