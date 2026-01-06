import logging
from typing import List, Dict, Any, Optional
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
import asyncio

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, embedding_manager=None):
        self.client = None
        self.collection_name = "book_content"
        # Use appropriate size based on embedding model
        # text-embedding-004 from Gemini returns 768 dimensions
        self.vector_size = 768
        self.embedding_manager = embedding_manager

    async def initialize(self):
        """Initialize the Qdrant client"""
        import os
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_api_key:
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key
            )
        else:
            # For local development
            self.client = QdrantClient(host="localhost", port=6333)

        # Create collection if it doesn't exist
        await self._create_collection()

    async def _create_collection(self):
        """Create the collection for storing book content vectors"""
        try:
            # Check if collection exists - Qdrant client.get_collections() is not async
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    ),
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise

    async def add_content(self, content: str, chapter_id: str, section_title: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add content to the vector store"""
        if not self.client:
            raise Exception("Qdrant client not initialized")

        # Generate embedding (this would typically be done with OpenAI or another embedding service)
        # For now, we'll simulate this with a placeholder
        embedding = await self._generate_embedding(content)

        # Create a unique ID for this content
        content_id = str(uuid.uuid4())

        # Prepare the point to be inserted
        point = models.PointStruct(
            id=content_id,
            vector=embedding,
            payload={
                "content": content,
                "chapter_id": chapter_id,
                "section_title": section_title,
                "metadata": metadata or {}
            }
        )

        # Insert the point into the collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        logger.info(f"Added content to vector store: {content_id}")
        return content_id

    async def search(self, query: str, top_k: int = 5, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for relevant content based on the query"""
        if not self.client:
            raise Exception("Qdrant client not initialized")

        # Generate embedding for the query
        query_embedding = await self._generate_embedding(query)

        # Prepare search filter based on selected text if provided
        search_filter = None
        if selected_text:
            # This is a simplified approach - in practice you might want to
            # use more sophisticated filtering
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="content",
                        match=models.MatchText(text=selected_text[:100])  # Limit for performance
                    )
                ]
            )

        # Perform the search - Qdrant client.search() is not async
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=top_k,
            with_payload=True
        )

        # Format the results
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "chapter_id": result.payload.get("chapter_id", ""),
                "section_title": result.payload.get("section_title", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            })

        logger.info(f"Found {len(results)} results for query")
        return results

    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using the embedding manager"""
        # For testing purposes, let's use random embeddings to avoid quota issues
        # In production, uncomment the code below to use the actual embedding manager
        import random
        return [random.random() for _ in range(self.vector_size)]

        # Uncomment the following code when you have embedding quota available:
        # if self.embedding_manager:
        #     try:
        #         return await self.embedding_manager.generate_embedding(text)
        #     except Exception as e:
        #         logger.error(f"Error generating embedding with manager: {e}")
        #         # Fallback to random embedding if manager fails
        #         import random
        #         return [random.random() for _ in range(self.vector_size)]
        # else:
        #     # Fallback to random embedding if no manager is provided
        #     import random
        #     return [random.random() for _ in range(self.vector_size)]

    async def batch_add_content(self, contents: List[Dict[str, Any]]) -> List[str]:
        """Add multiple content items to the vector store"""
        content_ids = []
        for content_item in contents:
            content_id = await self.add_content(
                content=content_item.get("content", ""),
                chapter_id=content_item.get("chapter_id", ""),
                section_title=content_item.get("section_title", ""),
                metadata=content_item.get("metadata")
            )
            content_ids.append(content_id)

        return content_ids

    async def delete_content(self, content_id: str):
        """Delete content from the vector store"""
        if not self.client:
            raise Exception("Qdrant client not initialized")

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[content_id]
            )
        )
        logger.info(f"Deleted content from vector store: {content_id}")