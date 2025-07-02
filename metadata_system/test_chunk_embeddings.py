#!/usr/bin/env python3
"""Test chunk embeddings generation and search."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import numpy as np
from embeddings import EmbeddingGenerator

def test_chunk_embeddings():
    generator = EmbeddingGenerator()
    
    print("=== Testing Chunk Embeddings ===\n")
    
    # Only generate embeddings for first 5 chunks as a test
    print("Generating embeddings for first 5 chunks...")
    conn = generator.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM document_chunks WHERE embedding IS NULL LIMIT 5")
    chunk_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    for chunk_id in chunk_ids:
        # Generate embedding for specific chunk
        conn = generator.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.chunk_title, c.chunk_content, d.title as doc_title
            FROM document_chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.id = ?
        """, (chunk_id,))
        chunk = cursor.fetchone()
        
        if chunk:
            text = f"Document: {chunk['doc_title']}\n"
            text += f"Section: {chunk['chunk_title']}\n"
            text += f"Content: {chunk['chunk_content'][:1000]}"
            
            embedding = generator.generate_embedding(text)
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            cursor.execute("UPDATE document_chunks SET embedding = ? WHERE id = ?", 
                         (embedding_bytes, chunk_id))
            conn.commit()
            print(f"✓ Generated embedding for: {chunk['chunk_title']}")
        
        conn.close()
    
    print("\n=== Testing Chunk Search ===\n")
    
    # Test queries
    test_queries = [
        "Hellinger-Kantorovich distance and optimal transport",
        "convergence theorems and proofs",
        "neural networks and deep learning applications",
        "risk-sensitive control and reinforcement learning",
        "large deviation principles"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        similar_chunks = generator.find_similar_chunks(query, top_k=3)
        
        if similar_chunks:
            print("Top matching sections:")
            for chunk_id, similarity, chunk_title, doc_title in similar_chunks:
                print(f"  - [{similarity:.3f}] {chunk_title}")
                print(f"    From: {doc_title[:60]}...")
        else:
            print("  No results found")


if __name__ == "__main__":
    test_chunk_embeddings()