# Interactive CV System

An AI-powered system that transforms academic research papers and personal notes into a dynamic, queryable professional profile. Using advanced NLP and knowledge graphs, it enables intelligent conversations about research expertise and professional journey.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd interactive_cv

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Add your API keys:
# OPENROUTER_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here

# 4. Extract and populate metadata (modular workflow)
# Extract personal notes metadata to JSON
python scripts/extract_personal_notes_metadata.py

# Populate database from JSON metadata
python DB/unified_metadata_populator.py

# Update knowledge graph
python populate_graph_tables.py

# 5. Run the interactive agent
python interactive_agent.py
```

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Data Sources   │     │ Processing Layer │     │   Query Layer   │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ Academic Papers │────▶│ LLM Analysis     │────▶│ SQL + Graph     │
│ Personal Notes  │     │ Entity Extraction│     │ Semantic Search │
└─────────────────┘     │ Embeddings       │     │ LangChain Agent │
                        │ Chunking         │     └─────────────────┘
                        └──────────────────┘     

Processing Pipeline:
┌──────────────┐    ┌─────────────┐    ┌──────────────┐    ┌──────────┐
│ Raw Document │───▶│ LLM Analyzer│───▶│ LLM Extractor│───▶│ Database │
└──────────────┘    └─────────────┘    └──────────────┘    └──────────┘
                           │                    │                  │
                    (Full Analysis)    (Entity Extraction)   (Normalized)

Modular Workflow (NEW):
┌──────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────┐
│ Raw Document │───▶│ LLM Extractor│───▶│ JSON Files  │───▶│ Database │
└──────────────┘    └──────────────┘    └─────────────┘    └──────────┘
                           │                    │                  │
                    (Extract Metadata)   (Inspectable)      (Unified Import)
```

## 📁 Project Structure

```
interactive_cv/
├── academic/              # Research papers and analyses
├── personal_notes/        # Daily and weekly notes
├── agents/                # LLM-based analyzers and extractors
├── DB/                    # Database and processing system
│   ├── extractors/        # Base extraction logic
│   ├── process_paper_pipeline.py  # End-to-end pipeline
│   ├── embeddings.py      # Vector embedding generation
│   └── query_comprehensive.py # Database exploration
├── KG/                    # Knowledge Graph system
│   ├── knowledge_graph.py # Graph generation
│   └── graph_enhanced_query.py # Intelligent queries
├── scripts/               # Utility scripts
├── .sync/                 # Chronicle sync system
├── interactive_agent.py   # Conversational AI interface
└── web_ui/               # Visualization interface
```

## 🔍 Key Features

### 1. Multi-Stage Academic Processing Pipeline

The system uses a sophisticated "Extract First, Chunk Later" approach:

```
Raw Paper → Full Analysis → Entity Extraction → Database → Chunking → Embeddings
```

**Why This Order Matters**:
- **Full Context Extraction**: Catches cross-document references, relationships, and concept hierarchies
- **Smart Chunking**: Splits at semantic boundaries (1000-1500 tokens) AFTER extraction
- **Entity Mapping**: Each chunk knows which entities it contains (no re-extraction needed)
- **Efficient RAG**: Small chunks with rich metadata pointers

**Pipeline Stages**:
1. **Analysis**: LLM analyzes complete paper following structured methodology
2. **Extraction**: Different LLM extracts entities from FULL analysis (not raw paper)
3. **Storage**: Atomic database transactions preserve relationships
4. **Chunking**: Semantic splitting with section awareness
5. **Embeddings**: Generated for documents, chunks, AND entities

### 2. Knowledge Graph
- Database-agnostic design
- 790 nodes and 546 edges from academic papers and personal notes
- Entity types: documents, topics, people, projects, methods, institutions
- Pre-computed graph tables for performance
- PageRank identifies key research areas and connections

### 3. Semantic Search & RAG

**RAG Query Flow Example** - "What did Vaios work on with optimal transport?":
1. **Entity Recognition**: Identify "Vaios" (person) and "optimal transport" (topic)
2. **Relationship Query**: Find documents linking these entities via SQL
3. **Chunk Retrieval**: Get chunks from those documents mentioning both
4. **Semantic Search**: Use embeddings to rank chunk relevance
5. **Context Assembly**: Include document metadata + chunk content
6. **Response Generation**: LLM uses rich context to answer

