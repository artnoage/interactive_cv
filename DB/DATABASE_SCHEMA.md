# Interactive CV Database Schema V2

## Overview

This document outlines the redesigned database schema for the Interactive CV system. The new design eliminates redundancy, normalizes data storage, and provides a clean structure that supports both RAG (Retrieval Augmented Generation) agents and knowledge graph construction without requiring additional processing scripts.

## Design Principles

1. **Single Source of Truth**: Each piece of information stored once
2. **Normalized Structure**: Proper entity tables with attributes
3. **Flexible Relationships**: Generic relationship model supporting any connection type
4. **Graph-Ready**: Pre-computed graph structures for fast queries
5. **RAG-Optimized**: Embeddings and metadata readily accessible

## Schema Design

### Document Tables

```sql
-- Chronicle documents (daily/weekly/monthly notes)
CREATE TABLE chronicle_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT,
    date DATE NOT NULL,
    note_type TEXT CHECK(note_type IN ('daily', 'weekly', 'monthly')),
    content TEXT,
    content_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic documents (papers and analyses)
CREATE TABLE academic_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    date DATE,
    document_type TEXT CHECK(document_type IN ('paper', 'analysis')),
    domain TEXT CHECK(domain IN ('mathematics', 'computer_science', 'physics')),
    content TEXT,
    content_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Unified view for common queries
CREATE VIEW documents AS
SELECT 
    'chronicle_' || id as unified_id,
    'chronicle' as doc_type,
    id as original_id,
    file_path,
    title,
    date,
    content,
    content_hash,
    created_at,
    modified_at
FROM chronicle_documents
UNION ALL
SELECT 
    'academic_' || id as unified_id,
    'academic' as doc_type,
    id as original_id,
    file_path,
    title,
    date,
    content,
    content_hash,
    created_at,
    modified_at
FROM academic_documents;
```

### Entity Tables

```sql
-- Topics/Concepts (mathematical concepts, research areas, technologies)
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT, -- 'mathematical', 'technology', 'research_area', etc.
    description TEXT,
    parent_topic_id INTEGER REFERENCES topics(id),
    hierarchy_level INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- People (collaborators, researchers, authors)
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    email TEXT,
    affiliation TEXT,
    role TEXT, -- 'collaborator', 'advisor', 'student', etc.
    expertise TEXT, -- JSON array of expertise areas
    orcid TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects (research projects, work projects)
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('active', 'completed', 'paused', 'planned')),
    project_type TEXT, -- 'research', 'development', 'thesis', etc.
    start_date DATE,
    end_date DATE,
    outcomes TEXT, -- JSON array of outcomes/deliverables
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Institutions (universities, research centers, companies)
CREATE TABLE institutions (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT, -- 'university', 'research_center', 'company', etc.
    location TEXT,
    description TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Methods/Algorithms (specific techniques used in papers)
CREATE TABLE methods (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT, -- 'algorithm', 'technique', 'framework', etc.
    description TEXT,
    paper_reference TEXT, -- Original paper where introduced
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Applications (practical applications of research)
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    domain TEXT, -- 'healthcare', 'finance', 'robotics', etc.
    description TEXT,
    impact_level TEXT CHECK(impact_level IN ('theoretical', 'experimental', 'production')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relationship Tables

```sql
-- Generic relationships table (single source of truth for all connections)
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    source_type TEXT NOT NULL, -- 'document', 'topic', 'person', 'project', etc.
    source_id TEXT NOT NULL, -- Can be 'chronicle_123' or 'academic_456' for documents
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL, -- 'mentions', 'uses', 'collaborates_with', etc.
    confidence FLOAT DEFAULT 1.0, -- Extraction confidence
    context TEXT, -- Optional context about the relationship
    metadata JSON, -- Additional relationship-specific data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_type, source_id, target_type, target_id, relationship_type)
);

-- Indexes for efficient querying
CREATE INDEX idx_rel_source ON relationships(source_type, source_id);
CREATE INDEX idx_rel_target ON relationships(target_type, target_id);
CREATE INDEX idx_rel_type ON relationships(relationship_type);
```

### Embeddings and Chunks

```sql
-- Document chunks for RAG
CREATE TABLE document_chunks (
    id INTEGER PRIMARY KEY,
    document_type TEXT NOT NULL, -- 'chronicle' or 'academic'
    document_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    start_char INTEGER,
    end_char INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_type, document_id, chunk_index)
);

-- Embeddings for documents, chunks, and entities
CREATE TABLE embeddings (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL, -- 'document', 'chunk', 'topic', 'person', etc.
    entity_id TEXT NOT NULL, -- Flexible ID format
    embedding BLOB NOT NULL,
    model_name TEXT NOT NULL DEFAULT 'text-embedding-3-small',
    model_version TEXT,
    dimensions INTEGER DEFAULT 1536,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_type, entity_id, model_name)
);

