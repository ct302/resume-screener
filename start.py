#!/usr/bin/env python
"""
Quick start script for Resume Screener API
Run this to start your money-making machine!
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Resume Screener API...")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        
        # Install requirements
        print("📥 Installing dependencies...")
        pip_path = os.path.join("venv", "Scripts", "pip.exe") if os.name == 'nt' else os.path.join("venv", "bin", "pip")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # Start the server
    print("\n✅ Starting server at http://localhost:8000")
    print("📚 API Documentation at http://localhost:8000/docs")
    print("\n💡 Tip: Read CHARLES_START_SELLING_NOW.md for instant monetization!")
    print("=" * 50)
    
    uvicorn_path = os.path.join("venv", "Scripts", "uvicorn.exe") if os.name == 'nt' else os.path.join("venv", "bin", "uvicorn")
    subprocess.run([uvicorn_path, "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    main()
