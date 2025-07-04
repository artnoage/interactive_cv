"""
Semantic search functionality for the Interactive CV RAG system.
Uses embeddings for similarity-based retrieval.
"""

import sqlite3
import numpy as np
from typing import List, Dict, Any, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI for embedding generation
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    OPENAI_AVAILABLE = False
    client = None


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def generate_embedding(text: str, model: str = "text-embedding-3-large") -> np.ndarray:
    """Generate embedding for a text using OpenAI API."""
    if not OPENAI_AVAILABLE or not client:
        raise RuntimeError("OpenAI API not available")
    
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return np.array(response.data[0].embedding)


def load_embedding_from_blob(blob: bytes) -> np.ndarray:
    """Convert stored BLOB back to numpy array."""
    return np.frombuffer(blob, dtype=np.float32)


def semantic_search_chunks(db_path: str, query: str, limit: int = 5, 
                          doc_type: str = None, similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Search document chunks using semantic similarity.
    
    Args:
        db_path: Path to the database
        query: Search query
        limit: Maximum number of results
        doc_type: Filter by document type (academic/chronicle)
        similarity_threshold: Minimum similarity score
    
    Returns:
        List of chunk results with similarity scores
    """
    if not OPENAI_AVAILABLE:
        return []
    
    try:
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        
        conn = sqlite3.connect(db_path)
        
        # Build query based on filters
        base_query = """
            SELECT 
                dc.id,
                dc.document_id,
                dc.document_type,
                dc.chunk_index,
                dc.content,
                dc.start_char,
                dc.end_char,
                e.embedding
            FROM document_chunks dc
            JOIN embeddings e ON e.entity_id = dc.id AND e.entity_type = 'chunk'
            WHERE e.embedding IS NOT NULL
        """
        
        if doc_type:
            base_query += f" AND dc.document_type = '{doc_type}'"
        
        results = []
        for row in conn.execute(base_query):
            chunk_id, doc_id, doc_type, chunk_idx, content, start_char, end_char, embedding_blob = row
            
            # Calculate similarity
            chunk_embedding = load_embedding_from_blob(embedding_blob)
            similarity = cosine_similarity(query_embedding, chunk_embedding)
            
            if similarity >= similarity_threshold:
                results.append({
                    'chunk_id': chunk_id,
                    'document_id': doc_id,
                    'document_type': doc_type,
                    'chunk_index': chunk_idx,
                    'content': content,
                    'similarity': float(similarity),
                    'start_char': start_char,
                    'end_char': end_char
                })
        
        conn.close()
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
        
    except Exception as e:
        print(f"Semantic search error: {e}")
        return []


def find_similar_entities(db_path: str, query: str, entity_type: str = None, 
                         limit: int = 10, similarity_threshold: float = 0.6) -> List[Dict[str, Any]]:
    """
    Find entities similar to the query using embeddings.
    
    Args:
        db_path: Path to the database
        query: Search query
        entity_type: Filter by entity type (topic/person/method/etc)
        limit: Maximum number of results
        similarity_threshold: Minimum similarity score
    
    Returns:
        List of similar entities with scores
    """
    if not OPENAI_AVAILABLE:
        return []
    
    try:
        query_embedding = generate_embedding(query)
        
        conn = sqlite3.connect(db_path)
        
        # Build query based on filters
        base_query = """
            SELECT 
                e.entity_id,
                e.entity_type,
                e.embedding
            FROM embeddings e
            WHERE e.embedding IS NOT NULL
        """
        
        if entity_type:
            base_query += f" AND e.entity_type = '{entity_type}'"
        
        results = []
        for row in conn.execute(base_query):
            entity_id, ent_type, embedding_blob = row
            
            # Calculate similarity
            entity_embedding = load_embedding_from_blob(embedding_blob)
            similarity = cosine_similarity(query_embedding, entity_embedding)
            
            if similarity >= similarity_threshold:
                # Get entity details based on type
                if ent_type == 'topic':
                    entity_query = "SELECT name, category FROM topics WHERE id = ?"
                elif ent_type == 'person':
                    entity_query = "SELECT name, role FROM people WHERE id = ?"
                elif ent_type == 'method':
                    entity_query = "SELECT name, category FROM methods WHERE id = ?"
                else:
                    continue
                
                entity_details = conn.execute(entity_query, (entity_id,)).fetchone()
                if entity_details:
                    results.append({
                        'entity_id': entity_id,
                        'entity_type': ent_type,
                        'name': entity_details[0],
                        'category': entity_details[1] if len(entity_details) > 1 else None,
                        'similarity': float(similarity)
                    })
        
        conn.close()
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
        
    except Exception as e:
        print(f"Entity search error: {e}")
        return []