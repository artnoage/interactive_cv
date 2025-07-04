#!/usr/bin/env python3
"""
Embeddings generation using OpenAI API.
Stores embeddings in the dedicated embeddings table for semantic search.
"""

import os
import json
import sqlite3
import numpy as np
from typing import List, Optional, Tuple, Dict
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
    """Generate and manage embeddings for documents, chunks, and entities."""
    
    def __init__(self, db_path: str = "DB/metadata.db"):
        self.db_path = db_path
        
        # Initialize OpenAI embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
            
        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(api_key),
            model="text-embedding-3-small"  # Good balance of performance/cost
        )
        self.model_name = "text-embedding-3-small"
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def store_embedding(self, entity_type: str, entity_id: str, embedding: List[float]):
        """Store embedding in the embeddings table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Convert embedding to bytes for storage
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            # Insert or update embedding
            cursor.execute("""
                INSERT OR REPLACE INTO embeddings 
                (entity_type, entity_id, embedding, model_name)
                VALUES (?, ?, ?, ?)
            """, (entity_type, entity_id, embedding_bytes, self.model_name))
            
            conn.commit()
            logger.debug(f"Stored embedding for {entity_type}:{entity_id}")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error storing embedding: {e}")
            raise
        finally:
            conn.close()
    
    def prepare_document_text(self, doc_id: int, doc_type: str) -> Optional[str]:
        """Prepare document text for embedding."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get document details
            table = f"{doc_type}_documents"
            cursor.execute(f"""
                SELECT title, content, date 
                FROM {table} 
                WHERE id = ?
            """, (doc_id,))
            
            doc = cursor.fetchone()
            if not doc:
                return None
            
            # Build text representation
            text_parts = [f"Title: {doc['title']}"]
            
            if doc['date']:
                text_parts.append(f"Date: {doc['date']}")
            
            # Add content preview (first 2000 chars)
            if doc['content']:
                text_parts.append(f"Content:\n{doc['content'][:2000]}")
            
            # Add related entities
            unified_id = f"{doc_type}_{doc_id}"
            cursor.execute("""
                SELECT target_type, target_id, relationship_type
                FROM relationships
                WHERE source_type = 'document' AND source_id = ?
                LIMIT 20
            """, (unified_id,))
            
            relationships = cursor.fetchall()
            if relationships:
                entities_by_type = {}
                for rel in relationships:
                    entity_type = rel['target_type']
                    if entity_type not in entities_by_type:
                        entities_by_type[entity_type] = []
                    
                    # Get entity name
                    table_map = {
                        'topic': 'topics',
                        'person': 'people',
                        'project': 'projects',
                        'institution': 'institutions',
                        'method': 'methods',
                        'application': 'applications'
                    }
                    
                    if entity_type in table_map:
                        entity_table = table_map[entity_type]
                        cursor.execute(f"SELECT name FROM {entity_table} WHERE id = ?", 
                                     (rel['target_id'],))
                        result = cursor.fetchone()
                        if result:
                            entities_by_type[entity_type].append(result['name'])
                
                # Add entities to text
                if entities_by_type.get('topic'):
                    text_parts.append(f"Topics: {', '.join(entities_by_type['topic'][:10])}")
                if entities_by_type.get('person'):
                    text_parts.append(f"People: {', '.join(entities_by_type['person'][:5])}")
                if entities_by_type.get('method'):
                    text_parts.append(f"Methods: {', '.join(entities_by_type['method'][:5])}")
            
            return '\n'.join(text_parts)
            
        finally:
            conn.close()
    
    def prepare_chunk_text(self, chunk_id: int) -> Optional[str]:
        """Prepare chunk text for embedding."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get chunk details
            cursor.execute("""
                SELECT c.content, c.section_name, c.document_type, c.document_id
                FROM document_chunks c
                WHERE c.id = ?
            """, (chunk_id,))
            
            chunk = cursor.fetchone()
            if not chunk:
                return None
            
            # Get document title
            table = f"{chunk['document_type']}_documents"
            cursor.execute(f"SELECT title FROM {table} WHERE id = ?", 
                         (chunk['document_id'],))
            doc = cursor.fetchone()
            
            # Build text representation
            text_parts = []
            if doc:
                text_parts.append(f"Document: {doc['title']}")
            if chunk['section_name']:
                text_parts.append(f"Section: {chunk['section_name']}")
            text_parts.append(f"Content:\n{chunk['content']}")
            
            return '\n'.join(text_parts)
            
        finally:
            conn.close()
    
    def prepare_entity_text(self, entity_type: str, entity_id: int) -> Optional[str]:
        """Prepare entity text for embedding."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Map entity types to tables
            table_map = {
                'topic': 'topics',
                'person': 'people',
                'project': 'projects',
                'institution': 'institutions',
                'method': 'methods',
                'application': 'applications'
            }
            
            if entity_type not in table_map:
                return None
            
            table = table_map[entity_type]
            
            # Get entity details
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (entity_id,))
            entity_row = cursor.fetchone()
            
            if not entity_row:
                return None
            
            # Convert Row to dict
            entity = dict(entity_row)
            
            # Build text representation
            text_parts = [f"{entity_type.title()}: {entity['name']}"]
            
            # Add additional fields based on entity type
            if entity_type == 'topic' and entity.get('category'):
                text_parts.append(f"Category: {entity['category']}")
            elif entity_type == 'person':
                if entity.get('role'):
                    text_parts.append(f"Role: {entity['role']}")
                if entity.get('affiliation'):
                    text_parts.append(f"Affiliation: {entity['affiliation']}")
            elif entity_type == 'method' and entity.get('category'):
                text_parts.append(f"Type: {entity['category']}")
            elif entity_type == 'application' and entity.get('domain'):
                text_parts.append(f"Domain: {entity['domain']}")
            
            # Add description if available
            if entity.get('description'):
                text_parts.append(f"Description: {entity['description']}")
            
            # Add related documents
            cursor.execute("""
                SELECT source_id, relationship_type
                FROM relationships
                WHERE target_type = ? AND target_id = ?
                AND source_type = 'document'
                LIMIT 10
            """, (entity_type, str(entity_id)))
            
            doc_relationships = cursor.fetchall()
            if doc_relationships:
                doc_titles = []
                for rel in doc_relationships:
                    doc_type, doc_id = rel['source_id'].split('_')
                    table = f"{doc_type}_documents"
                    cursor.execute(f"SELECT title FROM {table} WHERE id = ?", (doc_id,))
                    doc = cursor.fetchone()
                    if doc:
                        doc_titles.append(doc['title'])
                
                if doc_titles:
                    text_parts.append(f"Mentioned in: {', '.join(doc_titles[:5])}")
            
            return '\n'.join(text_parts)
            
        finally:
            conn.close()
    
    def generate_document_embeddings(self) -> int:
        """Generate embeddings for all documents."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        count = 0
        
        try:
            # Process academic documents
            cursor.execute("SELECT id FROM academic_documents")
            for row in cursor.fetchall():
                doc_id = row['id']
                entity_id = f"academic_{doc_id}"
                
                # Check if embedding already exists
                cursor.execute("""
                    SELECT 1 FROM embeddings 
                    WHERE entity_type = 'document' AND entity_id = ?
                """, (entity_id,))
                
                if not cursor.fetchone():
                    text = self.prepare_document_text(doc_id, 'academic')
                    if text:
                        embedding = self.generate_embedding(text)
                        self.store_embedding('document', entity_id, embedding)
                        count += 1
                        logger.info(f"Generated embedding for academic document {doc_id}")
            
            # Process chronicle documents
            cursor.execute("SELECT id FROM chronicle_documents")
            for row in cursor.fetchall():
                doc_id = row['id']
                entity_id = f"chronicle_{doc_id}"
                
                # Check if embedding already exists
                cursor.execute("""
                    SELECT 1 FROM embeddings 
                    WHERE entity_type = 'document' AND entity_id = ?
                """, (entity_id,))
                
                if not cursor.fetchone():
                    text = self.prepare_document_text(doc_id, 'chronicle')
                    if text:
                        embedding = self.generate_embedding(text)
                        self.store_embedding('document', entity_id, embedding)
                        count += 1
                        logger.info(f"Generated embedding for chronicle document {doc_id}")
            
            return count
            
        finally:
            conn.close()
    
    def generate_chunk_embeddings(self) -> int:
        """Generate embeddings for all chunks."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        count = 0
        
        try:
            # Get all chunks
            cursor.execute("SELECT id FROM document_chunks")
            chunk_ids = [row['id'] for row in cursor.fetchall()]
            
            for chunk_id in chunk_ids:
                entity_id = f"chunk_{chunk_id}"
                
                # Check if embedding already exists
                cursor.execute("""
                    SELECT 1 FROM embeddings 
                    WHERE entity_type = 'chunk' AND entity_id = ?
                """, (entity_id,))
                
                if not cursor.fetchone():
                    text = self.prepare_chunk_text(chunk_id)
                    if text:
                        embedding = self.generate_embedding(text)
                        self.store_embedding('chunk', entity_id, embedding)
                        count += 1
                        
                        if count % 10 == 0:
                            logger.info(f"Generated {count} chunk embeddings...")
            
            logger.info(f"Generated embeddings for {count} chunks")
            return count
            
        finally:
            conn.close()
    
    def generate_entity_embeddings(self) -> int:
        """Generate embeddings for all entities."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        count = 0
        
        entity_types = [
            ('topic', 'topics'),
            ('person', 'people'),
            ('project', 'projects'),
            ('institution', 'institutions'),
            ('method', 'methods'),
            ('application', 'applications')
        ]
        
        try:
            for entity_type, table in entity_types:
                cursor.execute(f"SELECT id FROM {table}")
                entity_ids = [row['id'] for row in cursor.fetchall()]
                
                for entity_id in entity_ids:
                    entity_str_id = f"{entity_type}_{entity_id}"
                    
                    # Check if embedding already exists
                    cursor.execute("""
                        SELECT 1 FROM embeddings 
                        WHERE entity_type = ? AND entity_id = ?
                    """, (entity_type, entity_str_id))
                    
                    if not cursor.fetchone():
                        text = self.prepare_entity_text(entity_type, entity_id)
                        if text:
                            embedding = self.generate_embedding(text)
                            self.store_embedding(entity_type, entity_str_id, embedding)
                            count += 1
                            
                            if count % 20 == 0:
                                logger.info(f"Generated {count} entity embeddings...")
            
            logger.info(f"Generated embeddings for {count} entities")
            return count
            
        finally:
            conn.close()
    
    def find_similar(self, query_text: str, entity_type: Optional[str] = None, 
                    top_k: int = 10) -> List[Dict]:
        """Find similar entities using cosine similarity."""
        try:
            # Generate query embedding
            query_embedding = np.array(self.generate_embedding(query_text), dtype=np.float32)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build query based on entity type filter
            if entity_type:
                cursor.execute("""
                    SELECT entity_type, entity_id, embedding
                    FROM embeddings
                    WHERE entity_type = ?
                """, (entity_type,))
            else:
                cursor.execute("""
                    SELECT entity_type, entity_id, embedding
                    FROM embeddings
                """)
            
            results = []
            for row in cursor.fetchall():
                # Convert bytes back to numpy array
                embedding = np.frombuffer(row['embedding'], dtype=np.float32)
                
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                )
                
                results.append({
                    'entity_type': row['entity_type'],
                    'entity_id': row['entity_id'],
                    'similarity': float(similarity)
                })
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            conn.close()
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar entities: {e}")
            raise
    
    def generate_entity_embeddings_with_verification(self) -> int:
        """Generate embeddings for all entities with verification steps."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("ENTITY EMBEDDING GENERATION WITH VERIFICATION")
        print("="*60)
        
        entity_types = [
            ('topic', 'topics'),
            ('person', 'people'),
            ('project', 'projects'),
            ('institution', 'institutions'),
            ('method', 'methods'),
            ('application', 'applications')
        ]
        
        total_count = 0
        
        try:
            for entity_type, table in entity_types:
                print(f"\n\n--- Processing {entity_type.upper()} entities ---")
                
                # Get count of entities
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                total_entities = cursor.fetchone()[0]
                
                # Check existing embeddings
                cursor.execute("""
                    SELECT COUNT(*) FROM embeddings 
                    WHERE entity_type = ?
                """, (entity_type,))
                existing_embeddings = cursor.fetchone()[0]
                
                print(f"Total {entity_type}s: {total_entities}")
                print(f"Existing embeddings: {existing_embeddings}")
                print(f"Need to generate: {total_entities - existing_embeddings}")
                
                # Show sample entities
                cursor.execute(f"""
                    SELECT id, name FROM {table} 
                    ORDER BY RANDOM() 
                    LIMIT 5
                """)
                samples = cursor.fetchall()
                
                print(f"\nSample {entity_type}s:")
                for sample in samples:
                    print(f"  - {sample['name']}")
                
                # Ask for confirmation
                if total_entities - existing_embeddings > 0:
                    response = input(f"\nGenerate embeddings for {total_entities - existing_embeddings} {entity_type}s? (y/n): ")
                    if response.lower() != 'y':
                        print(f"Skipping {entity_type} embeddings")
                        continue
                    
                    # Generate embeddings
                    count = 0
                    cursor.execute(f"SELECT id FROM {table}")
                    entity_ids = [row['id'] for row in cursor.fetchall()]
                    
                    for entity_id in entity_ids:
                        entity_str_id = f"{entity_type}_{entity_id}"
                        
                        # Check if embedding already exists
                        cursor.execute("""
                            SELECT 1 FROM embeddings 
                            WHERE entity_type = ? AND entity_id = ?
                        """, (entity_type, entity_str_id))
                        
                        if not cursor.fetchone():
                            text = self.prepare_entity_text(entity_type, entity_id)
                            if text:
                                embedding = self.generate_embedding(text)
                                self.store_embedding(entity_type, entity_str_id, embedding)
                                count += 1
                                
                                if count % 20 == 0:
                                    print(f"  Generated {count} {entity_type} embeddings...")
                    
                    print(f"✓ Generated {count} embeddings for {entity_type}s")
                    total_count += count
                else:
                    print(f"✓ All {entity_type} embeddings already exist")
            
            print(f"\n\nTotal embeddings generated: {total_count}")
            return total_count
            
        finally:
            conn.close()
    
    def generate_all_embeddings(self, verify: bool = False) -> Dict[str, int]:
        """Generate all embeddings with optional verification."""
        results = {}
        
        print("\n" + "="*60)
        print("GENERATING ALL EMBEDDINGS")
        print("="*60)
        
        # Documents
        print("\n1. Generating document embeddings...")
        results['documents'] = self.generate_document_embeddings()
        
        # Chunks
        print("\n2. Generating chunk embeddings...")
        results['chunks'] = self.generate_chunk_embeddings()
        
        # Entities
        print("\n3. Generating entity embeddings...")
        if verify:
            results['entities'] = self.generate_entity_embeddings_with_verification()
        else:
            results['entities'] = self.generate_entity_embeddings()
        
        print("\n" + "="*60)
        print("EMBEDDING GENERATION COMPLETE")
        print("="*60)
        print(f"Documents: {results['documents']}")
        print(f"Chunks: {results['chunks']}")
        print(f"Entities: {results['entities']}")
        print(f"Total: {sum(results.values())}")
        
        return results


def main():
    """Main entry point for embedding generation."""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='Generate embeddings for database entities')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (in DB folder)')
    parser.add_argument('--entities-only', action='store_true',
                       help='Generate only entity embeddings')
    parser.add_argument('--verify', action='store_true',
                       help='Enable verification prompts for entity embeddings')
    parser.add_argument('--skip-documents', action='store_true',
                       help='Skip document embeddings')
    parser.add_argument('--skip-chunks', action='store_true',
                       help='Skip chunk embeddings')
    
    args = parser.parse_args()
    
    # Ensure we're working in the DB directory
    db_path = Path(__file__).parent / args.db
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return 1
    
    try:
        generator = EmbeddingGenerator(str(db_path))
        
        if args.entities_only:
            # Generate only entity embeddings
            if args.verify:
                count = generator.generate_entity_embeddings_with_verification()
            else:
                count = generator.generate_entity_embeddings()
            print(f"\nGenerated {count} entity embeddings")
        else:
            # Generate all embeddings
            results = generator.generate_all_embeddings(verify=args.verify)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

