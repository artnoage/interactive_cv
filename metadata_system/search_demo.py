#!/usr/bin/env python3
"""Demo semantic search across documents and chunks."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from embeddings import EmbeddingGenerator

def search_demo():
    generator = EmbeddingGenerator()
    
    print("="*60)
    print("INTERACTIVE CV SEMANTIC SEARCH DEMO")
    print("="*60)
    
    # Test queries
    queries = [
        "optimal transport theory and Wasserstein distances",
        "reinforcement learning for game AI",
        "convergence proofs and mathematical analysis",
        "neural networks and deep learning applications",
        "daily work on Collapsi project"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-"*60)
        
        # Search chunks (more granular)
        print("\n📄 Most relevant sections:")
        chunks = generator.find_similar_chunks(query, top_k=3)
        for i, (chunk_id, similarity, chunk_title, doc_title) in enumerate(chunks, 1):
            print(f"{i}. [{similarity:.3f}] {chunk_title}")
            print(f"   From: {doc_title[:50]}...")
        
        # Search full documents
        print("\n📚 Most relevant documents:")
        docs = generator.find_similar_documents(query, top_k=3)
        for i, (doc_id, similarity, title) in enumerate(docs, 1):
            print(f"{i}. [{similarity:.3f}] {title[:60]}...")
    
    print("\n" + "="*60)
    print("✅ Search demo complete!")


if __name__ == "__main__":
    search_demo()