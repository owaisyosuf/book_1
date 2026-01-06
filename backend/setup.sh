#!/bin/bash
# Script to set up and run the RAG Chatbot for the AI/Spec-Driven Book

echo "Setting up RAG Chatbot for AI/Spec-Driven Book..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Set up environment variables
echo "Setting up environment variables..."
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Qdrant Configuration
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Neon Postgres Configuration
NEON_POSTGRES_URL=your_neon_postgres_connection_string_here

# Development settings
DEBUG=true
EOF

echo "Environment file created at backend/.env"
echo "Please update the values in the .env file with your actual API keys and connection strings."

# Create a script to run the backend
cat > run_backend.py << EOF
import asyncio
import uvicorn
import os
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload for development
    )
EOF

echo "To run the backend server:"
echo "  1. cd backend"
echo "  2. Update the .env file with your API keys"
echo "  3. python run_backend.py"

echo "To index your book content, you can use the /index endpoint"
echo "To start the Docusaurus frontend, run 'npm run start' from the root directory"

echo "Setup complete!"