**Key Components**:
- OpenAI embeddings for all content (447 total)
- 186 document chunks for granular retrieval
- Chunk-entity mappings with relevance scores
- Combined SQL + vector search for best results

### 4. Modular Metadata Workflow

The system now supports a modular approach that separates extraction from storage:

**Benefits**:
- **Separation of Concerns**: Extraction logic is independent of storage
- **Inspectable Metadata**: JSON files can be reviewed before database import
- **Flexibility**: Re-run database population without re-extracting
- **Consistency**: Academic and personal notes follow the same pattern
- **Debugging**: Easy to see what was extracted and modify if needed

**Components**:
- `agents/academic_metadata_extractor.py` - Extracts academic metadata to JSON
- `agents/chronicle_metadata_extractor.py` - Extracts personal notes metadata to JSON  
- `DB/unified_metadata_populator.py` - Populates database from JSON files

**Workflow**:
1. Extract metadata from documents → JSON files
2. Review/modify JSON if needed
3. Import JSON to database
4. Update knowledge graph

### 5. Interactive Agent
- Natural language interface
- Multiple specialized tools
- Conversation memory
- Real-time streaming responses

## 📊 Current Status (2025-01-03)

### Database Statistics
- **12 academic papers**: All successfully processed
- **7 personal notes**: Extracted and ready
- **192 topics**: Mathematical concepts and research areas
- **18 people**: Authors and researchers
- **57 methods**: Analytical and computational techniques
- **25 institutions**: Universities and organizations
- **186 document chunks**: For semantic search
- **447 embeddings**: For RAG capabilities
- **315 relationships**: Between entities

### Processing Pipeline Status
✅ Academic paper analysis and extraction
✅ Direct database population
✅ Semantic chunking with entity mapping
✅ Embedding generation
✅ Chronicle sync system
⏳ Knowledge graph visualization (tables need population)
⏳ Interactive web UI

## 🗄️ Complete Database Schema

### Core Document Tables

```sql
-- Chronicle documents (daily/weekly/monthly notes)
CREATE TABLE IF NOT EXISTS chronicle_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    date DATE,
    note_type TEXT DEFAULT 'daily',
    content TEXT,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic documents (papers, analyses)
CREATE TABLE IF NOT EXISTS academic_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    date DATE,
    document_type TEXT DEFAULT 'paper',
    domain TEXT,
    content TEXT,
    content_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Backward compatibility view
CREATE VIEW IF NOT EXISTS documents AS
SELECT 
    'chronicle_' || id as unified_id,
    'chronicle' as doc_type,
    id,
    file_path,
    title,
    date,
    note_type,
    NULL as document_type,
    NULL as domain,
    content,
    content_hash,
    created_at,
    modified_at
FROM chronicle_documents
UNION ALL
SELECT 
    'academic_' || id as unified_id,
    'academic' as doc_type,
    id,
    file_path,
    title,
    date,
    NULL as note_type,
    document_type,
    domain,
    content,
    content_hash,
    created_at,
    modified_at
FROM academic_documents;
```

### Entity Tables

```sql
-- Topics (including mathematical concepts, research areas)
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- People (authors, collaborators, mentioned individuals)
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    role TEXT,
    affiliation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Institutions
CREATE TABLE IF NOT EXISTS institutions (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Methods (including algorithms)
CREATE TABLE IF NOT EXISTS methods (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Applications
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    domain TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Relationship Tables

```sql
-- Unified relationships table (no redundancy!)
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_type, source_id, target_type, target_id, relationship_type)
);

-- Index for efficient querying
CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type);
```

### Embeddings and Graph Tables

```sql
-- Embeddings for all entities
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    embedding BLOB NOT NULL,
    model_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_type, entity_id, model_name)
);

