import asyncpg
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.connection_string = os.getenv("NEON_POSTGRES_URL")

    async def initialize(self):
        """Initialize the database connection pool"""
        if not self.connection_string:
            logger.warning("NEON_POSTGRES_URL not set, skipping database initialization")
            return

        try:
            self.pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {e}")
            raise

    async def close(self):
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()

    async def get_session_id(self) -> str:
        """Generate a new session ID"""
        import uuid
        return str(uuid.uuid4())

    async def save_chat_message(self, session_id: str, role: str, content: str):
        """Save a chat message to the database"""
        if not self.pool:
            return  # Skip if no database connection

        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO chat_history (session_id, message_id, role, content, timestamp)
                VALUES ($1, $2, $3, $4, NOW())
                """,
                session_id,
                f"msg_{hash(content) % 1000000}",
                role,
                content
            )

    async def get_chat_history(self, session_id: str):
        """Retrieve chat history for a session"""
        if not self.pool:
            return []  # Return empty list if no database connection

        async with self.pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT role, content, timestamp
                FROM chat_history
                WHERE session_id = $1
                ORDER BY timestamp ASC
                """,
                session_id
            )
            return [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]} for row in rows]

    async def save_user_interaction(self, session_id: str, user_id: Optional[str], interaction_type: str, query: str, response: str):
        """Save user interaction for analytics"""
        if not self.pool:
            return  # Skip if no database connection

        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO user_interactions (session_id, user_id, interaction_type, query_text, response_text, timestamp)
                VALUES ($1, $2, $3, $4, $5, NOW())
                """,
                session_id, user_id, interaction_type, query, response
            )