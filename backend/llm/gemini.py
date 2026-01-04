import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini Pro
MODEL_NAME = "gemini-pro"

def generate_response(prompt: str) -> str:
    """
    Generates a response from Google Gemini API.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"
