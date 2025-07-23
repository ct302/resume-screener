import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')

# SECURITY WARNING: 
# The current app.py has your API key hardcoded!
# Before pushing to GitHub:
# 1. Create a .env file with: GEMINI_API_KEY=AIzaSyBTUhWLV5oZZ00QwqhCYiIhgY4s5Z-qB34
# 2. Update app.py to use: genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
# 3. Never commit .env to Git (.gitignore already excludes it)

print("⚠️  SECURITY WARNING:")
print("Your API key is currently hardcoded in app.py!")
print("Follow the instructions above to secure it before pushing to GitHub.")
