# Interactive CV Project - CLAUDE.md

## 🚀 Embedding-First Agent Overview

The Interactive CV uses a **unified tool agent** that leverages semantic search across all entities with advanced reasoning capabilities.

**Key Achievement**: *6 unified tools with semantic search + MCP integration provide comprehensive functionality*

### System Architecture

- **`interactive_agent.py`** - Main agent with 6 unified tools and semantic intelligence
- **Pep Talk Coach** - Motivational agent that prevents lazy responses and ensures tool usage
- **Blueprint Configuration** - YAML files define all domain knowledge for database building
- **Semantic Enhancement** - Hybrid SQL + embedding search for concept discovery
- **MCP Integration** - Real Model Context Protocol for structured reasoning
- **Centralized Profile** - Consistent biography from Profile/ directory

### The 6 Unified Tools

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

4. **`list_available_papers`** - Paper catalog access
   - Shows complete list of papers in the system
   - Useful for understanding available research scope

5. **`consult_manuscript`** - Deep document analysis (META TOOL)
   - Manuscript Agent integration for original document access
   - Specialized multi-tool agent with file reading capabilities
   - Used when database search isn't detailed enough

6. **`sequential_reasoning`** - Structured analysis (META TOOL)
   - Real MCP (Model Context Protocol) integration
   - Step-by-step reasoning for complex cross-domain questions
   - JSON-RPC communication with dedicated MCP server subprocess

### The Pep Talk Coach 🎯

A **quality assurance agent** that intervenes ONLY when the agent provides truly non-informative responses:

- **Strict Intervention** - Only activates when answers have no useful information at all
- **Single Intervention** - Maximum of one pep talk per conversation to prevent loops
- **Answer Quality Focus** - Evaluates response content, not question patterns
- **General Guidance** - Provides actionable advice without seeing the original question
- **Non-Informative Detection** - Catches planning statements, generic IDs, error messages, very short responses

**Key Features**:
- Only triggers on truly empty or non-informative responses
- Eliminates coaching loops that could block good answers
- Maintains high quality scoring (e.g., risk-sensitive POMDP question scores 95/100)

**Evolution from v1 to v2**:
- **v1**: Intervened too frequently, sometimes blocking good answers
- **v2**: Smarter detection - only intervenes for truly non-informative responses
- **Result**: Better performance on complex questions without unnecessary interruptions

**Workflow**: User → Agent → Tools → **Quality Check** → (Pep Talk if needed) → User

This ensures quality responses without blocking legitimate answers that contain real information!

### Usage

```bash
# Run the interactive agent
python interactive_agent.py

# Use Claude for best instruction following (recommended)
AGENT_MODEL=claude python interactive_agent.py

# Use Flash for cost-effective performance with coaching
AGENT_MODEL=flash python interactive_agent.py

# Use Pro model for sophisticated analysis
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

- **Database**: 19 documents (12 academic papers + 7 personal notes) with full content
- **Entities**: 1,135 entities with 24+ rich types (745 topics, 181 people, 132 methods, 24 institutions)
- **Knowledge Graph**: Rich categorization with 1,249 typed relationships
- **Semantic Search**: OpenAI text-embedding-3-large (3072 dimensions)
- **MCP Integration**: Real JSON-RPC subprocess communication for structured reasoning
- **Performance**: Best scores ever achieved with Pep Talk Coach + MCP system
- **Quality Control**: Smart coaching system prevents non-informative responses only when needed
- **Test Suite**: 40 comprehensive test questions with automated evaluation
- **Remote Deployment**: Successfully deployed with environment configuration
- **Chronicle Sync**: Automated Obsidian to remote server synchronization

## 🛠️ Core Commands

### Database Management

```bash
# Academic Paper Workflow (3 steps)
# 1. Analyze papers for deep insights
python agents/academic_analyzer.py --input academic/ --output raw_data/academic/generated_analyses/

# 2. Extract structured metadata from analyses
python agents/extractor.py academic --input raw_data/academic/generated_analyses/ --output raw_data/academic/extracted_metadata/

# 3. Build database from all metadata
python DB/build_database.py

# Personal Notes Workflow (2 steps)
# 1. Extract metadata directly from notes
python agents/extractor.py personal --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/

# 2. Update database (if already built)
python DB/update_database.py
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

1. The system includes a **built-in profile** for Vaios Laschos:
   - Profile is embedded in `Profile/profile_loader.py` for reliability
   - No manual setup required - works out of the box
   - Includes complete identity, research expertise, and professional experience
   - To customize: Edit the `prompt_content` in `ProfileLoader._load_agent_prompt()`

