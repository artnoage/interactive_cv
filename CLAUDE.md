# Interactive CV Project - CLAUDE.md

## 🚀 Blueprint-Driven System Overview

The Interactive CV has been transformed into a **blueprint-driven system** that automatically generates tools from YAML configurations.

**Key Achievement**: *83+ automatically generated tools from blueprints vs 13 manual tools (6.4x improvement)*

### System Architecture

- **`interactive_agent.py`** - Main agent with blueprint-generated tools and semantic intelligence
- **Blueprint Configuration** - YAML files define all domain knowledge and tool generation
- **Semantic Enhancement** - Hybrid SQL + embedding search for concept discovery
- **Centralized Profile** - Consistent biography from Profile/ directory

### Usage

```bash
# Run the interactive agent
python interactive_agent.py

# Use Claude for better instruction following (recommended)
AGENT_MODEL=claude python interactive_agent.py

# Use Pro model
AGENT_MODEL=pro python interactive_agent.py

# Validate blueprint configurations
python RAG/blueprint_driven_loader.py
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

2. Both agents automatically load this profile - no code changes needed

## 🔧 Technical Details

### Key Components

- **`RAG/blueprint_driven_loader.py`** - Parses YAML blueprints
- **`RAG/blueprint_driven_tools.py`** - Generates 83+ tools automatically
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
- Validate blueprints before production builds
- Keep domain knowledge in YAML, not code
- Use incremental updates for new documents

## 🚀 Blueprint System Benefits

1. **Zero-Code Extension**: Add domains via YAML only
2. **Universal Platform**: Works for any research field
3. **Schema-Safe**: Tools match database automatically
4. **Rich Types**: 24+ entity categories with visualization
5. **Collaborative**: Non-programmers can modify rules

## 📈 Recent Improvements

- **Semantic Intelligence**: Hybrid search with embeddings
- **Unified UI**: Integrated chat and graph visualization
- **Thread-Safe**: Fixed SQLite threading issues
- **Content Loading**: Full document content (20-29k chars)
- **Profile System**: Centralized biography management

## 🎯 Known Issues & Solutions

### Multi-Tool Orchestration
- Complex queries requiring tool chaining work better with Claude model
- Use `AGENT_MODEL=claude` for superior instruction following

### Personal Notes Chunking
- Shorter notes may not be chunked (below 300 token threshold)
- Adjust chunk parameters in `build_database.py` if needed

### Tips
- For complex queries, use Claude model: `AGENT_MODEL=claude`
- View SQL queries directly with datasette: `./view_database.sh`
- Check tool generation: `python RAG/blueprint_driven_tools.py`

## Summary

The Interactive CV is a **blueprint-driven knowledge platform** that:
- Generates 83+ tools automatically from YAML configurations
- Works universally across any research domain
- Combines SQL queries with semantic embeddings
- Provides both CLI and web interfaces
- Maintains all domain knowledge in version-controlled blueprints

*From manual coding to automatic tool generation - a 6.4x improvement in capabilities through configuration.*