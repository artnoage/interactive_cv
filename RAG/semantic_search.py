"""
Semantic search functionality for the Interactive CV RAG system.

This module provides advanced semantic search capabilities using OpenAI embeddings
to find semantically similar content across documents, chunks, and entities.
It supports multiple search modes and provides rich context for RAG applications.
"""

import sqlite3
import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional, Union
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import OpenAI for embedding generation
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.info("OpenAI client initialized successfully")
except ImportError:
    OPENAI_AVAILABLE = False
    client = None
    logger.warning("OpenAI not available - semantic search will be limited")
except Exception as e:
    OPENAI_AVAILABLE = False
    client = None
    logger.error(f"Error initializing OpenAI client: {e}")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score between -1 and 1
    """
    try:
        # Handle zero vectors
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return np.dot(a, b) / (norm_a * norm_b)
    except Exception as e:
        logger.error(f"Error calculating cosine similarity: {e}")
        return 0.0


def generate_embedding(text: str, model: str = "text-embedding-3-large") -> Optional[np.ndarray]:
    """
    Generate embedding for a text using OpenAI API.
    
    Args:
        text: Text to embed
        model: OpenAI embedding model to use
        
    Returns:
        Numpy array of embeddings or None if failed
    """
    if not OPENAI_AVAILABLE or not client:
        logger.warning("OpenAI API not available for embedding generation")
        return None
    
    try:
        # Clean and truncate text if needed
        text = text.strip()[:8000]  # OpenAI has token limits
        
        if not text:
            logger.warning("Empty text provided for embedding")
            return None
            
        response = client.embeddings.create(
            input=text,
            model=model
        )
        
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        logger.debug(f"Generated embedding with shape {embedding.shape}")
        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None


class SemanticSearchEngine:
    """Unified semantic search engine for all entity types."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def search_all_entities(self, query: str, limit: int = 20, 
                           entity_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search across all entity types using semantic embeddings.
        
        Args:
            query: Natural language search query
            limit: Maximum results to return
            entity_types: Optional list to filter by type
            
        Returns:
            List of entities sorted by similarity score
        """
        if not OPENAI_AVAILABLE:
            logger.warning("Semantic search not available - OpenAI client not initialized")
            return []
        
        conn = None
        try:
            # Create connection for this search
            conn = get_db_connection(self.db_path)
            
            # Generate query embedding
            query_embedding = generate_embedding(query)
            if query_embedding is None:
                logger.error("Failed to generate query embedding")
                return []
            
            results = []
            
            # Define entity type mappings
            type_mappings = {
                'document': [('academic_documents', 'academic'), ('chronicle_documents', 'chronicle')],
                'topic': [('topics', None)],
                'person': [('people', None)],
                'method': [('methods', None)],
                'institution': [('institutions', None)],
                'application': [('applications', None)],
                'project': [('projects', None)]
            }
            
            # Filter types if specified
            if entity_types:
                type_mappings = {k: v for k, v in type_mappings.items() if k in entity_types}
            
            # Search each entity type
            for entity_type, tables in type_mappings.items():
                for table_name, id_prefix in tables:
                    # Build query for this entity type
                    query_sql = f"""
                    SELECT 
                        t.*,
                        e.embedding
                    FROM {table_name} t
                    JOIN embeddings e ON 
                        e.entity_type = ? AND 
                        e.entity_id = CASE 
                            WHEN ? IS NOT NULL THEN (? || '_' || CAST(t.id AS TEXT))
                            ELSE (? || '_' || CAST(t.id AS TEXT))
                        END
                    WHERE e.embedding IS NOT NULL
                    """
                    
                    # Execute query
                    params = [
                        entity_type if entity_type != 'document' else 'document',
                        id_prefix,
                        id_prefix,
                        entity_type if entity_type != 'document' else table_name.replace('_documents', '')
                    ]
                    
                    for row in conn.execute(query_sql, params):
                        # Convert Row to dict
                        row_dict = dict(row)
                        
                        # Load embedding
                        entity_embedding = load_embedding_from_blob(row_dict['embedding'])
                        if entity_embedding is None:
                            continue
                        
                        # Calculate similarity
                        similarity = cosine_similarity(query_embedding, entity_embedding)
                        
                        # Build result
                        result = {
                            'entity_type': entity_type,
                            'entity_id': f"{id_prefix}_{row_dict['id']}" if id_prefix else f"{entity_type}_{row_dict['id']}",
                            'name': row_dict.get('title', row_dict.get('name', 'Unknown')),
                            'similarity': float(similarity)
                        }
                        
                        # Add description if available
                        if row_dict.get('description'):
                            result['description'] = row_dict['description']
                        elif row_dict.get('content'):
                            result['description'] = row_dict['content'][:500]
                        
                        # Add date for documents
                        if row_dict.get('date'):
                            result['date'] = row_dict['date']
                        
                        # Add category if available
                        if row_dict.get('category'):
                            result['category'] = row_dict['category']
                        
                        results.append(result)
            
            # Sort by similarity and limit
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
        finally:
            if conn:
                conn.close()


def load_embedding_from_blob(blob: bytes) -> Optional[np.ndarray]:
    """
    Convert stored BLOB back to numpy array.
    
    Args:
        blob: Binary data from database
        
    Returns:
        Numpy array or None if conversion failed
    """
    try:
        if not blob:
            return None
        return np.frombuffer(blob, dtype=np.float32)
    except Exception as e:
        logger.error(f"Error loading embedding from blob: {e}")
        return None


def get_db_connection(db_path: str) -> sqlite3.Connection:
    """
    Get database connection with proper configuration.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        SQLite connection with row factory
    """
    try:
        if not Path(db_path).exists():
            raise FileNotFoundError(f"Database not found at {db_path}")
            
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def semantic_search_chunks(db_path: str, query: str, limit: int = 5, 
                          doc_type: Optional[str] = None, 
                          similarity_threshold: float = 0.5,
                          include_metadata: bool = True) -> List[Dict[str, Any]]:
    """
    Search document chunks using semantic similarity.
    
    This function performs semantic search across document chunks using OpenAI embeddings
    to find the most relevant content for a given query. It supports filtering by document
    type and provides rich metadata about each result.
    
    Args:
        db_path: Path to the SQLite database
        query: Search query text
        limit: Maximum number of results to return
        doc_type: Filter by document type (academic/chronicle)
        similarity_threshold: Minimum similarity score (0.0-1.0)
        include_metadata: Whether to include document metadata
    
    Returns:
        List of chunk results sorted by similarity score
    """
    if not OPENAI_AVAILABLE:
        logger.warning("Semantic search not available - OpenAI client not initialized")
        return []
    
    try:
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            logger.error("Failed to generate query embedding")
            return []
        
        conn = get_db_connection(db_path)
        
        # Build query based on filters
        base_query = """
            SELECT 
                dc.id as chunk_id,
                dc.document_id,
                dc.document_type,
                dc.chunk_index,
                dc.content,
                dc.start_char,
                dc.end_char,
                e.embedding
        """
        
        if include_metadata:
            base_query += """
                ,COALESCE(ad.title, cd.title) as document_title,
                COALESCE(ad.date, cd.date) as document_date
            """
        
        base_query += """
            FROM document_chunks dc
            JOIN embeddings e ON e.entity_id = ('chunk_' || dc.id) AND e.entity_type = 'chunk'
        """
        
        if include_metadata:
            base_query += """
                LEFT JOIN academic_documents ad ON dc.document_type = 'academic' AND dc.document_id = ad.id
                LEFT JOIN chronicle_documents cd ON dc.document_type = 'chronicle' AND dc.document_id = cd.id
            """
        
        base_query += " WHERE e.embedding IS NOT NULL"
        
        params = []
        if doc_type:
            base_query += " AND dc.document_type = ?"
            params.append(doc_type)
        
        logger.info(f"Searching {doc_type or 'all'} chunks for: '{query}'")
        
        results = []
        for row in conn.execute(base_query, params):
            # Extract data safely
            chunk_embedding = load_embedding_from_blob(row['embedding'])
            if chunk_embedding is None:
                continue
                
            # Calculate similarity
            similarity = cosine_similarity(query_embedding, chunk_embedding)
            
            if similarity >= similarity_threshold:
                result = {
                    'chunk_id': row['chunk_id'],
                    'document_id': row['document_id'],
                    'document_type': row['document_type'],
                    'chunk_index': row['chunk_index'],
                    'content': row['content'],
                    'similarity': float(similarity),
                    'start_char': row['start_char'],
                    'end_char': row['end_char']
                }
                
                if include_metadata:
                    result.update({
                        'document_title': row['document_title'] if row['document_title'] else 'Unknown',
                        'document_date': row['document_date'] if row['document_date'] else 'Unknown'
                    })
                
                results.append(result)
        
        conn.close()
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x['similarity'], reverse=True)
        final_results = results[:limit]
        
        logger.info(f"Found {len(final_results)} relevant chunks (threshold: {similarity_threshold})")
        return final_results
        
    except Exception as e:
        logger.error(f"Semantic search error: {e}")
        return []


def find_similar_entities(db_path: str, query: str, entity_type: Optional[str] = None, 
                         limit: int = 10, similarity_threshold: float = 0.6) -> List[Dict[str, Any]]:
    """
    Find entities similar to the query using embeddings.
    
    This function searches across all entity types (topics, people, methods, etc.)
    to find semantically similar entities based on the query. It's useful for
    discovering related concepts and expanding query context.
    
    Args:
        db_path: Path to the SQLite database
        query: Search query text
        entity_type: Filter by entity type (topic/person/method/etc)
        limit: Maximum number of results to return
        similarity_threshold: Minimum similarity score (0.0-1.0)
    
    Returns:
        List of similar entities with metadata and similarity scores
    """
    if not OPENAI_AVAILABLE:
        logger.warning("Entity search not available - OpenAI client not initialized")
        return []
    
    try:
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            logger.error("Failed to generate query embedding")
            return []
        
        conn = get_db_connection(db_path)
        
        # Build query based on filters
        base_query = """
            SELECT 
                e.entity_id,
                e.entity_type,
                e.embedding
            FROM embeddings e
            WHERE e.embedding IS NOT NULL
        """
        
        params = []
        if entity_type:
            base_query += " AND e.entity_type = ?"
            params.append(entity_type)
        
        logger.info(f"Searching for entities similar to: '{query}' (type: {entity_type or 'all'})")
        
        results = []
        for row in conn.execute(base_query, params):
            entity_id, ent_type, embedding_blob = row
            
            # Calculate similarity
            entity_embedding = load_embedding_from_blob(embedding_blob)
            if entity_embedding is None:
                continue
                
            similarity = cosine_similarity(query_embedding, entity_embedding)
            
            if similarity >= similarity_threshold:
                # Get entity details based on type
                entity_details = _get_entity_details(conn, entity_id, ent_type)
                if entity_details:
                    result = {
                        'entity_id': entity_id,
                        'entity_type': ent_type,
                        'similarity': float(similarity)
                    }
                    result.update(entity_details)
                    results.append(result)
        
        conn.close()
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x['similarity'], reverse=True)
        final_results = results[:limit]
        
        logger.info(f"Found {len(final_results)} similar entities (threshold: {similarity_threshold})")
        return final_results
        
    except Exception as e:
        logger.error(f"Entity search error: {e}")
        return []


def _get_entity_details(conn: sqlite3.Connection, entity_id: str, entity_type: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about an entity based on its type.
    
    Args:
        conn: Database connection
        entity_id: Entity ID
        entity_type: Type of entity
        
    Returns:
        Dictionary with entity details or None if not found
    """
    try:
        # Extract numeric ID from entity_id format like "topic_123"
        if '_' in entity_id:
            numeric_id = entity_id.split('_')[-1]
        else:
            numeric_id = entity_id
            
        if entity_type == 'topic':
            query = "SELECT name, category, description FROM topics WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                return {
                    'name': row[0],
                    'category': row[1],
                    'description': row[2]
                }
        elif entity_type == 'person':
            query = "SELECT name, role, affiliation FROM people WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                return {
                    'name': row[0],
                    'role': row[1],
                    'affiliation': row[2]
                }
        elif entity_type == 'method':
            query = "SELECT name, category, description FROM methods WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                return {
                    'name': row[0],
                    'category': row[1],
                    'description': row[2]
                }
        elif entity_type == 'project':
            query = "SELECT name, description, start_date, end_date FROM projects WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                # Determine status from dates
                status = 'active' if not row[3] else 'completed'
                return {
                    'name': row[0],
                    'description': row[1],
                    'status': status,
                    'start_date': row[2],
                    'end_date': row[3]
                }
        elif entity_type == 'institution':
            query = "SELECT name, type, location FROM institutions WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                return {
                    'name': row[0],
                    'type': row[1],
                    'location': row[2]
                }
        elif entity_type == 'application':
            query = "SELECT name, domain, description FROM applications WHERE id = ?"
            row = conn.execute(query, (numeric_id,)).fetchone()
            if row:
                return {
                    'name': row[0],
                    'domain': row[1],
                    'description': row[2]
                }
    except Exception as e:
        logger.error(f"Error getting entity details for {entity_type} {entity_id}: {e}")
    
    return None


