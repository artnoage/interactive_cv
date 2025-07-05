# 🧠 RAG (Retrieval-Augmented Generation) System

## 🚀 Revolutionary Blueprint-Driven Architecture

The RAG system has been **completely transformed** using a revolutionary blueprint-driven approach that automatically generates sophisticated, domain-aware tools from YAML specifications. This system now embodies the principle: **"Blueprints over Business Logic, Configuration over Code"**.

## 🎯 Core Philosophy Evolution

### Before: Manual Tool Development
```
Manual Coding → Limited Tools → Static Capabilities → Maintenance Overhead
```

### After: Blueprint-Driven Generation
```
YAML Blueprints → Automatic Tool Generation → 79 Sophisticated Tools → Zero-Code Extension
```

The RAG system now leverages:
- **🎛️ Blueprint-Driven Tools**: 79 automatically generated tools vs 13 manual tools (6.1x improvement)
- **🔬 Entity-Aware Intelligence**: 22+ category types with rich visualization
- **🕸️ Relationship Traversal**: 20+ relationship types for graph navigation  
- **🎨 Configuration-Driven Visualization**: Complete styling from YAML specifications
- **🧬 Schema-Safe Operations**: Tools guaranteed to match database structure
- **📈 Domain-Agnostic Extensibility**: Add new research domains via YAML files only

## 🏗️ Revolutionary Architecture Components

### 1. **🎯 Blueprint-Driven Tool Generation** - The Heart of the System

**New Core Components**:
- **`blueprint_driven_loader.py`** - Parses all YAML blueprints and provides unified API
- **`blueprint_driven_tools.py`** - Automatically generates 79 sophisticated tools from specifications
- **`agent_tools_generated.py`** - Clean interface wrapper maintaining compatibility

#### 🔥 Generated Tool Categories (79 Total)

1. **Schema-Driven Tools (27 tools)**: 
   - `search_academic_documents`, `search_topics`, `search_people`, etc.
   - `get_*_by_id` tools for all entity types
   - `list_*` tools with pagination and filtering

2. **Entity-Aware Search (10 tools)**:
   - `search_academic_topics`, `search_personal_people`
   - Domain-specific with category filtering
   - Generated from `database_mapping.yaml`

3. **Relationship Traversal (40 tools)**:
   - **Forward**: `traverse_discusses`, `traverse_uses_method`, `traverse_authored_by`
   - **Reverse**: `reverse_discusses`, `reverse_authored_by`, `reverse_innovates`
   - Automatic discovery from entity mappings

4. **Category Exploration (1 tool)**:
   - `explore_topic_categories` with 22 categories
   - Visualization-ready data (colors, sizes, types)

5. **Visualization Tools (1 tool)**:
   - `get_visualization_data` with complete styling
   - Colors, sizes, groups from `visualization.yaml`

#### 🎛️ Configuration Sources
```
bluepints/
├── core/
│   ├── database_schema.yaml       # Complete database structure (15 tables)
│   └── visualization.yaml         # 28 node types, colors, layouts
├── academic/
│   └── database_mapping.yaml      # 15 entity mappings with rich categories
└── personal/
    └── database_mapping.yaml      # 12 entity mappings
```

### 2. **graph_enhanced_query.py** - Graph-Powered Intelligence (Enhanced)

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

## 🔗 Blueprint-Driven Integration Points

### 1. **Revolutionary Interactive Agent Integration**
The blueprint-generated tools power the interactive agent with:
- **🎯 79 Sophisticated Tools**: Automatically generated from YAML specifications
- **🔬 Entity-Aware Intelligence**: 22+ category types with rich domain knowledge
- **🕸️ Graph Traversal**: 20+ relationship types for deep exploration
- **🎨 Visualization-Ready Data**: Complete styling configuration from blueprints
- **📊 Schema-Safe Queries**: Tools guaranteed to match database structure
- **🧬 Domain Extension**: New research areas via YAML configuration only

#### 🏆 Transformation Results
| Aspect | Manual Tools | Blueprint-Generated |
|--------|-------------|--------------------|
| **Tool Count** | 13 methods | **79 tools** (6.1x more) |
| **Relationship Types** | 1 basic tool | **20 relationship types** |
| **Category Awareness** | Basic filtering | **22 rich categories** |
| **Schema Safety** | Prone to errors | **Guaranteed consistency** |
| **Domain Extension** | Code changes | **YAML file additions** |

### 2. **Configuration-Driven Tool Usage**
```python
# Initialize blueprint-generated tools
from RAG.agent_tools_generated import GeneratedInteractiveCVTools
tools = GeneratedInteractiveCVTools()

# Schema-driven search (auto-generated)
papers = tools.search_academic_papers("neural networks", limit=5)

# Relationship traversal (auto-generated)
relations = tools.traverse_relationship("discusses", "document", "academic_1")

# Category exploration (auto-generated)  
categories = tools.explore_topic_categories()

# Visualization data (auto-generated)
viz_data = tools.get_visualization_data("topic", "1")
```

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

