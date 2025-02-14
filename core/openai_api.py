import openai
import os
from dotenv import load_dotenv

# Load API key from .env file (if using)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(user_input):
    """Sends user input to OpenAI and returns the response using the latest API format."""
    try:
        client = openai.OpenAI()  # Create OpenAI client (New API format)
        response = client.chat.completions.create(
            model="gpt-4",  # Change model if needed
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content  # Adjusted response format
    except Exception as e:
        return f"Error: {e}"
