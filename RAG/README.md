# 🧠 RAG (Retrieval-Augmented Generation) System

## Overview

The RAG system provides semantic search capabilities for the Interactive CV project using OpenAI embeddings to find semantically similar content across documents, chunks, and entities.

## System Architecture

```
Documents → Semantic Chunking → Embeddings → Search & Retrieval
```

The RAG system integrates with:
- **Database System**: SQLite database with document chunks and embeddings
- **Interactive Agent**: Provides semantic search tools for intelligent responses
- **Knowledge Graph**: Works alongside graph traversal for comprehensive queries

## Core Components

### 1. **semantic_search.py** - Advanced Semantic Retrieval

**Purpose**: Provides state-of-the-art semantic search capabilities using OpenAI embeddings to find semantically similar content across documents, chunks, and entities.

#### Key Features
- **Multi-Level Search**: Document, chunk, and entity-level semantic search
- **Hybrid Search**: Combines multiple search modes for comprehensive results
- **Rich Metadata**: Includes document titles, dates, types, and categories
- **Similarity Scoring**: Cosine similarity with configurable thresholds
- **Content Excerpting**: Intelligent excerpt extraction with query highlighting
- **Batch Processing**: Efficient handling of large result sets

#### Core Functions

**Semantic Chunk Search**:
```python
# Search document chunks with semantic similarity
results = semantic_search_chunks(
    db_path="DB/metadata.db",
    query="neural networks for optimal transport",
    limit=10,
    doc_type="academic",  # Filter by document type
    similarity_threshold=0.6,
    include_metadata=True
)
```

**Entity Similarity Search**:
```python
# Find semantically similar entities
entities = find_similar_entities(
    db_path="DB/metadata.db",
    query="gradient flows",
    entity_type="topic",  # Filter by entity type
    limit=15,
    similarity_threshold=0.7
)
```

**Document-Level Search**:
```python
# Search full documents for broader context
documents = semantic_search_documents(
    db_path="DB/metadata.db",
    query="reinforcement learning applications",
    limit=5,
    similarity_threshold=0.5
)
```

**Hybrid Search**:
```python
# Combine chunk and entity search
hybrid_results = hybrid_search(
    db_path="DB/metadata.db",
    query="mathematical foundations of AI",
    limit=10,
    chunk_weight=0.6,    # Weight for content results
    entity_weight=0.4,   # Weight for concept results
    similarity_threshold=0.5
)
```

#### Advanced Features
- **Smart Entity Resolution**: Automatically fetches detailed entity information based on type
- **Content Excerpting**: Extracts relevant passages around query terms
- **Weighted Scoring**: Configurable weights for different result types
- **Comprehensive Logging**: Detailed search analytics and performance metrics
- **Graceful Fallback**: Handles missing embeddings and API failures

## Integration Points

### 1. Interactive Agent Integration
The semantic search system powers the interactive agent with:
- **Semantic search tool**: Embedding-powered search across all entity types
- **Entity-aware intelligence**: Understanding of document types and categories
- **Cross-domain discovery**: Finding connections between different research areas
- **Contextual search**: Rich metadata and relationship information

### 2. Database Integration
**Source Tables**:
- `documents`: Academic papers and personal notes
- `document_chunks`: Semantic document segments
- `embeddings`: Vector representations (text-embedding-3-large, 3072 dimensions)
- `topics`, `people`, `methods`, `institutions`, `applications`: Entity tables
- `relationships`: Entity connections

### 3. Knowledge Graph Integration
- Works alongside graph traversal for comprehensive exploration
- Provides semantic similarity while graph provides structural relationships
- Combines embedding-based and graph-based search strategies

### 4. Web UI Integration
The unified web interface (`serve_ui.py`) uses RAG capabilities for:
- Real-time chat responses with semantic search
- Query-based content discovery
- Interactive exploration of related concepts

## Usage Examples

### Basic Semantic Search
```python
from RAG.semantic_search import semantic_search_chunks

# Traditional semantic search
results = semantic_search_chunks(
    "DB/metadata.db",
    "What is optimal transport theory?",
    limit=5,
    similarity_threshold=0.6
)

for result in results:
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Content: {result['content'][:200]}...")
    print(f"Source: {result['document_title']}")
    print("---")
```

### Comprehensive Query Search
```python
from RAG.semantic_search import hybrid_search

# Perform comprehensive search
results = hybrid_search(
    "DB/metadata.db",
    "mathematical foundations of generative adversarial networks",
    limit=8,
    chunk_weight=0.7,
    entity_weight=0.3
)

print(f"Found {results['total_results']} total results:")
print(f"- {len(results['chunks'])} content chunks")
print(f"- {len(results['entities'])} related entities")

# Display top chunks
for chunk in results['chunks'][:3]:
    print(f"Chunk (similarity: {chunk['similarity']:.3f}): {chunk['content'][:100]}...")

# Display top entities
for entity in results['entities'][:3]:
    print(f"Entity (similarity: {entity['similarity']:.3f}): {entity['name']} ({entity['entity_type']})")
```

