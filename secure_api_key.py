import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')


print("⚠️  SECURITY WARNING:")
print("Your API key is currently hardcoded in app.py!")
print("Follow the instructions above to secure it before pushing to GitHub.")