2. The agent automatically loads this built-in profile - fully self-contained

## 🔧 Technical Details

### Key Components

- **`interactive_agent.py`** - Main agent with 6 unified tools + MCP integration
- **`RAG/semantic_search.py`** - Semantic search engine for all entities
- **`DB/build_database.py`** - Database builder using blueprints
- **`KG/graph_builder.py`** - Graph generator with rich node types
- **`serve_ui.py`** - Flask server for unified web interface
- **`mcp_subfolder/`** - Model Context Protocol implementation
- **`.sync/chronicle_sync.py`** - Obsidian to remote server synchronization

### Environment Setup

```bash
# Required API keys in .env:
OPENROUTER_API_KEY=your_key_here    # For LLM agents (Gemini, Claude models)
OPENAI_API_KEY=your_key_here        # For embeddings (text-embedding-3-large)

# Optional environment variables:
AGENT_MODEL=claude                  # Model selection (claude, flash, pro)
```

### Best Practices

- Use `uv` for package management
- Run scripts from project root
- Keep domain knowledge in YAML for database building
- Use incremental updates for new documents

## 🚀 Unified Agent Benefits

1. **Comprehensive Tools**: 6 unified tools handle all query types from simple to complex
2. **Semantic Intelligence**: Finds concepts regardless of exact terms using high-quality embeddings
3. **Entity Resolution**: Handles name variations and synonyms automatically
4. **Rich Types**: 24+ entity categories with professional visualization
5. **Structured Reasoning**: Real MCP integration for complex cross-domain analysis
6. **Quality Assurance**: Smart Pep Talk Coach intervenes only for truly non-informative responses
7. **Universal Scalability**: Works with any number of entities across any domain
8. **Deployment Ready**: Successfully configured for remote server deployment

## 📈 Recent Improvements

### Agent System Enhancements
- **MCP Integration**: Real Model Context Protocol with JSON-RPC subprocess communication
- **Tool Expansion**: 6 unified tools including manuscript consultation and structured reasoning
- **Smart Quality Assurance**: Pep Talk Coach v2 only intervenes for truly non-informative responses
- **Targeted Detection**: Only catches planning statements, generic IDs, error messages, and very short responses
- **Performance Optimization**: Coaching loops eliminated for complex questions (achieving 95/100 scores)

### Infrastructure Improvements
- **Chronicle Sync**: Automated sync from Obsidian Chronicles to remote server
- **Remote Deployment**: Successfully deployed with proper environment configuration
- **Database Expansion**: 19 documents with 1,135 entities and rich categorization
- **Test Suite**: 40 comprehensive test questions with automated evaluation
- **High-Quality Embeddings**: OpenAI text-embedding-3-large (3072 dimensions)
- **Thread-Safe**: SQLite threading optimized for web deployment
- **Content Loading**: Full document content (20-29k chars academic, 1.6-5.4k personal)
- **Blueprint System**: Mature YAML-driven configuration for universal domain adaptation

## 🎯 Known Issues & Solutions

### Model Performance
- **Claude**: Best instruction following and complex reasoning (recommended for critical analysis)
- **Flash + Pep Talk Coach**: Excellent performance at 1/10th the cost (recommended for daily use)
- **Pro**: Most sophisticated analysis capabilities

### Environment Configuration
- **Local vs Remote**: Ensure `.env` file is properly configured on remote deployments
- **LangChain Versions**: Keep updated for latest tool calling and MCP compatibility
- **Database Access**: Verify working directory and SQLite permissions in deployment

### Deployment Tips
- Set `AGENT_MODEL=claude` for best results in production
- Use `chronicle` command for automated Obsidian sync
- Monitor database size and consider chunking adjustments for very large documents
- View SQL queries directly with datasette: `./view_database.sh`

## Summary

The Interactive CV is a **unified knowledge platform** with **MCP-powered reasoning** and **smart quality assurance** that:
- Uses 6 unified tools powered by semantic search and structured reasoning
- Features intelligent Pep Talk Coach that ensures quality responses
- Integrates real Model Context Protocol for complex cross-domain analysis
- Works universally across any research domain via blueprint configuration
- Combines high-quality embeddings with SQL queries and graph navigation
- Provides CLI, web interface, and automated synchronization workflows
- Successfully deployed to remote servers with proper environment configuration

*6 intelligent tools + MCP reasoning + motivational coaching achieve exceptional performance through semantic intelligence and quality assurance.*