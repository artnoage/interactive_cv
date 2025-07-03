#!/usr/bin/env python3
"""
Simple example showing how chunking preserves entity relationships
"""

def example_chunk_with_metadata():
    """
    This shows what a chunk looks like in our system
    """
    
    # Original analysis section
    full_section = """
    ## Mathematical Concepts
    
    The Hellinger-Kantorovich space (M(X), HK) is a metric space that 
    combines optimal transport with mass creation. Vaios Laschos and 
    Alexander Mielke proved that this space has a cone structure. The 
    key insight is that the Spherical Hellinger-Kantorovich distance 
    provides a natural metric on probability measures.
    
    This work builds on the Wasserstein distance theory and extends it
    to handle mass changes. The Local Angle Condition (LAC) transfers
    from the base space to the measure space, which is crucial for
    gradient flow theory.
    """
    
    # After chunking, chunk #3 might look like:
    chunk_in_db = {
        'id': 3,
        'document_id': 'academic_123',
        'content': """The key insight is that the Spherical Hellinger-Kantorovich distance 
provides a natural metric on probability measures.

This work builds on the Wasserstein distance theory and extends it
to handle mass changes.""",
        'section_name': 'Mathematical Concepts',
        'chunk_metadata': {
            'position': 'middle',
            'has_math': False,
            'has_citations': False
        }
    }
    
    # Entities found in this specific chunk
    chunk_entities = [
        {
            'chunk_id': 3,
            'entity_type': 'topic',
            'entity_id': 45,  # -> topics table: "Spherical Hellinger-Kantorovich distance"
            'relevance_score': 0.8
        },
        {
            'chunk_id': 3,
            'entity_type': 'topic', 
            'entity_id': 12,  # -> topics table: "Wasserstein distance"
            'relevance_score': 0.6
        },
        {
            'chunk_id': 3,
            'entity_type': 'topic',
            'entity_id': 89,  # -> topics table: "probability measures"
            'relevance_score': 0.7
        }
    ]
    
    # When RAG retrieves this chunk, it can:
    # 1. Use the chunk content for context
    # 2. Follow entity_ids to get full entity details
    # 3. Find related chunks through shared entities
    # 4. Include document metadata from academic_documents table
    
    print("Chunk Example:")
    print(f"Content: {chunk_in_db['content'][:100]}...")
    print(f"Section: {chunk_in_db['section_name']}")
    print(f"Entities in chunk: {len(chunk_entities)}")
    print("\nThis chunk discusses:")
    for entity in chunk_entities:
        print(f"  - Entity {entity['entity_id']} ({entity['entity_type']}) "
              f"with relevance {entity['relevance_score']}")


def show_rag_query_flow():
    """
    Shows how RAG uses chunks with metadata
    """
    
    # User query: "What distance metrics did Vaios work on?"
    
    print("\n" + "="*60)
    print("RAG Query Flow Example")
    print("="*60)
    print("User: 'What distance metrics did Vaios work on?'")
    print("\n1. Find Vaios in people table -> person_id: 23")
    print("2. Find documents by Vaios:")
    print("   SELECT * FROM relationships WHERE target_id = 23 AND relationship_type = 'authored_by'")
    print("   -> document academic_123")
    print("\n3. Find topics that are distance metrics in those documents:")
    print("   -> Hellinger-Kantorovich distance")
    print("   -> Spherical Hellinger-Kantorovich distance") 
    print("   -> Wasserstein distance")
    print("\n4. Find chunks mentioning these topics:")
    print("   -> chunk_ids: [3, 7, 12, 18]")
    print("\n5. Get embeddings and rank by relevance")
    print("6. Return top chunks with full context")


if __name__ == "__main__":
    example_chunk_with_metadata()
    show_rag_query_flow()