#!/usr/bin/env python3
"""
Generate embeddings for chronicle documents and their chunks.
Run this after process_chronicle_notes.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def generate_chronicle_embeddings(db_path: str = "DB/metadata.db"):
    """Generate embeddings for all chronicle documents"""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENAI_API_KEY in your .env file")
        exit(1)
    
    print("Generating embeddings for chronicle documents...")
    print("=" * 80)
    
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
    conn = sqlite3.connect(db_path)
    
    # Get all chronicle documents without embeddings
    cursor = conn.execute("""
        SELECT cd.id, cd.title, cd.content
        FROM chronicle_documents cd
        LEFT JOIN embeddings e ON e.entity_type = 'document' 
            AND e.entity_id = 'chronicle_' || cd.id
        WHERE e.id IS NULL
    """)
    
    documents = cursor.fetchall()
    print(f"Found {len(documents)} chronicle documents without embeddings")
    
    embeddings_created = 0
    
    for doc_id, title, content in documents:
        print(f"\nProcessing: {title}")
        
        try:
            # Generate embedding for the full document
            doc_embedding = embeddings_model.embed_documents([content])[0]
            
            # Store embedding
            conn.execute("""
                INSERT OR REPLACE INTO embeddings (
                    entity_type, entity_id, embedding, model_name
                ) VALUES (?, ?, ?, ?)
            """, ('document', f'chronicle_{doc_id}', 
                  json.dumps(doc_embedding), 'text-embedding-3-small'))
            
            embeddings_created += 1
            print(f"  ✓ Generated document embedding")
            
        except Exception as e:
            print(f"  ✗ Failed: {e}")
    
    # Also generate embeddings for entities from chronicle notes
    print("\nGenerating embeddings for chronicle entities...")
    
    # Topics from chronicle documents
    cursor = conn.execute("""
        SELECT DISTINCT t.id, t.name
        FROM topics t
        JOIN relationships r ON r.target_id = CAST(t.id AS TEXT) 
            AND r.target_type = 'topic'
        WHERE r.source_type = 'document' 
            AND r.source_id LIKE 'chronicle_%'
            AND NOT EXISTS (
                SELECT 1 FROM embeddings e 
                WHERE e.entity_type = 'topic' 
                AND e.entity_id = CAST(t.id AS TEXT)
            )
    """)
    
    topics = cursor.fetchall()
    print(f"Found {len(topics)} topics without embeddings")
    
    for topic_id, topic_name in topics:
        try:
            embedding = embeddings_model.embed_documents([topic_name])[0]
            conn.execute("""
                INSERT OR REPLACE INTO embeddings (
                    entity_type, entity_id, embedding, model_name
                ) VALUES (?, ?, ?, ?)
            """, ('topic', str(topic_id), 
                  json.dumps(embedding), 'text-embedding-3-small'))
            embeddings_created += 1
        except Exception as e:
            print(f"  ✗ Failed for topic '{topic_name}': {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Generated {embeddings_created} embeddings")
    return embeddings_created


def main():
    """Main function"""
    embeddings_created = generate_chronicle_embeddings()
    
    if embeddings_created > 0:
        print("\nNext steps:")
        print("1. View database: ./view_database.sh")
        print("2. Generate knowledge graph: python KG/knowledge_graph.py DB/metadata.db")
        print("3. Query with interactive agent: python interactive_agent.py")


if __name__ == "__main__":
    main()