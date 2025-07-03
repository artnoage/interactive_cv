# Chunking and Metadata Extraction Strategy - Note to Future Self

## Overview
This document explains our approach to processing academic papers for the Interactive CV system. We use a multi-stage pipeline that preserves full context during extraction while enabling efficient retrieval through chunking.

## The Problem
When building a RAG system from academic papers, we need to:
1. Extract rich metadata (concepts, relationships, people, etc.)
2. Enable semantic search through chunks
3. Maintain connections between related concepts
4. Avoid duplicating information

## Our Solution: Extract First, Chunk Later

### Core Principle
**Metadata extraction requires full document context, but retrieval works best with focused chunks.**

### Pipeline Architecture
```
1. Raw Paper (PDF/MD)
       ↓
2. Academic Analyzer (Pro Model)
       ↓
3. Complete Analysis Document (with all 3 phases)
       ↓
4. Academic Extractor (Pro Model) ← Extracts from FULL document
       ↓
5. Database Population
       ├── Entities (topics, people, methods, etc.)
       ├── Relationships (who mentions what, collaborations)
       └── Full document stored
       ↓
6. Document Chunker
       ├── Splits into semantic chunks
       ├── Identifies entities IN EACH CHUNK
       └── Preserves section context
       ↓
7. Embeddings Generator
       ├── Full document embedding
       ├── Chunk embeddings
       └── Entity embeddings
```

## Why This Order Matters

### Extraction Before Chunking
- **Cross-document references**: A method introduced on page 2 might be applied on page 10
- **Relationship discovery**: Collaborations mentioned in acknowledgments connect to work throughout
- **Concept hierarchies**: Parent concepts defined early, children scattered throughout
- **Complete understanding**: The extractor sees the full narrative arc

### Chunking After Extraction
- **Already have metadata**: No need to re-extract from chunks
- **Optimal chunk boundaries**: Can split at semantic boundaries without losing relationships
- **Local context**: Each chunk knows which pre-extracted entities it contains
- **Efficient retrieval**: Small chunks with rich metadata pointers

## Database Design Decisions

### Chunk Storage Strategy
```sql
-- Chunks store content + local context
document_chunks:
- id
- document_id
- content (text)
- section_name (e.g., "Mathematical Concepts")
- chunk_metadata (JSON with local properties)

-- Separate table for chunk-entity mappings
chunk_entities:
- chunk_id
- entity_type ('topic', 'person', etc.)
- entity_id
- relevance_score (how relevant is this entity to this chunk)
```

### Why Not Embed Metadata in Chunks?
1. **Single source of truth**: Entity details live in one place
2. **Updates propagate**: Change a person's affiliation once, reflects everywhere
3. **Efficient storage**: No duplicate metadata across chunks
4. **Flexible queries**: Can query chunks by entities or entities by chunks

## Chunking Strategy Details

### Chunk Size
- Target: 1000-1500 tokens (optimal for embeddings)
- Respect sentence boundaries
- Try to keep paragraphs together

### Section Awareness
- Preserve section headers in chunks
- Include section context in chunk_metadata
- Don't split mid-proof or mid-algorithm

### Entity Detection in Chunks
After chunking, scan each chunk to identify:
- Which topics/concepts are mentioned
- Which people are referenced
- Which methods are discussed
- Store these in chunk_entities with relevance scores

## RAG Query Flow

When a user asks: "What did Vaios work on with optimal transport?"

1. **Entity Recognition**: Identify "Vaios" (person) and "optimal transport" (topic)
2. **Relationship Query**: Find documents linking these entities
3. **Chunk Retrieval**: Get chunks from those documents mentioning both
4. **Semantic Search**: Use embeddings to rank chunk relevance
5. **Context Assembly**: Include document metadata + chunk content
6. **Response Generation**: LLM uses rich context to answer

## Benefits of This Approach

1. **Accuracy**: Full-document extraction catches all relationships
2. **Efficiency**: Chunks are small for fast retrieval
3. **Flexibility**: Can query by entities, embeddings, or both
4. **Maintainability**: Clear separation of concerns
5. **Scalability**: Can process documents in parallel after extraction

## Implementation Notes

### Order of Operations
1. Always run analyzer first (needs raw paper)
2. Always run extractor on complete analysis (needs full context)
3. Store document and metadata atomically (transaction)
4. Chunk after metadata is safely stored
5. Generate embeddings last (can be regenerated)

### Error Handling
- If extraction fails: Keep document, mark as "extraction_failed"
- If chunking fails: Document and metadata still usable
- If embedding fails: Can retry without losing data

### Performance Considerations
- Batch entity insertions during extraction
- Use transactions for atomic operations
- Create chunks in parallel (they're independent)
- Generate embeddings in batches

## Future Enhancements

1. **Smart Chunking**: Use section headers and concept boundaries
2. **Hierarchical Chunks**: Nested chunks for different granularities
3. **Cross-Document Chunks**: Identify similar sections across papers
4. **Dynamic Chunk Size**: Adjust based on content density

## Summary

The key insight: **Extraction needs context, retrieval needs focus**. By separating these concerns, we get the best of both worlds - comprehensive knowledge graphs from full documents and efficient semantic search from focused chunks.

Remember: The chunks are just windows into the document. The real knowledge lives in the relationships between entities, extracted with full context.