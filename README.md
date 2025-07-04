# Interactive CV System

An AI-powered system that transforms academic research papers and personal notes into a dynamic, queryable professional profile. Built with a **blueprint-driven architecture** that separates domain knowledge from code, enabling rich entity types and configurable processing.

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

# 4. Build database from scratch (complete pipeline)
python DB/build_database.py

# The build process automatically:
# - Validates all configurations
# - Creates database schema from blueprints
# - Imports all metadata with rich type preservation
# - Creates semantic chunks
# - Generates high-quality embeddings (text-embedding-3-large)
# - Deduplicates entities with 20 parallel workers
# - Builds knowledge graph with 24+ node types

# 5. Run the interactive agent
python interactive_agent.py
```

## 🏗️ Blueprint-Driven Architecture

The system is built with a revolutionary **blueprint-driven design** that completely separates domain knowledge from code:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  YAML Blueprints│     │ Generic Processors│     │ Rich Knowledge  │
├─────────────────┤     ├──────────────────┤     │     Graph       │
│ extraction_schema│────▶│ blueprint_driven │────▶│ 24+ Node Types  │
│ database_mapping │     │ components       │     │ Rich Relationships│
│ visualization   │     │ work with ANY    │     │ Configurable    │
│ database_schema │     │ document type    │     │ Visualization   │
└─────────────────┘     └──────────────────┘     └─────────────────┘

Blueprint Structure:
blueprints/
├── academic/          # Academic paper configurations
│   ├── extraction_schema.yaml     # 28 extraction fields  
│   └── database_mapping.yaml      # 15 entity mappings
├── personal/          # Personal notes configurations  
│   ├── extraction_schema.yaml     # 20 extraction fields
│   └── database_mapping.yaml      # 12 entity mappings
└── core/              # Domain-agnostic configurations
    ├── database_schema.yaml       # Complete database structure
    ├── visualization.yaml         # Node types, colors, layouts
    └── blueprint_loader.py        # Configuration parser
```

### 🎯 Key Blueprint Benefits

- **Domain-Agnostic Code**: DB and KG systems work with any domain
- **Rich Type Preservation**: Mathematical concepts keep original categories
- **Easy Extensibility**: Add new document types via YAML files
- **No Code Changes**: Modify behavior by editing blueprints
- **Validation**: Schema validation ensures blueprint correctness

## 📁 Project Structure

```
interactive_cv/
├── blueprints/            # YAML configuration files (NEW!)
│   ├── academic/         # Academic paper blueprints
│   ├── personal/         # Personal notes blueprints
│   └── core/            # Domain-agnostic blueprints
├── academic/             # Research papers and analyses
├── personal_notes/       # Daily and weekly notes
├── agents/               # LLM-based analyzers and extractors
│   ├── extractor.py                   # Generic document extractor
│   ├── academic_analyzer.py           # Paper analyzer
│   └── entity_deduplicator.py         # Deduplication
├── DB/                   # Database and processing system
│   ├── build_database.py              # Complete database builder
│   ├── update_database.py             # Incremental database updater (NEW!)
│   ├── populator.py                   # Generic metadata populator
│   ├── chunker.py                     # Document chunking
│   ├── embeddings.py                  # Vector embeddings
│   ├── populate_graph_tables.py       # Graph table population
│   └── utils/                         # Database utilities
│       ├── query_comprehensive.py     # Database exploration
│       └── verify_entities.py         # Entity verification
├── KG/                   # Knowledge Graph system
│   └── graph_builder.py               # Rich knowledge graph generator
├── RAG/                  # Retrieval-Augmented Generation system
│   └── graph_enhanced_query.py        # Intelligent RAG queries
├── .sync/                # Chronicle sync system
├── interactive_agent.py  # Conversational AI interface
├── serve_ui.py          # Unified Flask server (NEW!)
├── start_ui.sh          # Smart UI launcher (NEW!)
└── web_ui/              # Visualization interface
    ├── index.html       # Main UI with 3-panel layout
    └── knowledge_graph.json  # Pruned graph for performance
```

## 🔍 Rich Entity Types & Knowledge Graph

