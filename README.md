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

# 4. Sync chronicle notes (if you have Obsidian set up)
./.sync/sync-chronicle

# 5. Run the interactive agent
python interactive_agent.py
```

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Data Sources   │     │ Metadata System  │     │   Query Layer   │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ Academic Papers │────▶│ LLM Extraction   │────▶│ SQL + Graph     │
│ Chronicle Notes │     │ Embeddings       │     │ Semantic Search │
└─────────────────┘     │ Knowledge Graph  │     │ LangChain Agent │
                        └──────────────────┘     └─────────────────┘

Knowledge Graph Architecture (Database-Agnostic):
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Data Source   │────▶│  Data Provider   │────▶│ Knowledge Graph │
│  (SQL, API,     │     │  (Adapter)       │     │  (Pure Logic)   │
│   JSON, etc.)   │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 📁 Project Structure

```
interactive_cv/
├── academic/              # Research papers and analyses
├── chronicle/             # Daily notes (synced from Obsidian)
├── metadata_system/       # Core extraction and query system
│   ├── extractors/        # Metadata extraction logic
│   ├── embeddings.py      # Vector embedding generation
│   ├── knowledge_graph.py # Graph generation
│   └── graph_enhanced_query.py # Intelligent queries
├── .sync/                 # Sync scripts
├── interactive_agent.py   # Conversational AI interface
└── Gemini_knowledge_graph/ # Semantic relationship mappings
```

## 🔍 Key Features

### 1. Automated Metadata Extraction
- Uses LLMs to extract topics, people, projects from documents
- Maintains relationships in SQLite database
- Tracks document changes with content hashing

### 2. Knowledge Graph
- Database-agnostic design: can work with any data source
- 257 nodes: documents, topics, people, projects, institutions, concepts
- 326 edges showing relationships
- Semantic relationships (e.g., "Gradient Flows" → "is_foundational_for" → "Diffusion Models")
- PageRank algorithm identifies key research areas
- Clean separation between data fetching and graph building

### 3. Semantic Search
- OpenAI embeddings for all documents and chunks
- Vector similarity search for conceptual queries
- Combined with graph traversal for context-aware results

### 4. Interactive Agent
- Natural language interface to explore research
- Multiple specialized tools for different query types
- Maintains conversation history
- Streams responses in real-time

## 🛠️ Usage Examples

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
python metadata_system/query_comprehensive.py
```

### Knowledge Graph
```bash
# Generate/update the knowledge graph
python metadata_system/knowledge_graph.py

# View in Gemini visualization
open Gemini_knowledge_graph/index.html
```

### Interactive Agent
```python
# Example queries:
"What papers has Vaios written about optimal transport?"
"How does his mathematical research connect to modern AI?"
"What projects involve reinforcement learning?"
"Show the evolution of his work from 2016 to 2025"
```

## 📊 Current Database Statistics

- **21 documents**: 12 academic papers + 9 chronicle notes
- **193 unique topics**: From "optimal transport" to "machine learning"
- **18 active projects**: Interactive CV, Collapsi RL, etc.
- **4 institutions**: WIAS Berlin, TU Berlin, Brown University, University of Bath
- **113 semantic chunks**: From academic paper analyses
- **20 semantic concepts**: Mathematical foundations → ML applications
- **19 semantic relationships**: Theory-to-practice connections

## 🗄️ Database Structure Requirements

The system expects the following SQLite database structure:

### Document Tables
```sql
-- Chronicle documents (daily notes, journals)
CREATE TABLE chronicle_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT,
    date DATE,
    content_hash TEXT,
    metadata JSON,
    embedding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic documents (papers, research)
CREATE TABLE academic_documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    title TEXT,
    date DATE,
    content_hash TEXT,
    metadata JSON,
    embedding BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Entity Tables
```sql
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE institutions (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);
```

### Relationship Tables
```sql
-- Document-to-entity relationships
CREATE TABLE document_topics (
    document_id INTEGER,
    topic_id INTEGER,
    PRIMARY KEY (document_id, topic_id)
);

CREATE TABLE document_people (
    document_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (document_id, person_id)
);

CREATE TABLE document_projects (
    document_id INTEGER,
    project_id INTEGER,
    PRIMARY KEY (document_id, project_id)
);

