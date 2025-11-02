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

Please provide a complete, friendly, conversational response that:
1. Acknowledges their search query warmly
2. Summarizes the key findings in an easy-to-understand way
3. Highlights the most relevant properties with specific details
4. Mentions important details like property type, location, price, and features
5. Uses a warm, professional tone
6. Provides actionable next steps or offers to help with more details
7. IMPORTANT: Complete your response fully - don't cut off mid-sentence

Make sure to finish your thoughts completely and end with a helpful closing statement.

Response:"""
        
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
                stop=None  # Allow complete responses
            )
            
            response = completion.choices[0].message.content.strip()
            
            # Check if response seems cut off and add a completion note if needed
            if not response.endswith(('.', '!', '?', '"', "'")):
                response += "\n\nWould you like me to provide more details about any of these properties?"
                
            return response
            
        except Exception as e:
            return f"I apologize, but I encountered an issue while processing your request: {str(e)}. Please try again or contact support if the problem persists."

def make_search_conversational(query: str, data: List[Dict]) -> str:
    agent = ConversationalAgent()
    return agent.make_conversational(query, data)