### Knowledge Graph Statistics (Latest)
- **Total Nodes**: 1,135 with 24+ distinct types
- **Total Edges**: 1,249 relationships
- **Rich Node Types**:
  - `math_foundation` (203): Core mathematical concepts
  - `person` (181): Authors and collaborators
  - `research_insight` (93): Key insights from papers
  - `personal_achievement` (71): Work accomplishments
  - `research_area` (47): Research domains
  - `theoretical_method`, `algorithmic_method`, `analytical_method`: Categorized methods
  - `future_direction`, `innovation`, `limitation`: Research aspects
  - `tool`, `institution`, `application`: Practical entities

### Advanced Categorization Examples
- **Mathematical Concepts**: `space` → `math_foundation`, `probability` → `math_foundation`
- **Methods**: `numerical` → `computational_method`, `proof` → `theoretical_method`
- **Personal Work**: `accomplishment` → `personal_achievement`, `learning` → `personal_learning`

## 📊 Current Status (2025-01-04 - Unified UI Server & Recent Fixes)

### Unified UI Server (NEW!)
✅ **Unified server implementation** - Single `serve_ui.py` replaces multiple scripts
✅ **Integrated Flask API** - Chat endpoint directly integrated with web UI
✅ **Pruned graph support** - Web UI prefers optimized graph from `web_ui/` folder
✅ **Smart launcher script** - `start_ui.sh` handles all prerequisites and services
✅ **Duplicate edge ID fix** - Resolved graph visualization conflicts
✅ **Favicon handling** - No more 404 errors in server logs
⚠️ **Panel sizing** - Currently fixed widths; resizable panels planned

### Interactive Agent Status (RECENT FIXES)
✅ **Threading issues resolved** - Fixed SQLite connection errors in multi-threaded environment
✅ **Enhanced content retrieval** - Tools now return 1500+ chars (vs 200 previously)
✅ **New search capabilities** - Added `get_paper_content` and enhanced `semantic_search_chunks`
✅ **Improved tool reliability** - All tools execute without errors
✅ **Comprehensive system prompt** - Enhanced agent with detailed research profile and expertise context
⚠️ **Search precision** - Using SQL LIKE queries; semantic embedding search recommended

### Database Statistics
- **19 documents**: 12 academic papers + 7 personal notes
- **Full content loaded**: Academic papers (20-29k chars), Personal notes (1.6-5.4k chars)
- **Entities with Rich Categories**:
  - **745 topics**: Categorized by domain (math_foundation, research_area, etc.)
  - **181 people**: Authors and collaborators
  - **132 methods**: Theoretical, computational, analytical categories
  - **24 institutions**: Universities and organizations
  - **21 applications**: Real-world use cases
  - **13 projects**: Research initiatives
- **1,249 relationships**: Categorized by type (discusses, proves, uses_method, etc.)
- **Document Processing**:
  - **38 chunks**: Created from academic documents (800-token chunks)
  - **285 entity-chunk mappings**: For precise entity location

### Processing Pipeline Status
✅ **Blueprint-driven architecture** - Complete domain separation
✅ **Rich entity type preservation** - 24+ node types instead of generic "topics"
✅ **Academic paper analysis and extraction**
✅ **Full content loading** - Fixed to load complete documents not just summaries
✅ **Configurable database population**
✅ **Semantic chunking with entity mapping** - Working for academic papers
✅ **High-quality embeddings** with text-embedding-3-large
✅ **Integrated entity deduplication** - 20 parallel workers with LLM verification
✅ **Blueprint-driven knowledge graph** with rich visualization
⏳ Personal notes chunking optimization (notes are shorter than chunk threshold)
⏳ Interactive web UI completion

## 🛠️ Blueprint System Usage

### 1. Build Database with Blueprints

```bash
# Complete build with validation (from scratch)
python DB/build_database.py --validate-blueprints

# Options:
# --backup              # Backup existing database
# --skip-embeddings     # Skip embedding generation  
# --skip-graph          # Skip knowledge graph generation
# --no-deduplication    # Skip automatic deduplication
# --db custom.db        # Use custom database name
```

### 2. Update Existing Database (NEW!)

```bash
# Incremental update - only process new documents
python DB/update_database.py

# The update process:
# - Detects new documents automatically
# - Only processes changes (no duplicates)
# - Checks and upgrades embedding model if needed
# - Runs deduplication on new entities only
# - Updates knowledge graph incrementally

# Options:
# --skip-embeddings     # Skip embedding generation
# --skip-graph          # Skip graph update
# --no-deduplication    # Skip deduplication
```