## 🔥 Blueprint-Driven Usage Examples

### Revolutionary Tool Generation in Action
```python
from RAG.blueprint_driven_tools import BlueprintDrivenToolGenerator

# Initialize the generator (reads ALL YAML blueprints)
generator = BlueprintDrivenToolGenerator()

# Automatically generated 79 tools from blueprints!
print(f"Generated {len(generator.list_all_tools())} tools from YAML specifications")

# Execute any generated tool
results = generator.execute_tool("search_topics", query="neural", limit=5)
relations = generator.execute_tool("traverse_discusses", 
                                 source_type="document", 
                                 source_id="academic_1")
categories = generator.execute_tool("explore_topic_categories", limit=10)
```

### Schema-Driven Database Queries (Auto-Generated)
```python
from RAG.agent_tools_generated import GeneratedInteractiveCVTools

tools = GeneratedInteractiveCVTools()

# All these tools are automatically generated from blueprints!
papers = tools.search_academic_papers("optimal transport", limit=3)
topics = tools.find_research_topics("neural networks", category="innovation")
people = tools.get_collaborations("Vaios Laschos")
evolution = tools.get_research_evolution("machine learning")

# Rich category exploration with visualization data
categories = tools.explore_topic_categories()
print(f"Found {categories['total_categories']} categories with colors and styling")
```

### Legacy Semantic Search (Still Available)
```python
from RAG.semantic_search import semantic_search_chunks

# Traditional semantic search (fallback for complex similarity)
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

## 📚 Blueprint-Driven Documentation

- **[Main Project README](../README.md)**: Revolutionary blueprint-driven architecture overview
- **[Database System](../DB/README.md)**: Configuration-driven data processing
- **[Knowledge Graph](../KG/README.md)**: How blueprint-generated graph supports 24+ node types
- **[CLAUDE.md](../CLAUDE.md)**: Complete blueprint transformation documentation
- **[Blueprint Transformation Summary](../docs/BLUEPRINT_TRANSFORMATION_SUMMARY.md)**: Detailed comparison and technical achievements

---

## 🚀 Revolutionary Blueprint-Driven Impact

### 🎯 From Manual Tools to Automatic Generation

The RAG system has undergone a **revolutionary transformation** that embodies the future of research software development:

#### ✨ **Before: Manual Development Era**
- 13 manually coded tools
- Hardcoded database queries  
- Limited relationship types
- Code changes for new domains
- Maintenance overhead

#### 🔥 **After: Blueprint-Driven Revolution**
- **79 automatically generated tools** (6.1x improvement)
- **Schema-safe queries** guaranteed to match database
- **20+ relationship types** for comprehensive graph traversal
- **22+ entity categories** with rich visualization
- **Zero-code domain extension** via YAML files
- **Configuration-driven maintenance**

### 🌟 **The Future is Configuration-Driven**

**Vision Realized**: *"AI-driven/standard installation that creates tools out of blueprints"*

#### 🎛️ **Universal Principles**
- **Blueprints over Business Logic**: Domain knowledge in YAML, not Python
- **Configuration over Code**: Declarative specifications drive behavior
- **Generation over Manual**: Sophisticated tools created automatically
- **Consistency over Creativity**: Schema guarantees prevent errors
- **Extension over Modification**: New domains via configuration only

#### 🔮 **Transformative Capabilities**
- **Domain-Agnostic Architecture**: Works for any research field without code changes
- **LLM-Assistable Configuration**: AI can help generate domain blueprints
- **Shareable Standards**: Research communities can share domain configurations
- **Reproducible Science**: Exact blueprint configurations ensure consistent results
- **Collaborative Development**: Non-programmers can modify extraction rules

### 🏆 **Beyond Traditional RAG**

**From Simple Retrieval → Blueprint-Driven Intelligence → Universal Knowledge Platform**

The Interactive CV RAG system now represents:
- **🧬 Self-Configuring Intelligence**: Tools that generate themselves from specifications
- **🌐 Universal Adaptability**: Works across any research domain or knowledge area
- **🎯 Perfect Consistency**: Schema-driven operations prevent database mismatches
- **⚡ Rapid Extension**: New capabilities in minutes, not weeks
- **🔬 Research-Grade Reliability**: Configuration validation ensures correctness

**This is the future of intelligent knowledge systems: Blueprint-driven, universally adaptable, and automatically sophisticated.** 🌟

*The future of RAG is blueprint-driven, democratically accessible, and universally adaptable - and it starts here.* 🌟