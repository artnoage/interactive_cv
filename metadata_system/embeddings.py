#!/usr/bin/env python3
"""
Basic embeddings generation using OpenAI API.
Stores embeddings in the database for semantic search.
"""

import os
import json
import sqlite3
import numpy as np
from typing import List, Optional, Tuple
import logging
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate and manage embeddings for documents."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db"):
        self.db_path = db_path
        
        # Initialize OpenAI embeddings directly
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
            
        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(api_key),
            model="text-embedding-3-small"  # Good balance of performance/cost
        )
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def prepare_document_text(self, doc_id: int) -> Optional[str]:
        """Prepare document text for embedding."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get document metadata
            cursor.execute("""
                SELECT file_path, title, doc_type, metadata 
                FROM documents 
                WHERE id = ?
            """, (doc_id,))
            
            doc = cursor.fetchone()
            if not doc:
                return None
            
            # Parse metadata
            metadata = json.loads(doc['metadata'])
            
            # Build text representation based on document type
            text_parts = [f"Title: {doc['title']}"]
            
            if doc['doc_type'] == 'academic':
                # For academic papers, include key concepts and contributions
                if metadata.get('core_contributions'):
                    text_parts.append(f"Core Contributions: {metadata['core_contributions']}")
                if metadata.get('problem_solved'):
                    text_parts.append(f"Problem Solved: {metadata['problem_solved']}")
                if metadata.get('mathematical_concepts'):
                    text_parts.append(f"Mathematical Concepts: {', '.join(metadata['mathematical_concepts'])}")
                if metadata.get('applications'):
                    text_parts.append(f"Applications: {', '.join(metadata['applications'])}")
                if metadata.get('key_innovations'):
                    text_parts.append(f"Key Innovations: {', '.join(metadata['key_innovations'])}")
                    
            else:  # chronicle
                # For chronicle notes, include work focus and key insights
                if metadata.get('work_focus'):
                    text_parts.append(f"Work Focus: {metadata['work_focus']}")
                if metadata.get('daily_summary'):
                    text_parts.append(f"Summary: {metadata['daily_summary']}")
                if metadata.get('topics'):
                    text_parts.append(f"Topics: {', '.join(metadata['topics'])}")
                if metadata.get('projects'):
                    text_parts.append(f"Projects: {', '.join(metadata['projects'])}")
                if metadata.get('insights'):
                    insights_text = ' '.join(metadata['insights'][:3])  # First 3 insights
                    text_parts.append(f"Key Insights: {insights_text}")
            
            return '\n'.join(text_parts)
            
        finally:
            conn.close()
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def store_embedding(self, doc_id: int, embedding: List[float]):
        """Store embedding in database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Convert embedding to bytes for storage
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            # Update document with embedding
            cursor.execute("""
                UPDATE documents 
                SET embedding = ? 
                WHERE id = ?
            """, (embedding_bytes, doc_id))
            
            conn.commit()
            logger.info(f"Stored embedding for document {doc_id}")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error storing embedding: {e}")
            raise
        finally:
            conn.close()
    
    def process_document(self, doc_id: int) -> bool:
        """Generate and store embedding for a single document."""
        try:
            # Prepare text
            text = self.prepare_document_text(doc_id)
            if not text:
                logger.warning(f"No text found for document {doc_id}")
                return False
            
            logger.info(f"Generating embedding for document {doc_id}")
            logger.debug(f"Text preview: {text[:200]}...")
            
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            # Store in database
            self.store_embedding(doc_id, embedding)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {e}")
            return False
    
    def process_all_documents(self, doc_type: Optional[str] = None):
        """Process all documents without embeddings."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Find documents without embeddings
            query = "SELECT id, title FROM documents WHERE embedding IS NULL"
            params = []
            
            if doc_type:
                query += " AND doc_type = ?"
                params.append(doc_type)
            
            cursor.execute(query, params)
            documents = cursor.fetchall()
            
            logger.info(f"Found {len(documents)} documents without embeddings")
            
            successful = 0
            for doc in documents:
                if self.process_document(doc['id']):
                    successful += 1
                    logger.info(f"✓ Processed: {doc['title']}")
                else:
                    logger.error(f"✗ Failed: {doc['title']}")
            
            logger.info(f"Successfully generated embeddings for {successful}/{len(documents)} documents")
            
        finally:
            conn.close()
    
    def generate_chunk_embeddings(self, doc_id: Optional[int] = None):
        """Generate embeddings for document chunks."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Find chunks without embeddings
            if doc_id:
                query = """
                    SELECT c.id, c.chunk_title, c.chunk_content, d.title as doc_title
                    FROM document_chunks c
                    JOIN documents d ON c.document_id = d.id
                    WHERE c.embedding IS NULL AND c.document_id = ?
                """
                cursor.execute(query, (doc_id,))
            else:
                query = """
                    SELECT c.id, c.chunk_title, c.chunk_content, d.title as doc_title
                    FROM document_chunks c
                    JOIN documents d ON c.document_id = d.id
                    WHERE c.embedding IS NULL
                """
                cursor.execute(query)
            
            chunks = cursor.fetchall()
            logger.info(f"Found {len(chunks)} chunks without embeddings")
            
            successful = 0
            for chunk in chunks:
                try:
                    # Prepare chunk text
                    text = f"Document: {chunk['doc_title']}\n"
                    text += f"Section: {chunk['chunk_title']}\n"
                    text += f"Content: {chunk['chunk_content'][:1000]}"  # Limit length
                    
                    # Generate embedding
                    embedding = self.generate_embedding(text)
                    
                    # Store in database
                    embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
                    cursor.execute("""
                        UPDATE document_chunks 
                        SET embedding = ? 
                        WHERE id = ?
                    """, (embedding_bytes, chunk['id']))
                    
                    conn.commit()
                    successful += 1
                    logger.info(f"✓ Generated embedding for chunk: {chunk['chunk_title']}")
                    
                except Exception as e:
                    logger.error(f"Failed to embed chunk {chunk['id']}: {e}")
            
            logger.info(f"Successfully generated embeddings for {successful}/{len(chunks)} chunks")
            
        finally:
            conn.close()
    
    def find_similar_chunks(self, query_text: str, top_k: int = 5) -> List[Tuple[int, float, str, str]]:
        """Find similar document chunks using cosine similarity."""
        try:
            # Generate query embedding
            query_embedding = np.array(self.generate_embedding(query_text), dtype=np.float32)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get all chunks with embeddings
            cursor.execute("""
                SELECT c.id, c.chunk_title, c.embedding, d.title as doc_title
                FROM document_chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE c.embedding IS NOT NULL
            """)
            
            results = []
            for row in cursor.fetchall():
                # Convert bytes back to numpy array
                chunk_embedding = np.frombuffer(row['embedding'], dtype=np.float32)
                
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, chunk_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
                )
                
                results.append((
                    row['id'], 
                    float(similarity), 
                    row['chunk_title'],
                    row['doc_title']
                ))
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x[1], reverse=True)
            
            conn.close()
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar chunks: {e}")
            return []
    
    def find_similar_documents(self, query_text: str, top_k: int = 5) -> List[Tuple[int, float, str]]:
        """Find similar documents using cosine similarity."""
        try:
            # Generate query embedding
            query_embedding = np.array(self.generate_embedding(query_text), dtype=np.float32)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get all documents with embeddings
            cursor.execute("""
                SELECT id, title, embedding 
                FROM documents 
                WHERE embedding IS NOT NULL
            """)
            
            results = []
            for row in cursor.fetchall():
                # Convert bytes back to numpy array
                doc_embedding = np.frombuffer(row['embedding'], dtype=np.float32)
                
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                
                results.append((row['id'], float(similarity), row['title']))
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x[1], reverse=True)
            
            conn.close()
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar documents: {e}")
            return []


