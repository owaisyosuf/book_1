import os
import logging
from typing import List, Dict, Any, Optional
import asyncio
import openai
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

class OpenAIManager:
    def __init__(self):
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

    async def initialize(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OPENAI_API_KEY environment variable is required")

        self.client = AsyncOpenAI(api_key=api_key)

        logger.info("OpenAI client initialized successfully")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text"""
        if not self.client:
            raise Exception("OpenAI client not initialized")

        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    async def generate_response(self, query: str, context: List[Dict[str, Any]], history: List[Dict[str, Any]]) -> str:
        """Generate a response based on the query, context, and history"""
        if not self.client:
            raise Exception("OpenAI client not initialized")

        try:
            # Format the context into a readable string
            context_str = ""
            if context:
                context_str = "Relevant information from the book:\n\n"
                for idx, item in enumerate(context):
                    context_str += f"Source {idx + 1} (Chapter: {item.get('chapter_id', 'Unknown')}):\n"
                    context_str += f"{item.get('content', '')}\n\n"

            # Prepare the messages for the chat
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant for the AI/Spec-Driven Book. "
                        "Your role is to answer questions about the book's content. "
                        "Use only the information provided in the context to answer questions. "
                        "If the context doesn't contain the information needed to answer a question, "
                        "say so explicitly. Always cite the chapter or section when providing information. "
                        "Keep your responses helpful and concise."
                    )
                }
            ]

            # Add history if available
            if history:
                for message in history:
                    messages.append({
                        "role": message.get("role", "user"),
                        "content": message.get("content", "")
                    })

            # Add the current query with context
            messages.append({
                "role": "user",
                "content": f"{context_str}\n\nQuestion: {query}\n\nPlease provide a helpful answer based on the above information."
            })

            # Generate the response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not self.client:
            raise Exception("OpenAI client not initialized")

        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise

    async def validate_api_key(self) -> bool:
        """Validate the OpenAI API key by making a simple request"""
        try:
            response = await self.client.models.list()
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False

    async def get_token_count(self, text: str) -> int:
        """Estimate the number of tokens in the text"""
        # This is a simple estimation - for more accurate counting,
        # we could use tiktoken library
        import math
        # Rough estimate: 1 token ≈ 4 characters
        return math.ceil(len(text) / 4)