### 3. Extract Metadata Using Blueprints

```bash
# Extract academic papers (uses academic blueprints)
python agents/extractor.py academic \
  --input academic/ --output raw_data/academic/extracted_metadata/

# Extract personal notes (uses personal blueprints)
python agents/extractor.py personal \
  --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/
```

### 4. Generate Rich Knowledge Graph

```bash
# Generate graph with rich node types
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# View rich visualization
open web_ui/index.html
```

### 5. Validate Blueprint Configurations

```bash
# Check all blueprints for errors
python blueprints/core/blueprint_loader.py --validate
```

## 🗄️ Blueprint-Driven Database Schema

The database schema is entirely generated from `blueprints/core/database_schema.yaml`:

### Document Tables (Generated from Blueprint)
- `academic_documents`: Papers and analyses  
- `chronicle_documents`: Personal notes and logs

### Entity Tables (Generated from Blueprint)
- `topics`: Research concepts with rich categories
- `people`: Authors and collaborators
- `methods`: Techniques with type classification  
- `institutions`: Organizations and affiliations
- `applications`: Real-world use cases
- `projects`: Research initiatives

### Processing Tables (Generated from Blueprint)
- `relationships`: Unified relationship storage
- `document_chunks`: Semantic chunks for RAG
- `chunk_entities`: Entity-chunk mappings
- `embeddings`: Vector storage
- `graph_nodes`, `graph_edges`: Pre-computed graph

## 🎨 Blueprint Visualization Configuration

The `blueprints/core/visualization.yaml` defines:

```yaml
# Node type mappings - how database categories become visual types
node_type_mappings:
  topic:
    space: "math_foundation"
    optimization: "math_foundation"  
    numerical: "computational_method"
    proof: "theoretical_method"
    general: "general_topic"
    
# 28 distinct colors for node types
colors:
  math_foundation: "#FF6B35"     # Orange - mathematical concepts
  research_insight: "#4ECDC4"    # Teal - key insights
  personal_achievement: "#45B7D1" # Blue - accomplishments
  theoretical_method: "#96CEB4"   # Green - theory methods
  # ... 24 more types

# Layout grouping for better visualization
node_groups:
  academic: ["math_foundation", "research_area", "research_insight"]
  methods: ["theoretical_method", "computational_method", "analytical_method"]
  personal: ["personal_achievement", "personal_learning", "challenge"]
```

## 🌐 Interactive Web UI

Unified interface with knowledge graph visualization and AI-powered chat assistant.

### Features
- **3-panel layout**: Graph controls, interactive chat, and knowledge visualization
- **AI Chat Integration**: Talk directly with the Interactive CV assistant
- **24+ node types** with calm, soothing dark theme
- **Advanced filtering** by node and edge types
- **Real-time search** with automatic node highlighting
- **Conversation-aware graph**: Nodes highlight based on chat context
- **Responsive design** that works on mobile and desktop

### Running the Interactive UI
```bash
# Start the unified server (NEW!)
./start_ui.sh

# Or with database viewer (Datasette)
./start_ui.sh --with-datasette

# Then open: http://localhost:8888
```

### Unified Server Details
The new unified server (`serve_ui.py`) replaces previous separate scripts and includes:
- **Flask-based server** with integrated chat API
- **API endpoints**:
  - `/api/chat` - Interactive agent chat endpoint
  - `/api/stats` - Database statistics
  - `/knowledge_graph.json` - Graph data (prefers pruned version from `web_ui/`)
- **Automatic handling**:
  - Favicon requests (returns 204 to prevent 404s)
  - CORS for API access
  - Pruned graph preference for better performance
- **Smart launcher** (`start_ui.sh`):
  - Checks for required database and graph files
  - Generates knowledge graph if missing
  - Manages optional Datasette integration
  - Handles graceful shutdown

## 🚦 Development Workflow

### Adding New Document Types
1. Create `blueprints/new_type/extraction_schema.yaml`
2. Create `blueprints/new_type/database_mapping.yaml`  
3. Update `blueprints/core/visualization.yaml` with new node types
4. Run `python DB/build_database.py --validate-blueprints`
5. System automatically supports the new type!