-- Pre-computed graph nodes for visualization
CREATE TABLE IF NOT EXISTS graph_nodes (
    id INTEGER PRIMARY KEY,
    node_id TEXT UNIQUE NOT NULL,
    node_type TEXT NOT NULL,
    node_label TEXT NOT NULL,
    attributes JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pre-computed graph edges for visualization
CREATE TABLE IF NOT EXISTS graph_edges (
    id INTEGER PRIMARY KEY,
    source_node_id TEXT NOT NULL,
    target_node_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    attributes JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_node_id, target_node_id, edge_type),
    FOREIGN KEY (source_node_id) REFERENCES graph_nodes(node_id),
    FOREIGN KEY (target_node_id) REFERENCES graph_nodes(node_id)
);
```

### Chunking Tables

```sql
-- Document chunks for RAG
CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY,
    document_type TEXT NOT NULL,
    document_id INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    section_name TEXT,
    chunk_metadata JSON,
    start_char INTEGER,
    end_char INTEGER,
    token_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_type, document_id, chunk_index)
);

-- Entity mapping to chunks
CREATE TABLE IF NOT EXISTS chunk_entities (
    chunk_id INTEGER REFERENCES document_chunks(id),
    entity_type TEXT NOT NULL,
    entity_id INTEGER NOT NULL,
    relevance_score FLOAT DEFAULT 1.0,
    PRIMARY KEY (chunk_id, entity_type, entity_id)
);
```

### Key Design Principles

1. **No Redundancy**: Single `relationships` table for ALL relationships
2. **Unified IDs**: Documents use format `{type}_{id}` (e.g., 'chronicle_1', 'academic_2')
3. **Direct Extraction**: Entities created during extraction, no intermediate JSON
4. **Graph-Ready**: Pre-computed tables for fast visualization
5. **Flexible Metadata**: JSON fields for extensibility
6. **Entity Normalization**: Shared entities across documents (topics, people, etc.)

### Common Relationship Types

- `discusses`: Document discusses a topic
- `authored_by`: Document authored by person
- `uses_method`: Document uses a method/algorithm
- `has_application`: Document has an application
- `part_of`: Document part of project
- `affiliated_with`: Person affiliated with institution
- `builds_on`: Document/topic builds on another
- `enables`: Document/topic enables another

## 🛠️ Usage Examples

### Process Academic Papers

```bash
# Test with single paper
python scripts/test_pipeline.py

# Process all papers
python scripts/process_all_papers.py
```

### Chronicle Sync

```bash
# Regular sync with metadata extraction
chronicle

# Dry run to see what would change
chronicle-dry

# Force re-extraction of all metadata
chronicle-force
```

### Database Exploration

```bash
# Launch web-based database viewer
./view_database.sh

# Query the database directly
python DB/query_comprehensive.py
```

### Knowledge Graph

```bash
# Generate/update the knowledge graph
python KG/knowledge_graph.py DB/metadata.db

# View in web UI
open web_ui/index.html
```

### Interactive Agent

```python
# Example queries:
"What papers has Vaios written about optimal transport?"
"How does his work on gradient flows connect to machine learning?"
"What are the key mathematical methods used across all papers?"
"Show me papers that mention neural networks"
```

## 🔧 Configuration

### Environment Variables
```bash
OPENROUTER_API_KEY=     # For LLM analysis and extraction
OPENAI_API_KEY=         # For embeddings
```

### Obsidian Setup
Edit `.sync/sync_chronicle_with_metadata.py`:
```python
"source": "/path/to/Obsidian/Chronicles/",
"local_dest": "chronicle/",
```

## 🚦 Development Workflow

1. **Add academic papers**: Place in `academic/` → Run `python scripts/process_all_papers.py`
2. **Add chronicle notes**: Write in Obsidian → Run `chronicle` → Automatic extraction
3. **Update knowledge graph**: Run `python KG/knowledge_graph.py DB/metadata.db`
4. **Query the system**: Use `interactive_agent.py` or direct SQL queries

## 📈 Future Enhancements

- [ ] Populate pre-computed graph tables for visualization
- [ ] Extract institutions from papers
- [ ] Web API (REST/GraphQL) for remote queries
- [ ] Interactive web UI completion
- [ ] Real-time RAG pipeline integration
- [ ] Export to various CV formats (PDF, JSON, etc.)
- [ ] Multi-language support
- [ ] Citation network analysis
- [ ] Automated paper discovery and import

## 🤝 Contributing

This is currently a personal project, but ideas and feedback are welcome!

## 📝 License

[Your chosen license]

---

Built with ❤️ to transform static CVs into living, intelligent representations of research journeys.