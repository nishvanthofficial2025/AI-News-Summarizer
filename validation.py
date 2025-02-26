import os  # ✅ Import os module
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ Ensure API key is set correctly
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Check your .env file.")

genai.configure(api_key=api_key)

# ✅ List all available models
print("Available Gemini models:")
for model in genai.list_models():
    print(model.name)
