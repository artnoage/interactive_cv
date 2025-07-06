# Interactive CV System

## Blueprint-Driven Knowledge Platform

An AI-powered system that transforms academic research papers and personal notes into a dynamic, queryable professional profile. The system uses a blueprint-driven architecture that automatically generates tools from YAML specifications.

### Key Features

- **83+ automatically generated tools** from YAML blueprints
- **Semantic search** - hybrid SQL and embedding-based search
- **Centralized profile system** - consistent representation across all agents
- **Domain extension via configuration** - add new research areas through YAML files
- **Universal adaptability** - works for any research field
- **Schema consistency** - tools automatically match database structure

## 📋 Profile Setup (Required First Step)

### Centralized Profile System

The Interactive CV uses a **centralized profile system** that ensures consistent representation across all agents. Before running the system, you must customize your profile.

**Required Setup:**
1. **Edit `Profile/Profile_Prompt.md`** with your information:
   - Core identity and professional background
   - Research expertise with specific keywords
   - Professional experience and positions
   - Current focus areas and interests
   - Personal details and philosophy

2. **Both agents automatically load this profile** - no code changes needed

**Profile Template Structure:**
```markdown
### **Agent System Prompt: My Profile**

**1. Core Identity**
[Your background, PhD, experience]

**2. Executive Narrative** 
[Your career evolution and expertise]

**3. Research Expertise (Keywords)**
[Detailed technical areas for search optimization]

**4. Research Evolution & Key Contributions**
[Your research phases and major contributions]

**5. Professional Experience**
[Work history and institutional affiliations]

**6. Education**
[Academic background and degrees]

**7. Practical Implementation Experience**
[Technical skills, tools, and hands-on projects]

**8. Personal & Professional Profile**
[Work philosophy, interests, languages]
```

This centralized approach follows the blueprint philosophy: configuration over code, ensuring your profile is consistent across all system components.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd interactive_cv

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your profile (REQUIRED)
# Edit Profile/Profile_Prompt.md with your information:
# - Core identity and background
# - Research expertise and keywords  
# - Professional experience
# - Current focus areas
# - Personal details

# 4. Set up environment variables
cp .env.example .env
# Add your API keys:
# OPENROUTER_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here

# 5. Build database from scratch (complete pipeline)
python DB/build_database.py

# The build process automatically:
# - Validates all configurations
# - Creates database schema from blueprints
# - Imports all metadata with rich type preservation
# - Creates semantic chunks
# - Generates high-quality embeddings (text-embedding-3-large)
# - Deduplicates entities with 20 parallel workers
# - Builds knowledge graph with 24+ node types

# 6. Run the interactive agent (blueprint-powered with semantic intelligence)
python interactive_agent.py

# Or use Pro model for better instruction following
AGENT_MODEL=pro python interactive_agent.py

# Or use Claude 4 Sonnet for superior instruction following (recommended for complex queries)
AGENT_MODEL=claude python interactive_agent.py
```

## Current Status

- ✅ **Blueprint system operational** - 83+ tools generated from YAML
- ✅ **Semantic search integrated** - Hybrid SQL + embedding search
- ✅ **Database populated** - 12 academic papers, personal notes, 1000+ entities
- ✅ **Knowledge graph built** - 1,135 nodes, 1,249 relationships
- ⚠️ **LLM instruction following** - Complex multi-tool queries need improvement
- 🔄 **In progress** - Optimizing agent prompts for better tool orchestration

## Blueprint-Driven Architecture

### Architecture Overview

The system uses a configuration-driven approach where YAML blueprints define domain knowledge and tool generation

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  YAML Blueprints│     │ Tool Generator   │     │ 79 Sophisticated│
├─────────────────┤     ├──────────────────┤     │     Tools       │
│ extraction_schema│────▶│ Reads blueprints │────▶│ Schema-Driven   │
│ database_mapping │     │ Generates tools  │     │ Entity-Aware    │
│ visualization   │     │ Ensures safety   │     │ Relationship    │
│ database_schema │     │ NO manual coding │     │ Traversal       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               ↓
                    ┌──────────────────┐
                    │ Universal Agent  │
                    │ Uses generated   │
                    │ tools for ANY    │
                    │ research domain  │
                    └──────────────────┘

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

### Blueprint System Benefits

- **Automatic Tool Generation**: 83+ tools created from YAML specifications
- **Configuration-Based Extension**: Add research domains by editing YAML files
- **Domain-Agnostic**: Same codebase works for any research field
- **Schema Consistency**: Tools automatically match database structure
- **Rich Type Preservation**: Concepts maintain categories (24+ node types)
- **Collaborative Development**: Non-programmers can modify extraction rules
- **Reproducible Results**: Blueprint configurations ensure consistency
- **LLM-Compatible**: AI can help generate domain-specific blueprints
- **Version Control**: All domain knowledge tracked in git

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

## Entity Types & Knowledge Graph

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

## Implementation Status

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

## Blueprint System Usage

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

## Database Schema

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

## Visualization Configuration

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

## Interactive Web UI

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

## Development Workflow

### Adding New Document Types
1. Create `blueprints/new_type/extraction_schema.yaml` - Define what to extract
2. Create `blueprints/new_type/database_mapping.yaml` - Define how to store
3. Update `blueprints/core/visualization.yaml` with new node types - Define how to visualize
4. Run `python DB/build_database.py --validate-blueprints` - System validates and builds
5. Tools automatically generated for the new type

### Example: Adding Clinical Research Domain

```yaml
# blueprints/clinical/extraction_schema.yaml
fields:
  medical_procedures: {type: "list", description: "Medical procedures mentioned"}
  patient_outcomes: {type: "list", description: "Treatment outcomes"}
  clinical_trials: {type: "list", description: "Referenced clinical trials"}