### Modifying Entity Categories
1. Edit `blueprints/academic/database_mapping.yaml` or `blueprints/personal/database_mapping.yaml`
2. Update `blueprints/core/visualization.yaml` node mappings
3. Rebuild database: `python DB/build_database.py`
4. New categories appear automatically in the knowledge graph

### Chronicle Sync (Personal Notes)
```bash
# Regular sync with blueprint-driven extraction
chronicle

# Dry run to see what would change
chronicle-dry

# Force re-extraction using current blueprints
chronicle-force
```

## 🔧 Configuration

### Environment Variables
```bash
OPENROUTER_API_KEY=     # For LLM analysis and extraction
OPENAI_API_KEY=         # For embeddings
```

### Blueprint Customization
Edit YAML files in `blueprints/` to modify:
- Extraction schemas (what fields to extract)
- Database mappings (how fields map to entities)
- Visualization rules (node types, colors, layouts)
- Database schema (table structure, indexes)

## 📈 Future Enhancements

### Completed ✅
- [x] Blueprint-driven architecture with complete domain separation
- [x] Rich entity type preservation (24+ node types)
- [x] Configurable visualization with 28 colors and 7 groups
- [x] Generic extraction/population/graph systems
- [x] Entity deduplication with LLM verification
- [x] High-quality embeddings (text-embedding-3-large)

### In Progress 🚧
- [ ] Resizable UI panels for better customization
- [ ] Web API (REST/GraphQL) for remote queries  
- [ ] Real-time RAG pipeline integration
- [ ] Export to various CV formats (PDF, JSON, etc.)
- [ ] Semantic embedding search integration

### Future 🔮
- [ ] Multi-language blueprint support
- [ ] Citation network analysis
- [ ] Automated paper discovery and import
- [ ] Blueprint marketplace for different research domains

## 🏆 Blueprint System Advantages

1. **Zero Code Changes**: Add new document types via YAML
2. **Rich Type System**: 24+ entity types vs generic "topics"
3. **Domain Flexibility**: Same code works for any research field
4. **Easy Debugging**: All logic is in readable YAML files
5. **Collaborative**: Non-programmers can modify extraction rules
6. **Version Control**: Blueprint changes are tracked in git
7. **Validation**: Schema validation prevents configuration errors

## 🐛 Troubleshooting

### Common Issues

1. **Empty document_chunks table**
   - **Cause**: Documents only containing summaries instead of full content
   - **Fix**: Ensure populator loads full content from analysis files (fixed in latest version)

2. **Personal notes not chunked**
   - **Cause**: Personal notes are shorter than minimum chunk size (300 tokens)
   - **Fix**: Adjust `min_chunk_size` in `build_database.py` or use different chunking strategy

3. **Blueprint file not found errors**
   - **Cause**: Relative path issues when running from different directories
   - **Fix**: Always run scripts from project root or use absolute paths

4. **Deduplication taking too long**
   - **Cause**: Too many false positive pairs to check
   - **Fix**: Increase similarity threshold or use `--no-deduplication` flag

5. **Duplicate edge IDs in knowledge graph**
   - **Cause**: Edge ID generation not ensuring uniqueness
   - **Fix**: Updated in latest version; regenerate graph with `python KG/graph_builder.py`

6. **Web UI panel sizes**
   - **Issue**: Fixed panel widths may be too small for knowledge graph
   - **Workaround**: Zoom out browser or use larger display
   - **Fix**: Resizable panels planned for next update

## 📚 Documentation

For detailed information on specific components:
- **[Database System](DB/README.md)**: Complete database architecture and management
- **[Knowledge Graph](KG/README.md)**: Graph generation and visualization system
- **[AI Agents](agents/README.md)**: Extraction and analysis agents
- **[Web UI](web_ui/README.md)**: Interactive visualization interface

## 🤝 Contributing

This blueprint-driven system makes contributions easier! You can:
- Add new document types by creating blueprint YAML files
- Modify extraction schemas without touching Python code  
- Customize visualization by editing `visualization.yaml`
- Extend database schema via `database_schema.yaml`

## 📝 License

[Your chosen license]

---

Built with ❤️ and **blueprints** to transform static CVs into living, intelligent representations of research journeys.