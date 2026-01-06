# AI/Spec-Driven Book RAG Chatbot Backend

This backend provides a Retrieval-Augmented Generation (RAG) chatbot for the AI/Spec-Driven Book, allowing users to ask questions about the book content.

## Architecture

The backend uses:
- **FastAPI** - Web framework for the API
- **OpenAI API** - For embeddings and chat completions
- **Qdrant Cloud** - Vector database for content storage and retrieval
- **Neon Serverless Postgres** - Database for chat history and metadata

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with the following:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

   # Qdrant Configuration
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here

   # Neon Postgres Configuration
   NEON_POSTGRES_URL=your_neon_postgres_connection_string_here
   ```

3. **Run the backend server:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

## API Endpoints

- `GET /` - Health check and status
- `POST /chat` - Main chat endpoint
- `POST /index` - Index new content
- `GET /health` - Health check

## Indexing Book Content

To index the book content into the vector store:

```bash
python index_book_content.py
```

This will read all markdown files from the `../docs` directory and index them into the vector store.

## Frontend Integration

The frontend React component is located in the main Docusaurus project at `src/components/Chatbot.js` and is integrated into all pages via `src/theme/Root.js`.

## Testing

To test the API:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is AI?",
    "session_id": "test-session"
  }'
```

## Deployment

For deployment, ensure all environment variables are properly configured in your deployment environment.