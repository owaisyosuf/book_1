#!/usr/bin/env python3
"""
Script to run the RAG Chatbot backend server
"""

import os
import sys
import subprocess
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    print("Starting RAG Chatbot backend server...")
    print("Make sure you have set up your .env file with the required API keys.")
    print("Server will be available at http://localhost:8000")
    print("Press Ctrl+C to stop the server.")
    print()

    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # Set environment variables from .env file
    env_file = backend_dir / ".env"
    if env_file.exists():
        print(f"Loading environment variables from {env_file}")
        # Load environment variables from .env file
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    else:
        print(f"Warning: {env_file} not found. Please create it with your API keys.")

    # Run the uvicorn server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except FileNotFoundError:
        print("Error: uvicorn not found. Please install dependencies with: pip install -r requirements.txt")

if __name__ == "__main__":
    run_backend()