### Entity-Focused Search
```python
from RAG.semantic_search import find_similar_entities

# Search for similar entities
entities = find_similar_entities(
    "DB/metadata.db",
    "machine learning optimization",
    entity_type="topic",
    limit=10,
    similarity_threshold=0.6
)

for entity in entities:
    print(f"- {entity['name']} (similarity: {entity['similarity']:.3f})")
    if entity.get('description'):
        print(f"  Description: {entity['description'][:100]}...")
```

## Configuration

### Environment Setup
```bash
# Required environment variables in .env
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Configuration
- **Embedding Model**: `text-embedding-3-large` (3072 dimensions)
- **Similarity Metric**: Cosine similarity
- **Default Thresholds**: 0.5-0.7 depending on search type

### Performance Tuning
```python
# Adjust search parameters for performance vs. quality
semantic_search_chunks(
    query="your query",
    limit=20,                    # More results
    similarity_threshold=0.4,    # Lower threshold = more results
    include_metadata=False       # Faster without metadata
)
```

## Performance Characteristics

### Search Performance
- **Chunk Search**: ~100-500ms for 5-10 results (depending on database size)
- **Entity Search**: ~200-800ms for 10-15 results (depends on entity count)
- **Document Search**: ~50-200ms for 5-10 documents
- **Hybrid Search**: ~300-1000ms for comprehensive results

### Scaling Considerations
- **Database Size**: Optimized for 100-1000 documents with 1000-5000 entities
- **Memory Usage**: ~50-200MB for typical knowledge bases
- **API Costs**: ~$0.001-0.01 per query (depending on content volume)
- **Concurrent Users**: Supports 5-10 concurrent searches efficiently

## Error Handling & Reliability

### Graceful Degradation
- **OpenAI API Unavailable**: Provides empty results with clear warnings
- **Database Connection Issues**: Comprehensive error logging and recovery
- **Invalid Embeddings**: Skips corrupted embeddings automatically
- **Missing Tables**: Handles database schema variations gracefully

### Monitoring & Logging
```python
import logging

# Enable detailed RAG logging
logging.getLogger('RAG').setLevel(logging.DEBUG)

# Monitor search performance
logger.info(f"Search completed in {elapsed_time:.2f}s with {result_count} results")
```

## Future Enhancements

### Planned Features
1. **Caching Layer**: Redis-based result caching for improved performance
2. **Advanced Reranking**: Learning-to-rank models for result ordering
3. **Query Understanding**: NLP-based query parsing and intent detection
4. **Personalization**: User-specific search preferences and history
5. **Multi-Modal Search**: Support for images, tables, and structured data

### Technical Improvements
1. **Embedding Updates**: Support for newer OpenAI models and local embeddings
2. **Search Analytics**: Comprehensive search quality metrics and A/B testing
3. **Real-Time Updates**: Live index updates as new documents are added
4. **Graph Integration**: Better integration with knowledge graph traversal

## Dependencies

### Core Dependencies
```python
# Vector operations and similarity
import numpy as np

# Database connectivity
import sqlite3

# OpenAI embeddings
from openai import OpenAI

# Logging and utilities
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
```

### External Services
- **OpenAI API**: For embedding generation
- **SQLite Database**: For persistent data storage

## Troubleshooting

### Common Issues

1. **"OpenAI API not available"**
   - **Cause**: Missing or invalid OPENAI_API_KEY
   - **Solution**: Check .env file and API key validity

2. **"No embeddings found"**
   - **Cause**: Embeddings not generated for content
   - **Solution**: Run `python DB/utils/embeddings.py` to generate embeddings

3. **"Low similarity scores"**
   - **Cause**: Query mismatch or poor embedding quality
   - **Solution**: Lower similarity threshold or rephrase query

4. **"Database connection error"**
   - **Cause**: Missing or corrupted database file
   - **Solution**: Run `python DB/build_database.py` to rebuild database

### Debug Commands
```bash
# Test semantic search
python -c "from RAG.semantic_search import semantic_search_chunks; print(semantic_search_chunks('DB/metadata.db', 'test query', limit=3))"

# Check embedding availability
sqlite3 DB/metadata.db "SELECT COUNT(*) FROM embeddings WHERE entity_type='chunk';"

# Verify database structure
python DB/utils/query_comprehensive.py
```

## 📚 Related Documentation

- **[Main Project README](../README.md)**: Overall system architecture and quick start
- **[Database System](../DB/README.md)**: How data is processed and stored for search
- **[Knowledge Graph](../KG/README.md)**: How semantic search complements graph navigation
- **[Interactive Agent](../interactive_agent.py)**: How RAG powers intelligent responses

---

## System Impact

The RAG system transforms static document storage into an intelligent, searchable knowledge base that:

- **Understands Context**: Semantic similarity beyond keyword matching
- **Handles Synonyms**: Finds related concepts automatically
- **Scales Efficiently**: Optimized for large document collections
- **Integrates Seamlessly**: Works with graph navigation and agent systems
- **Provides Transparency**: Clear similarity scores and source attribution

*The RAG system makes your professional knowledge truly searchable and discoverable.*