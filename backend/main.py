from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our custom modules
from database import DatabaseManager
from vector_store import VectorStoreManager
from gemini_integration import GeminiManager

app = FastAPI(
    title="AI/Spec-Driven Book RAG Chatbot",
    description="A Retrieval-Augmented Generation chatbot for the AI/Spec-Driven Book",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None  # For context-specific queries
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[Dict[str, Any]]] = []
    timestamp: str

class IndexRequest(BaseModel):
    content: str
    chapter_id: str
    section_title: str

class RAGChatbot:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.gemini_manager = GeminiManager()
        self.vector_store = VectorStoreManager(embedding_manager=self.gemini_manager)

    async def initialize(self):
        """Initialize all components"""
        await self.db_manager.initialize()
        await self.gemini_manager.initialize()
        await self.vector_store.initialize()

    async def index_content(self, content: str, chapter_id: str, section_title: str) -> str:
        """Index content in Qdrant vector database"""
        return await self.vector_store.add_content(
            content=content,
            chapter_id=chapter_id,
            section_title=section_title
        )

    async def retrieve_context(self, query: str, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector database"""
        return await self.vector_store.search(
            query=query,
            selected_text=selected_text
        )

    async def generate_response(self, query: str, context: List[Dict[str, Any]], history: List[Message]) -> str:
        """Generate response using Gemini with retrieved context"""
        # Convert Message objects to dictionaries for Gemini
        history_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]

        return await self.gemini_manager.generate_response(
            query=query,
            context=context,
            history=history_dicts
        )

    async def save_chat_history(self, session_id: str, message: Message) -> None:
        """Save chat history to PostgreSQL"""
        await self.db_manager.save_chat_message(
            session_id=session_id,
            role=message.role,
            content=message.content
        )

    async def get_chat_history(self, session_id: str) -> List[Message]:
        """Get chat history from PostgreSQL"""
        history = await self.db_manager.get_chat_history(session_id)
        return [
            Message(role=item["role"], content=item["content"])
            for item in history
        ]

# Global chatbot instance
chatbot = RAGChatbot()

@app.on_event("startup")
async def startup_event():
    await chatbot.initialize()
    logger.info("RAG Chatbot initialized successfully")

@app.get("/")
async def root():
    return {"message": "AI/Spec-Driven Book RAG Chatbot API", "status": "running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Retrieve relevant context based on the query and selected text
        context = await chatbot.retrieve_context(request.message, request.selected_text)

        # Generate response using OpenAI
        response_text = await chatbot.generate_response(request.message, context, request.history)

        # Create a new session ID if not provided
        session_id = request.session_id or f"session_{hash(request.message) % 10000}"

        # Save user message to history
        user_message = Message(role="user", content=request.message)
        await chatbot.save_chat_history(session_id, user_message)

        # Save assistant response to history
        assistant_message = Message(role="assistant", content=response_text)
        await chatbot.save_chat_history(session_id, assistant_message)

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            sources=context,
            timestamp="2026-01-05T12:00:00Z"  # Mock timestamp
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/index")
async def index_content(request: IndexRequest):
    """Endpoint to index new content"""
    try:
        content_id = await chatbot.index_content(request.content, request.chapter_id, request.section_title)
        return {"message": "Content indexed successfully", "content_id": content_id}
    except Exception as e:
        logger.error(f"Error in index endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RAG Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)