def semantic_search_documents(db_path: str, query: str, limit: int = 5,
                             doc_type: Optional[str] = None,
                             similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Search full documents using semantic similarity.
    
    This function searches at the document level rather than chunk level,
    providing broader context for queries that need full document understanding.
    
    Args:
        db_path: Path to the SQLite database
        query: Search query text
        limit: Maximum number of results to return
        doc_type: Filter by document type (academic/chronicle)
        similarity_threshold: Minimum similarity score (0.0-1.0)
        
    Returns:
        List of document results sorted by similarity score
    """
    if not OPENAI_AVAILABLE:
        logger.warning("Document search not available - OpenAI client not initialized")
        return []
    
    try:
        query_embedding = generate_embedding(query)
        if query_embedding is None:
            logger.error("Failed to generate query embedding")
            return []
        
        conn = get_db_connection(db_path)
        
        # Search document-level embeddings - handle split tables
        base_query = """
            SELECT 
                'academic' as document_type,
                ad.id,
                ad.title,
                ad.date,
                ad.content,
                e.embedding
            FROM academic_documents ad
            JOIN embeddings e ON e.entity_id = ('academic_' || ad.id) AND e.entity_type = 'document'
            WHERE e.embedding IS NOT NULL
            
            UNION ALL
            
            SELECT 
                'chronicle' as document_type,
                cd.id,
                cd.title,
                cd.date,
                cd.content,
                e.embedding
            FROM chronicle_documents cd
            JOIN embeddings e ON e.entity_id = ('chronicle_' || cd.id) AND e.entity_type = 'document'
            WHERE e.embedding IS NOT NULL
        """
        
        # Handle doc_type filtering by modifying the query before UNION
        if doc_type:
            if doc_type == 'academic':
                base_query = """
                    SELECT 
                        'academic' as document_type,
                        ad.id,
                        ad.title,
                        ad.date,
                        ad.content,
                        e.embedding
                    FROM academic_documents ad
                    JOIN embeddings e ON e.entity_id = ('academic_' || ad.id) AND e.entity_type = 'document'
                    WHERE e.embedding IS NOT NULL
                """
            elif doc_type == 'chronicle':
                base_query = """
                    SELECT 
                        'chronicle' as document_type,
                        cd.id,
                        cd.title,
                        cd.date,
                        cd.content,
                        e.embedding
                    FROM chronicle_documents cd
                    JOIN embeddings e ON e.entity_id = ('chronicle_' || cd.id) AND e.entity_type = 'document'
                    WHERE e.embedding IS NOT NULL
                """
        
        params = []
        
        logger.info(f"Searching {doc_type or 'all'} documents for: '{query}'")
        
        results = []
        for row in conn.execute(base_query, params):
            # Extract data safely
            doc_embedding = load_embedding_from_blob(row['embedding'])
            if doc_embedding is None:
                continue
                
            # Calculate similarity
            similarity = cosine_similarity(query_embedding, doc_embedding)
            
            if similarity >= similarity_threshold:
                # Extract excerpt around query terms for preview
                content = row['content'] or ''
                excerpt = _extract_relevant_excerpt(content, query, max_length=300)
                
                results.append({
                    'document_id': row['id'],
                    'title': row['title'],
                    'date': row['date'],
                    'document_type': row['document_type'],
                    'similarity': float(similarity),
                    'excerpt': excerpt,
                    'content_length': len(content)
                })
        
        conn.close()
        
        # Sort by similarity and limit
        results.sort(key=lambda x: x['similarity'], reverse=True)
        final_results = results[:limit]
        
        logger.info(f"Found {len(final_results)} relevant documents (threshold: {similarity_threshold})")
        return final_results
        
    except Exception as e:
        logger.error(f"Document search error: {e}")
        return []


def _extract_relevant_excerpt(content: str, query: str, max_length: int = 300) -> str:
    """
    Extract a relevant excerpt from content based on query terms.
    
    Args:
        content: Full content text
        query: Search query
        max_length: Maximum excerpt length
        
    Returns:
        Relevant excerpt string
    """
    if not content:
        return ""
    
    query_terms = query.lower().split()
    content_lower = content.lower()
    
    # Find the first occurrence of any query term
    best_pos = -1
    for term in query_terms:
        pos = content_lower.find(term)
        if pos >= 0 and (best_pos == -1 or pos < best_pos):
            best_pos = pos
    
    if best_pos >= 0:
        # Extract around the found position
        start = max(0, best_pos - max_length // 3)
        end = min(len(content), start + max_length)
        excerpt = content[start:end]
        
        # Try to start and end at word boundaries
        if start > 0:
            first_space = excerpt.find(' ')
            if first_space > 0:
                excerpt = excerpt[first_space + 1:]
        
        if end < len(content):
            last_space = excerpt.rfind(' ')
            if last_space > 0:
                excerpt = excerpt[:last_space]
        
        return excerpt.strip()
    else:
        # No query terms found, return beginning
        return content[:max_length].strip()


def hybrid_search(db_path: str, query: str, limit: int = 10,
                 chunk_weight: float = 0.6, entity_weight: float = 0.4,
                 similarity_threshold: float = 0.5) -> Dict[str, List[Dict[str, Any]]]:
    """
    Perform hybrid search combining chunks and entities.
    
    This function combines semantic search across both document chunks and entities
    to provide comprehensive results that include both content and related concepts.
    
    Args:
        db_path: Path to the SQLite database
        query: Search query text
        limit: Maximum number of results per category
        chunk_weight: Weight for chunk results (0.0-1.0)
        entity_weight: Weight for entity results (0.0-1.0)
        similarity_threshold: Minimum similarity score
        
    Returns:
        Dictionary with separate lists of chunk and entity results
    """
    logger.info(f"Performing hybrid search for: '{query}'")
    
    # Search chunks
    chunk_results = semantic_search_chunks(
        db_path, query, limit=limit, 
        similarity_threshold=similarity_threshold
    )
    
    # Search entities  
    entity_results = find_similar_entities(
        db_path, query, limit=limit,
        similarity_threshold=similarity_threshold
    )
    
    # Apply weights to similarity scores
    for result in chunk_results:
        result['weighted_similarity'] = result['similarity'] * chunk_weight
        
    for result in entity_results:
        result['weighted_similarity'] = result['similarity'] * entity_weight
    
    return {
        'chunks': chunk_results,
        'entities': entity_results,
        'total_results': len(chunk_results) + len(entity_results)
    }