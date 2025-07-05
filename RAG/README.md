# RAG (Retrieval-Augmented Generation) System

## Overview

The RAG system for the Interactive CV provides advanced retrieval capabilities that combine semantic search, knowledge graph traversal, and intelligent query enhancement to power conversational AI agents with rich, contextual information from the research database.

## System Architecture

### Core Philosophy
```
Traditional Search → Semantic Understanding → Graph-Enhanced Intelligence → Rich Context Generation
```

The RAG system bridges the gap between simple keyword search and intelligent information retrieval by leveraging:
- **Semantic Embeddings**: OpenAI text-embedding-3-large for deep semantic understanding
- **Knowledge Graph Analysis**: NetworkX-powered graph traversal for relationship discovery
- **Multi-Modal Search**: Document chunks, entities, and full documents
- **Intelligent Context**: Query-aware context generation for agent responses

## Components

### 1. **graph_enhanced_query.py** - Graph-Powered Intelligence

**Purpose**: Combines SQL database queries with knowledge graph traversal to discover hidden relationships and provide intelligent context for agent queries.

#### Key Features
- **Multi-Distance Graph Traversal**: Find related concepts across graph distances
- **Research Evolution Tracking**: Track how topics develop over time
- **Collaboration Pattern Analysis**: Discover research partnerships and networks
- **Project Connection Discovery**: Map relationships between projects, people, and topics
- **Node Importance Analysis**: PageRank-based importance scoring
- **Query Context Generation**: Intelligent context creation for agent responses

#### Core Classes & Functions

**`GraphEnhancedQuery` Class**:
```python
# Initialize with database and graph
enhancer = GraphEnhancedQuery("DB/metadata.db", "KG/knowledge_graph.json")

# Find related topics through graph traversal
related = enhancer.find_related_topics("optimal transport", max_distance=2)

# Track research evolution over time
evolution = enhancer.find_research_evolution("machine learning")

# Discover collaboration patterns
patterns = enhancer.find_collaboration_patterns()

# Analyze project connections
connections = enhancer.find_project_connections("Interactive CV")
```

**Smart Context Creation**:
```python
# Create enriched context for agent queries
context = create_agent_context(
    "What research connects optimal transport to machine learning?",
    db_path="DB/metadata.db",
    graph_path="KG/knowledge_graph.json"
)
```

#### Advanced Features
- **Flexible Node Matching**: Supports 24+ entity types including math_foundation, research_insight, personal_achievement
- **Intelligent Path Finding**: Uses NetworkX algorithms for optimal graph traversal
- **Graceful Degradation**: Works even when knowledge graph is unavailable
- **Error Recovery**: Comprehensive error handling with detailed logging
- **Query Expansion**: Suggests related queries based on graph analysis

### 2. **semantic_search.py** - Advanced Semantic Retrieval

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
The RAG system powers the interactive agent by providing:
- **Rich Query Context**: Enhanced understanding of user questions
- **Semantic Content Retrieval**: Relevant document chunks and passages
- **Relationship Discovery**: Connected concepts and research evolution
- **Expert Knowledge**: Entity-based expertise and collaboration patterns

### 2. Database Integration
**Source Tables**:
- `documents`: Academic papers and personal notes
- `document_chunks`: Semantic document segments
- `embeddings`: Vector representations (text-embedding-3-large, 3072 dimensions)
- `topics`, `people`, `methods`, `institutions`, `applications`: Entity tables
- `relationships`: Entity connections
- `graph_nodes`, `graph_edges`: Pre-computed graph structure

### 3. Knowledge Graph Integration
**Graph Sources**:
- Primary: `KG/knowledge_graph.json` (full graph)
- Fallback: `web_ui/knowledge_graph.json` (pruned for performance)
- Format: NetworkX-compatible JSON with nodes and links

### 4. Web UI Integration
The unified web interface (`serve_ui.py`) uses RAG capabilities for:
- Real-time chat responses with semantic search
- Graph node highlighting based on query relevance
- Interactive exploration of related concepts

## Usage Examples

### Basic Semantic Search
```python
from RAG.semantic_search import semantic_search_chunks

# Search for content about optimal transport
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

### Graph-Enhanced Research Discovery
```python
from RAG.graph_enhanced_query import GraphEnhancedQuery

# Initialize the enhancer
enhancer = GraphEnhancedQuery()