-- Index for fast similarity search
CREATE INDEX idx_embeddings_lookup ON embeddings(entity_type, entity_id);
```

### Pre-computed Graph Tables

```sql
-- Graph nodes with computed properties
CREATE TABLE graph_nodes (
    node_id TEXT PRIMARY KEY, -- Format: "type_id" (e.g., "topic_123", "doc_chronicle_45")
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    label TEXT NOT NULL,
    attributes JSON, -- Node-specific attributes
    degree INTEGER DEFAULT 0, -- Number of connections
    pagerank_score FLOAT,
    betweenness_centrality FLOAT,
    community_id INTEGER, -- For community detection
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_type, entity_id)
);

-- Graph edges with weights
CREATE TABLE graph_edges (
    edge_id INTEGER PRIMARY KEY,
    source_node_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
    target_node_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
    relationship_type TEXT NOT NULL,
    weight FLOAT DEFAULT 1.0,
    attributes JSON, -- Edge-specific attributes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_node_id, target_node_id, relationship_type)
);

-- Indexes for graph traversal
CREATE INDEX idx_edges_source ON graph_edges(source_node_id);
CREATE INDEX idx_edges_target ON graph_edges(target_node_id);
CREATE INDEX idx_nodes_type ON graph_nodes(entity_type);
CREATE INDEX idx_nodes_pagerank ON graph_nodes(pagerank_score DESC);
```

### Extraction Tracking

```sql
-- Track extraction history and versions
CREATE TABLE extraction_log (
    id INTEGER PRIMARY KEY,
    source_file TEXT NOT NULL,
    extraction_type TEXT NOT NULL, -- 'chronicle', 'academic', 'relationships'
    extractor_version TEXT,
    entities_extracted INTEGER,
    relationships_extracted INTEGER,
    status TEXT CHECK(status IN ('success', 'partial', 'failed')),
    error_message TEXT,
    duration_seconds FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationship Types

### Document-to-Entity Relationships
- `mentions` - Document mentions a topic/concept
- `discusses` - Document discusses in detail
- `introduces` - Document introduces new concept
- `authored_by` - Document authored by person
- `references` - Document references another document
- `part_of` - Document is part of project
- `affiliated_with` - Document affiliated with institution

### Entity-to-Entity Relationships
- `related_to` - General relationship between topics
- `parent_of` / `child_of` - Hierarchical topic relationships
- `collaborates_with` - Person collaborates with person
- `works_on` - Person works on project
- `employs` - Institution employs person
- `hosts` - Institution hosts project
- `uses_method` - Project/Document uses method
- `enables_application` - Method/Topic enables application

## Usage Examples

### 1. Find all topics mentioned in a document
```sql
SELECT t.* 
FROM topics t
JOIN relationships r ON r.target_type = 'topic' AND r.target_id = t.id
WHERE r.source_type = 'document' 
  AND r.source_id = 'chronicle_123'
  AND r.relationship_type = 'mentions';
```

### 2. Get document with embeddings for RAG
```sql
SELECT d.*, e.embedding
FROM documents d
LEFT JOIN embeddings e ON e.entity_type = 'document' 
  AND e.entity_id = d.unified_id
WHERE d.unified_id = 'academic_456';
```

### 3. Build knowledge graph
```sql
-- Get all nodes
SELECT * FROM graph_nodes ORDER BY pagerank_score DESC;

-- Get all edges
SELECT * FROM graph_edges;
```

### 4. Find related documents through shared topics
```sql
WITH doc_topics AS (
    SELECT r.target_id as topic_id
    FROM relationships r
    WHERE r.source_type = 'document' 
      AND r.source_id = 'chronicle_100'
      AND r.target_type = 'topic'
)
SELECT DISTINCT d.*
FROM documents d
JOIN relationships r ON r.source_type = 'document' 
  AND r.source_id = d.unified_id
WHERE r.target_type = 'topic' 
  AND r.target_id IN (SELECT topic_id FROM doc_topics)
  AND d.unified_id != 'chronicle_100';
```

## Migration Benefits

1. **Eliminates Redundancy**: No more duplicate relationship storage
2. **Faster Queries**: Pre-computed graph structures and proper indexes
3. **Flexible Schema**: Easy to add new entity types or relationship types
4. **RAG-Ready**: Embeddings and chunks properly linked
5. **Graph-Native**: Can build KG directly from tables without processing
6. **Audit Trail**: Extraction log tracks all changes
7. **Extensible**: JSON fields allow schema evolution without migrations

## Implementation Notes

1. Use transactions for all multi-table operations
2. Implement triggers to update graph tables when relationships change
3. Use batch inserts for better performance during extraction
4. Regular VACUUM and ANALYZE for optimal query performance
5. Consider partitioning large tables by date if needed