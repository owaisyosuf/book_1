import os
import logging
from typing import List, Dict, Any, Optional
import asyncio
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiManager:
    def __init__(self):
        self.client = None
        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")  # or "gemini-1.5-pro-latest"
        self.embedding_model = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")  # Updated model

    async def initialize(self):
        """Initialize the Gemini client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=api_key)
        self.client = genai
        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")
        self.embedding_model = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")

        logger.info("Gemini client initialized successfully")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using Gemini"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=[text],  # Pass as a list
                task_type="RETRIEVAL_DOCUMENT"
            )
            return result['embedding'][0]  # Return first embedding from the list
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def generate_response(self, query: str, context: List[Dict[str, Any]], history: List[Dict[str, Any]]) -> str:
        """Generate a response based on the query, context, and history using Gemini"""
        try:
            # Format the context into a readable string
            context_str = ""
            if context:
                context_str = "Relevant information from the book:\n\n"
                for idx, item in enumerate(context):
                    context_str += f"Source {idx + 1} (Chapter: {item.get('chapter_id', 'Unknown')}):\n"
                    context_str += f"{item.get('content', '')}\n\n"

            # Prepare the full prompt
            prompt = f"{context_str}\n\nQuestion: {query}\n\nPlease provide a helpful answer based on the above information. Use only the information provided in the context to answer questions. If the context doesn't contain the information needed to answer a question, say so explicitly. Always cite the chapter or section when providing information. Keep your responses helpful and concise."

            # Get the model
            model = genai.GenerativeModel(self.model)

            # Generate content
            response = model.generate_content(prompt)

            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Return a helpful error message
            return f"Sorry, I encountered an error processing your request: {str(e)}. Please try again later."

    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            results = []
            for text in texts:
                embedding_result = genai.embed_content(
                    model=self.embedding_model,
                    content=[text],  # Pass as a list
                    task_type="RETRIEVAL_DOCUMENT"
                )
                results.append(embedding_result['embedding'][0])  # Return first embedding from the list
            return results
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    async def validate_api_key(self) -> bool:
        """Validate the Gemini API key by making a simple request"""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content("Hello")
            return len(response.text) > 0
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

    async def get_token_count(self, text: str) -> int:
        """Estimate the number of tokens in the text"""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.count_tokens(text)
            return response.total_tokens
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            # Fallback: rough estimate (1 token ≈ 4 characters)
            import math
            return math.ceil(len(text) / 4)