# Find research evolution
evolution = enhancer.find_research_evolution("reinforcement learning")
for item in evolution:
    print(f"{item['date']}: {item['title']}")
    print(f"Context: {item['excerpt'][:150]}...")

# Discover related topics
related = enhancer.find_related_topics("neural networks", max_distance=3)
for topic in related[:5]:
    print(f"- {topic['topic']} (strength: {topic['connection_strength']:.3f})")
```

### Comprehensive Query Context
```python
from RAG.graph_enhanced_query import create_agent_context

# Create rich context for agent responses
context = create_agent_context(
    "How has Vaios's research in optimal transport evolved into machine learning applications?"
)

print(f"Related topics found: {len(context['related_topics'])}")
print(f"Research evolution items: {len(context['research_evolution'])}")
print(f"Key entities: {[e[0] for e in context['key_entities'][:5]]}")
print(f"Suggested expansions: {context['suggested_expansions']}")
```

### Hybrid Search for Comprehensive Results
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
- **Graph Algorithm**: NetworkX PageRank for importance scoring

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
- **Graph Traversal**: ~50-200ms for distance-2 searches
- **Context Generation**: ~300-1000ms for comprehensive context

### Scaling Considerations
- **Database Size**: Optimized for 100-1000 documents with 1000-5000 entities
- **Memory Usage**: ~50-200MB for typical knowledge graphs
- **API Costs**: ~$0.001-0.01 per query (depending on content volume)
- **Concurrent Users**: Supports 5-10 concurrent searches efficiently

## Error Handling & Reliability

### Graceful Degradation
- **Missing Knowledge Graph**: Falls back to database-only search
- **OpenAI API Unavailable**: Provides empty results with clear warnings
- **Database Connection Issues**: Comprehensive error logging and recovery
- **Invalid Embeddings**: Skips corrupted embeddings automatically

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
2. **Graph Algorithms**: Advanced centrality measures and community detection
3. **Search Analytics**: Comprehensive search quality metrics and A/B testing
4. **Real-Time Updates**: Live index updates as new documents are added

## Dependencies

### Core Dependencies
```python
# Vector operations and similarity
import numpy as np

# Database connectivity
import sqlite3

# Graph analysis
import networkx as nx

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
- **Knowledge Graph**: JSON-based graph structure

## Troubleshooting

### Common Issues

1. **"OpenAI API not available"**
   - **Cause**: Missing or invalid OPENAI_API_KEY
   - **Solution**: Check .env file and API key validity

2. **"Knowledge graph not found"**
   - **Cause**: Missing graph files
   - **Solution**: Run `python KG/graph_builder.py` to generate graph

3. **"No embeddings found"**
   - **Cause**: Embeddings not generated for content
   - **Solution**: Run `python DB/embeddings.py` to generate embeddings

4. **"Low similarity scores"**
   - **Cause**: Query mismatch or poor embedding quality
   - **Solution**: Lower similarity threshold or rephrase query

### Debug Commands
```bash
# Test semantic search
python -c "from RAG.semantic_search import semantic_search_chunks; print(semantic_search_chunks('DB/metadata.db', 'test query', limit=3))"

# Test graph enhancement
python -c "from RAG.graph_enhanced_query import GraphEnhancedQuery; g = GraphEnhancedQuery(); print(g.is_graph_available())"

# Check embedding availability
sqlite3 DB/metadata.db "SELECT COUNT(*) FROM embeddings WHERE entity_type='chunk';"
```

## 📚 Related Documentation

- **[Main Project README](../README.md)**: Overall system architecture and quick start guide
- **[Database System](../DB/README.md)**: How data is stored and processed for RAG
- **[Knowledge Graph](../KG/README.md)**: How graph data is generated and used
- **[Interactive Agent](../agents/README.md)**: How RAG powers the conversational interface

---

## 🎯 Revolutionary Impact

The RAG system transforms the Interactive CV from a static knowledge base into a **living, intelligent research assistant** that:

- **Understands Context**: Semantic search goes beyond keywords to understand meaning
- **Discovers Connections**: Graph traversal reveals hidden relationships between concepts
- **Tracks Evolution**: Temporal analysis shows how research develops over time
- **Provides Intelligence**: Rich context generation enables sophisticated agent responses
- **Scales Gracefully**: Handles growing knowledge bases with consistent performance

**From Simple Search → Intelligent Understanding → Contextual Wisdom**

*The future of research exploration is semantic, graph-enhanced, and conversationally intelligent.*