def test_embeddings():
    """Test embedding generation and similarity search."""
    generator = EmbeddingGenerator()
    
    # Test processing a few documents
    print("Testing embedding generation...")
    
    # Process first 3 documents
    conn = generator.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM documents LIMIT 3")
    test_docs = cursor.fetchall()
    conn.close()
    
    for doc in test_docs:
        print(f"\nProcessing: {doc['title']}")
        success = generator.process_document(doc['id'])
        print(f"Result: {'✓ Success' if success else '✗ Failed'}")
    
    # Test similarity search
    print("\n" + "="*60)
    print("Testing similarity search...")
    
    test_queries = [
        "optimal transport and machine learning",
        "reinforcement learning and game development",
        "mathematical theory and probability"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        similar = generator.find_similar_documents(query, top_k=3)
        
        if similar:
            print("Similar documents:")
            for _, similarity, title in similar:
                print(f"  - {title[:60]}... (similarity: {similarity:.3f})")
        else:
            print("  No results found")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate embeddings for documents")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test mode with a few documents"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all documents without embeddings"
    )
    parser.add_argument(
        "--doc-type",
        choices=['academic', 'chronicle'],
        help="Process only specific document type"
    )
    
    args = parser.parse_args()
    
    if args.test:
        test_embeddings()
    elif args.all:
        generator = EmbeddingGenerator()
        generator.process_all_documents(doc_type=args.doc_type)
    else:
        print("Use --test for testing or --all to process all documents")