CREATE TABLE document_institutions (
    document_id INTEGER,
    institution_id INTEGER,
    PRIMARY KEY (document_id, institution_id)
);
```

### Optional Tables
```sql
-- For semantic relationships (optional but recommended)
CREATE TABLE semantic_concepts (
    concept_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    concept_type TEXT,
    description TEXT
);

CREATE TABLE semantic_relationships (
    id INTEGER PRIMARY KEY,
    source_type TEXT,
    source_id TEXT,
    target_type TEXT,
    target_id TEXT,
    relationship_type TEXT,
    description TEXT
);

-- For text chunks (used in RAG)
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    chunk_index INTEGER,
    content TEXT,
    embedding BLOB,
    metadata JSON
);
```

### Backward Compatibility View
```sql
-- View that combines both document types (for legacy queries)
CREATE VIEW documents_view AS
SELECT id, file_path, 'chronicle' as doc_type, title, date, 
       content_hash, metadata, embedding, created_at, modified_at
FROM chronicle_documents
UNION ALL
SELECT id, file_path, 'academic' as doc_type, title, date,
       content_hash, metadata, embedding, created_at, modified_at
FROM academic_documents;
```

### Knowledge Graph Data Format

When using the database-agnostic knowledge graph system, your data provider should return:

**Nodes Format:**
```json
{
    "id": "unique_identifier",
    "type": "document|topic|person|project|institution|concept",
    "label": "Human readable name",
    "additional_field": "any other attributes"
}
```

**Edges Format:**
```json
{
    "source": "source_node_id",
    "target": "target_node_id", 
    "relationship": "has_topic|mentions_person|relates_to_project|etc",
    "additional_field": "any other attributes"
}
```

### How the Knowledge Graph System Works

The knowledge graph system is now **completely database-agnostic** and consolidated into a single file (`metadata_system/knowledge_graph.py`). It contains:

1. **KnowledgeGraph Class**: Pure graph operations, no database knowledge
2. **DataProvider Interface**: Abstract interface for data sources  
3. **GenericSQLProvider**: Works with ANY SQLite database following conventions
4. **Main Function**: Simple orchestration

The system automatically extracts nodes and edges from your database without any hardcoded SQL. Just run:

```bash
python metadata_system/knowledge_graph.py
```

### Creating Custom Data Providers

The consolidated file includes everything you need. For non-SQL data sources, implement the `DataProvider` interface:

```python
from metadata_system.knowledge_graph import DataProvider, KnowledgeGraph

class MyDataProvider(DataProvider):
    def get_nodes(self):
        # Return list of nodes from your data source
        return [{
            'id': 'node_1',
            'type': 'document',
            'label': 'My Document',
            'custom_field': 'any value'
        }]
    
    def get_edges(self):
        # Return list of edges from your data source
        return [{
            'source': 'node_1',
            'target': 'topic_1',
            'relationship': 'has_topic'
        }]

# Use it
provider = MyDataProvider()
kg = KnowledgeGraph()
kg.add_nodes_batch(provider.get_nodes())
kg.add_edges_batch(provider.get_edges())
```

## 🔧 Configuration

### Environment Variables
```bash
OPENROUTER_API_KEY=     # For LLM metadata extraction
OPENAI_API_KEY=         # For embeddings
```

### Obsidian Setup
Edit `.sync/sync_chronicle_with_metadata.py`:
```python
"source": "/path/to/Obsidian/Chronicles/",
"local_dest": "chronicle/",
```

## 🚦 Development Workflow

1. **Add new chronicle notes**: Write in Obsidian → Run `chronicle` → Automatic extraction
2. **Add academic papers**: Place in `academic/` → Run import script → Generate embeddings
3. **Update knowledge graph**: Run `python metadata_system/knowledge_graph.py`
4. **Query the system**: Use `interactive_agent.py` or direct SQL queries

## 📈 Future Enhancements

- [ ] Web API (REST/GraphQL) for remote queries
- [ ] Interactive web UI for CV exploration
- [ ] Real-time RAG pipeline integration
- [ ] Export to various CV formats (PDF, JSON, etc.)
- [ ] Multi-language support
- [ ] Citation network analysis

## 🤝 Contributing

This is currently a personal project, but ideas and feedback are welcome!

## 📝 License

[Your chosen license]

---

Built with ❤️ to transform static CVs into living, intelligent representations of research journeys.