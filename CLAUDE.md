# Interactive CV Project - CLAUDE.md

## 🚀 Embedding-First Agent Overview

The Interactive CV uses a **simplified embedding-first agent** that leverages semantic search across all entities.

**Key Achievement**: *3 unified tools with semantic search replace 83+ specific tools*

### System Architecture

- **`interactive_agent.py`** - Main agent with 3 embedding-based tools and semantic intelligence
- **Blueprint Configuration** - YAML files define all domain knowledge for database building
- **Semantic Enhancement** - Hybrid SQL + embedding search for concept discovery
- **Centralized Profile** - Consistent biography from Profile/ directory

### The 3 Tools

1. **`semantic_search`** - Search across ALL entity types using embeddings
   - Finds documents, topics, people, methods, institutions, applications, projects
   - Handles synonyms and name variations automatically
   - Returns relevance scores

2. **`navigate_relationships`** - Traverse the knowledge graph
   - Forward mode: Find what an entity points to (e.g., paper → topics)
   - Reverse mode: Find what points to an entity (e.g., person → papers)
   - Critical for multi-hop queries (e.g., person → papers → institutions)

3. **`get_entity_details`** - Get full information about any entity
   - Returns all attributes and content
   - Works with any entity type

### Usage

```bash
# Run the interactive agent
python interactive_agent.py

# Use Claude for better instruction following (recommended)
AGENT_MODEL=claude python interactive_agent.py

# Use Pro model
AGENT_MODEL=pro python interactive_agent.py
```

## 📂 Blueprint Structure

```
blueprints/
├── academic/          # Academic paper configurations
│   ├── extraction_schema.yaml     # Extraction fields
│   └── database_mapping.yaml      # Entity mappings
├── personal/          # Personal notes configurations  
│   ├── extraction_schema.yaml
│   └── database_mapping.yaml
└── core/              # Domain-agnostic configurations
    ├── database_schema.yaml       # Database structure
    ├── visualization.yaml         # Node types, colors
    └── tool_guidance.yaml         # Tool usage patterns
```

## 📊 Current Status

- **Database**: 12 academic papers, 7 personal notes with full content
- **Entities**: 745 topics, 181 people, 132 methods, 24 institutions
- **Knowledge Graph**: 1,135 nodes with 24+ rich types, 1,249 relationships
- **Semantic Search**: Integrated OpenAI embeddings with SQL queries
- **Performance**: 90/100 on complex queries (vs 0/100 previously)

## 🛠️ Core Commands

### Database Management

```bash
# Build database from scratch
python DB/build_database.py

# Incremental update (new documents only)
python DB/update_database.py

# Extract metadata using blueprints
python agents/extractor.py academic --input academic/ --output raw_data/academic/extracted_metadata/
python agents/extractor.py personal --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/
```

### Chronicle Sync

```bash
chronicle              # Regular sync with metadata extraction
chronicle-dry          # Dry run
chronicle-force        # Force re-extraction
chronicle-status       # Check configuration
```

### Visualization

```bash
# View database
./view_database.sh

# Generate knowledge graph
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# Launch unified UI
./start_ui.sh
./start_ui.sh --with-datasette
```

## 🎯 Profile Setup

1. Edit `Profile/Profile_Prompt.md` with your information:
   - Core identity and background
   - Research expertise
   - Professional experience
   - Current focus areas

2. The agent automatically loads this profile - no code changes needed

## 🔧 Technical Details

### Key Components

- **`interactive_agent.py`** - Main agent with 3 embedding-based tools
- **`RAG/semantic_search.py`** - Semantic search engine for all entities
- **`DB/build_database.py`** - Database builder using blueprints
- **`KG/graph_builder.py`** - Graph generator with rich node types
- **`serve_ui.py`** - Flask server for unified web interface

### Environment Setup

```bash
# Required API keys in .env:
OPENROUTER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Best Practices

- Use `uv` for package management
- Run scripts from project root
- Keep domain knowledge in YAML for database building
- Use incremental updates for new documents

## 🚀 Embedding-First Agent Benefits

1. **Simple Tools**: Just 3 tools handle all queries
2. **Semantic Search**: Finds concepts regardless of exact terms
3. **Entity Resolution**: Handles name variations automatically
4. **Rich Types**: 24+ entity categories with visualization
5. **Scalable**: Works with any number of entities

## 📈 Recent Improvements

- **Semantic Intelligence**: Hybrid search with embeddings
- **Unified UI**: Integrated chat and graph visualization
- **Thread-Safe**: Fixed SQLite threading issues
- **Content Loading**: Full document content (20-29k chars)
- **Profile System**: Centralized biography management

## 🎯 Known Issues & Solutions

### Complex Queries
- Multi-hop queries (like finding author institutions) work better with Claude model
- Use `AGENT_MODEL=claude` for superior instruction following

### Personal Notes Chunking
- Shorter notes may not be chunked (below 300 token threshold)
- Adjust chunk parameters in `build_database.py` if needed

### Tips
- For complex queries, use Claude model: `AGENT_MODEL=claude`
- View SQL queries directly with datasette: `./view_database.sh`

## Summary

The Interactive CV is an **embedding-first knowledge platform** that:
- Uses just 3 unified tools powered by semantic search
- Works universally across any research domain  
- Combines SQL queries with semantic embeddings
- Provides both CLI and web interfaces
- Uses blueprints for database building while keeping the agent simple

*From 83 specific tools to 3 intelligent tools - simplicity through semantic search.*