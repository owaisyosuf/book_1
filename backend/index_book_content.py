#!/usr/bin/env python3
"""
Script to index the AI/Spec-Driven Book content into the vector store
"""

import asyncio
import os
import glob
from pathlib import Path
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to the path so we can import our modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import chatbot
from vector_store import VectorStoreManager

async def index_book_content():
    """Index all book content from the docs directory"""
    logger.info("Starting to index book content...")

    # Initialize the chatbot components
    await chatbot.initialize()

    # Get all markdown files from the docs directory
    docs_path = Path("../docs")
    markdown_files = list(docs_path.glob("*.md"))

    logger.info(f"Found {len(markdown_files)} markdown files to index")

    for file_path in markdown_files:
        logger.info(f"Processing {file_path.name}...")

        try:
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract chapter ID from filename
            chapter_id = file_path.stem  # e.g., "chapter-01-introduction-to-ai"

            # Extract title from the first line (assuming it's a markdown header)
            lines = content.split('\n')
            title = ""
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()  # Remove '# ' prefix
                    break

            # Split content into chunks for better retrieval
            chunks = split_content_into_chunks(content, max_chunk_size=1000)

            logger.info(f"Split {file_path.name} into {len(chunks)} chunks")

            # Index each chunk
            for i, chunk in enumerate(chunks):
                chunk_title = f"{title} - Part {i+1}" if len(chunks) > 1 else title
                content_id = await chatbot.index_content(
                    content=chunk,
                    chapter_id=chapter_id,
                    section_title=chunk_title
                )
                logger.info(f"Indexed chunk {i+1}/{len(chunks)} for {file_path.name}")

        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")

    logger.info("Finished indexing all book content!")

def split_content_into_chunks(content: str, max_chunk_size: int = 1000) -> list:
    """
    Split content into chunks of approximately max_chunk_size characters
    while preserving sentence boundaries where possible.
    """
    # Remove frontmatter if present
    if content.startswith('---'):
        try:
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                content = content[end_frontmatter + 3:].strip()
        except:
            pass

    # Split by paragraphs first
    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph would exceed the chunk size
        if len(current_chunk) + len(paragraph) > max_chunk_size:
            # If the current chunk is not empty, save it
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # If the paragraph itself is larger than max_chunk_size, split it
            if len(paragraph) > max_chunk_size:
                sentences = paragraph.split('. ')
                sentence_chunk = ""

                for sentence in sentences:
                    if len(sentence_chunk) + len(sentence) > max_chunk_size:
                        if sentence_chunk.strip():
                            chunks.append(sentence_chunk.strip())
                        sentence_chunk = sentence + '. '
                    else:
                        sentence_chunk += sentence + '. '

                if sentence_chunk.strip():
                    current_chunk = sentence_chunk.strip()
            else:
                current_chunk = paragraph
        else:
            current_chunk += "\n\n" + paragraph

    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

if __name__ == "__main__":
    asyncio.run(index_book_content())