# blueprints/clinical/database_mapping.yaml
entity_mappings:
  medical_procedures:
    target_table: "topics"
    relationship_type: "performs"
    category_override: "medical_procedure"
```

This generates tools including `search_clinical_topics()`, `traverse_performs()`, `explore_medical_categories()`, and visualization support.

### Blueprint Tool Categories (83 Generated Tools)

1. **Schema-Driven Tools (27 tools)**
   - `search_academic_documents`, `search_topics`, `search_people`, etc.
   - `get_*_by_id` tools for all entity types
   - `list_*` tools with pagination and filtering

2. **Entity-Aware Search (10 tools)**
   - `search_academic_topics`, `search_personal_people`
   - Domain-specific with category filtering

3. **Relationship Traversal (40 tools)**
   - **Forward**: `traverse_discusses`, `traverse_uses_method`, `traverse_authored_by`
   - **Reverse**: `reverse_discusses`, `reverse_authored_by`, `reverse_innovates`
   - Automatic discovery from entity mappings

4. **Semantic Intelligence Tools (4 tools)**
   - `semantic_search_chunks` - Find conceptually related content
   - `find_similar_entities` - Discover related concepts via embeddings
   - Query expansion and semantic enhancement

5. **Category & Visualization Tools (2 tools)**
   - `explore_topic_categories` with 22+ categories
   - `get_visualization_data` with complete styling

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

## Configuration

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

## Future Enhancements

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


## Advanced Agent System

The Interactive CV features a **multi-tier agent architecture** with progressive enhancements:

### Available Agents

1. **Original Agent** (`interactive_agent.py`) - Basic SQL keyword search
2. **Enhanced Agent** (`interactive_agent_enhanced.py`) - Adds semantic search with embeddings
3. **Advanced Agent** (`interactive_agent_advanced.py`) - Adds query planning for complex questions
4. **Ultimate Agent** (`interactive_agent_ultimate.py`) - Adds answer validation & knowledge graph exploration

### Key Features

- **20+ specialized tools** for comprehensive search and analysis
- **Semantic search** using OpenAI embeddings
- **Query planning** that breaks complex questions into steps
- **Answer validation** to reduce hallucination
- **Knowledge graph exploration** for entity relationships
- **Configurable models**: Gemini Flash 2.5 (fast) or Pro 2.5 (sophisticated)

### Usage

```bash
# Basic usage (Flash model)
python interactive_agent_ultimate.py

# Use Pro model for better results
AGENT_MODEL=pro python interactive_agent_ultimate.py

# Run tests with judge evaluation
AGENT_MODEL=pro JUDGE_MODEL=pro python tests/test_agent_with_judge.py

# Use the helper script
./run_with_models.sh pro pro ultimate
```

See [MODEL_USAGE_GUIDE.md](MODEL_USAGE_GUIDE.md) for detailed model configuration options.

## Documentation

### Core Documentation
- **[RAG System](RAG/README.md)**: Blueprint-driven tool generation
- **[Database System](DB/README.md)**: Database architecture and management
- **[Knowledge Graph](KG/README.md)**: Graph generation and visualization
- **[AI Agents](agents/README.md)**: Extraction and analysis agents
- **[Web UI](web_ui/README.md)**: Interactive visualization interface
- **[CLAUDE.md](CLAUDE.md)**: Comprehensive project documentation

## Contributing

This blueprint-driven system makes contributions easier! You can:
- Add new document types by creating blueprint YAML files
- Modify extraction schemas without touching Python code  
- Customize visualization by editing `visualization.yaml`
- Extend database schema via `database_schema.yaml`

## License

[Your chosen license]

