# Interactive CV Project - CLAUDE.md

## 🎯 Configuration-Driven Architecture

### Revolutionary Design: Complete Domain-Code Separation

The system uses a **configuration-driven architecture** that fundamentally separates domain knowledge from code:

**🏗️ System Design:**
```
YAML Blueprints → Generic Code → Rich Knowledge Graph with 24+ Node Types
```

**📂 Blueprint Structure:**
```
blueprints/
├── academic/          # Academic paper configurations
│   ├── extraction_schema.yaml     # 28 extraction fields with validation
│   └── database_mapping.yaml      # 15 entity mappings with rich categories
├── personal/          # Personal notes configurations  
│   ├── extraction_schema.yaml     # 20 extraction fields
│   └── database_mapping.yaml      # 12 entity mappings
└── core/              # Domain-agnostic configurations
    ├── database_schema.yaml       # Complete database structure (auto-generated)
    ├── visualization.yaml         # 28 node types, colors, layouts
    └── blueprint_loader.py        # Configuration parser with validation
```

**🎨 Rich Entity Types:**
- **Math Foundation** (203 nodes): Core mathematical concepts like "Optimal Transport"
- **Research Insights** (93): Key insights and discoveries
- **Personal Achievements** (71): Work accomplishments and progress
- **Method Categories**: `theoretical_method`, `algorithmic_method`, `computational_method`
- **Research Aspects**: `future_direction`, `innovation`, `limitation`, `assumption`

**🔧 Main Components:**
- `DB/build_database.py` - Complete database builder using blueprints
- `DB/populator.py` - Generic metadata importer
- `KG/graph_builder.py` - Rich graph generator with 24+ node types
- `agents/extractor.py` - Configurable metadata extractor

**✅ Key Achievements:**
1. **Zero Code Changes**: Add new document types via YAML files
2. **Rich Type Preservation**: Mathematical concepts keep original categories  
3. **Complete Domain Separation**: DB folder has NO domain knowledge
4. **24+ Node Types**: vs previous generic "topics"
5. **28 Visualization Colors**: Distinct colors for each entity type
6. **7 Layout Groups**: Organized visualization groupings
7. **Schema Validation**: Prevents configuration errors

**🚀 Impact:**
- **1,135 nodes** with rich typing
- **1,249 relationships** with proper categorization
- **Configurable visualization** with domain-specific colors
- **Extensible to any research domain** without code changes

## Project Overview

This project creates an **Interactive CV System** that transforms academic research papers and personal notes into a dynamic, queryable professional profile. The system uses AI to extract metadata, build a knowledge graph, and enable intelligent conversations about your research expertise and work history.

**Core Purpose**: Build a RAG-powered interactive CV that can answer questions about your research, skills, and experience by analyzing your academic papers and daily notes.

## System Architecture

### Data Sources
1. **Academic Papers** (`/academic/`)
   - Paper transcripts (PDFs → Markdown)
   - Detailed analyses of each paper
   - Mathematical concepts, methods, applications

2. **Personal Notes** (`/personal_notes/`)
   - Daily notes with work progress
   - Weekly summaries
   - Project updates and insights

### Database System Design

We use a **normalized SQLite database** with clean entity-relationship structure:

**Core Tables:**
- **Document Tables**: 
  - `chronicle_documents`: Daily/weekly notes from personal notes
  - `academic_documents`: Research papers and analyses
- **Entity Tables** (with attributes):
  - `topics`: Mathematical concepts, research areas (name, category, description)
  - `people`: Authors, collaborators (name, role, affiliation)
  - `projects`: Research projects (name, description, dates)
  - `institutions`: Universities, research centers (name, type, location)
  - `methods`: Algorithms, techniques (name, category, description)
  - `applications`: Real-world uses (name, domain, description)
- **Relationship & Graph**:
  - `relationships`: Single unified table for ALL connections
  - `graph_nodes` & `graph_edges`: Pre-computed for visualization
  - `document_chunks`: Semantic segments for RAG
  - `chunk_entities`: Maps entities to chunks
  - `embeddings`: Vector storage for all entities

**Design Principles:**
- Single source of truth (no duplicate data)
- Graph-ready structure with pre-computed metrics
- Flexible JSON metadata fields for extensibility
- Unified ID format: `{type}_{id}` (e.g., 'academic_1', 'chronicle_2')

## File Structure (Configuration-Driven Architecture)

```
/interactive_cv/
├── blueprints/             # YAML configuration files
│   ├── academic/           # Academic paper blueprints
│   │   ├── extraction_schema.yaml     # 28 extraction fields with validation
│   │   └── database_mapping.yaml      # 15 entity mappings with rich categories
│   ├── personal/           # Personal notes blueprints  
│   │   ├── extraction_schema.yaml     # 20 extraction fields
│   │   └── database_mapping.yaml      # 12 entity mappings
│   └── core/               # Domain-agnostic blueprints
│       ├── database_schema.yaml       # Complete database structure
│       ├── visualization.yaml         # 28 node types, colors, layouts
│       └── blueprint_loader.py        # Configuration parser
├── academic/               # Research papers and analyses
├── personal_notes/         # Daily/weekly notes
├── DB/                     # Database and processing system
│   ├── build_database.py              # Complete builder using blueprints
│   ├── populator.py                   # Generic metadata importer
│   ├── embeddings.py                  # Vector embedding generation
│   ├── chunker.py                     # Smart document chunking
│   ├── populate_graph_tables.py       # Graph table populator
│   ├── metadata.db                    # SQLite database (not in git)
│   ├── query_comprehensive.py         # Database exploration tool
│   ├── verify_entities.py             # Entity verification and stats
│   └── README.md                      # Comprehensive DB architecture docs
├── KG/                     # Knowledge Graph system
│   ├── graph_builder.py               # Rich graph generator with 24+ node types
│   └── graph_enhanced_query.py        # Graph-aware query system
├── agents/                 # LLM analyzers and extractors
│   ├── extractor.py                   # Generic extractor for any document type
│   ├── academic_analyzer.py           # Academic paper analyzer
│   └── entity_deduplicator.py         # Entity deduplication with LLM verification
├── Profile/                # Academic profile documents
│   ├── Profile.md          # Detailed academic profile
│   └── cv.md              # Generated CV
├── .sync/                  # Chronicle sync system
│   ├── sync-chronicle      # Shell wrapper
│   └── sync_chronicle_with_metadata.py  # Main sync logic
├── interactive_agent.py    # Conversational interface
├── requirements.txt        # Python dependencies
├── view_database.sh        # Launch Datasette viewer
├── README.md              # Project overview
└── CLAUDE.md              # This file (detailed documentation)
```

## Current Status

### Configuration-Driven Architecture Status
- **Architecture**: Complete configuration-driven system with domain-code separation
- **Database**: Rich entity types with 24+ distinct node categories
- **Academic Papers**: 12 papers successfully processed with configuration extractors
- **Chronicle Notes**: 7 notes processed with configuration-driven personal extractors
- **Entities with Rich Categories**:
  - 745 topics: Categorized by domain (math_foundation: 203, research_area: 47, etc.)
  - 181 people: Authors, researchers, and collaborators  
  - 132 methods: Theoretical (25), computational (2), analytical (22), general (28), algorithmic (23)
  - 24 institutions: Universities and research centers
  - 21 applications: Real-world use cases
  - 13 projects: Research and development projects
- **Document Processing**:
  - Configuration-driven chunking system
  - Rich type preservation during extraction
  - 1,249 relationships established with proper categorization
- **Knowledge Graph**: 1,135 nodes with 24+ rich types and 1,249 relationships
  - **Rich Node Types**: math_foundation, research_insight, personal_achievement, etc.
  - **Configurable Visualization**: 28 colors, 7 layout groups
  - **Configuration-driven generation**: No hardcoded mappings
- **Pipeline Status**: ✅ Configuration architecture complete, ✅ Rich types preserved, ✅ Configurable extraction, ✅ Domain-agnostic code

## Usage

### Configuration-Driven Database Management

The system uses a revolutionary configuration-driven architecture that separates all domain knowledge from code:

```
YAML Blueprints → Schema Generation → Rich Entity Extraction → Database → Rich Knowledge Graph
```

#### 1. Build Database with Configuration System
```bash
# Complete configuration-driven rebuild with rich entity types
python DB/build_database.py

# This script includes:
# 1. Validates all blueprint configurations
# 2. Creates database schema from blueprints/core/database_schema.yaml
# 3. Imports metadata with rich type preservation (24+ node types)
# 4. Chunks documents intelligently (1000-1500 tokens)
# 5. Maps entities to chunks for granular search
# 6. Generates high-quality embeddings with text-embedding-3-large
# 7. Deduplicates entities automatically (20 parallel workers)
# 8. Builds knowledge graph with configuration-driven visualization

# Options:
python DB/build_database.py --validate-blueprints  # Validate YAML configs first
python DB/build_database.py --backup               # Backup existing database
python DB/build_database.py --skip-embeddings      # Skip embedding generation
python DB/build_database.py --no-deduplication     # Skip automatic deduplication
python DB/build_database.py --skip-graph           # Skip graph population
python DB/build_database.py --db custom.db         # Use custom database name
```

#### 2. Extract Metadata Using Blueprints
```bash
# Extract academic papers (uses blueprints/academic/ configurations)
python agents/extractor.py academic \
  --input academic/ --output raw_data/academic/extracted_metadata/

# Extract personal notes (uses blueprints/personal/ configurations)  
python agents/extractor.py personal \
  --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/

# Options:
# --model google/gemini-2.5-flash    # LLM model to use
# --pattern "*.md"                   # File pattern to process
```

### Chronicle Sync Commands
After setting up, use these commands from anywhere:

```bash
# Regular sync with metadata extraction
chronicle

# Dry run - see what would change
chronicle-dry

# Force re-extraction of all metadata
chronicle-force

# Check sync configuration
chronicle-status
```

### What the sync does:
1. Syncs from Obsidian Chronicles folder to local
2. Detects new/changed files using content hashes
3. Extracts metadata using LLM (topics, people, projects)
4. Generates embeddings for semantic search
5. Syncs both files and database to remote server

## Visualization & Analysis

### Database Viewer (Datasette)
```bash
./view_database.sh  # Launches Datasette on http://localhost:8001
```

Features:
- Browse all tables interactively
- Run SQL queries with autocomplete
- Export data in JSON/CSV formats
- Automatic API generation for queries
- Faceted search and filtering

### Rich Knowledge Graph
```bash
# Generate graph with rich entity types using blueprints
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# Validate blueprint configurations
python KG/graph_builder.py --validate-blueprints

# View rich visualization
open web_ui/index.html
```

Graph Statistics (Configuration-Driven):
- **Current**: 1,135 nodes, 1,249 edges (✅ rich types, configuration-generated)
- **Rich Node Types (24+ categories)**:
  - 🧠 **math_foundation** (203): Core mathematical concepts like "Optimal Transport"
  - 👤 **person** (181): Authors, researchers, collaborators  
  - 💡 **research_insight** (93): Key insights and discoveries
  - 🏆 **personal_achievement** (71): Work accomplishments and progress
  - 🔬 **research_area** (47): Research domains and fields
  - 📐 **theoretical_method** (25): Proof techniques, analytical approaches
  - 💻 **computational_method** (2): Numerical and algorithmic techniques
  - 🔍 **analytical_method** (22): Analysis and evaluation methods
  - 🛠️ **general_method** (28): General techniques and approaches
  - ⚙️ **algorithmic_method** (23): Specific algorithms and procedures
  - 🎯 **future_direction** (79): Research directions and next steps
  - ✨ **innovation** (39): Novel contributions and breakthroughs
  - ⚠️ **limitation** (36): Constraints and boundaries
  - 📚 **assumption** (48): Underlying assumptions
  - 🏢 **institution** (24): Universities and organizations
  - 💼 **application** (21): Real-world use cases
  - 📄 **paper** (12): Academic documents
  - 📝 **personal_note** (7): Personal notes and logs
  - And more...
- **Configuration Visualization Features**:
  - 🎨 **28 distinct colors** for different node types
  - 📊 **7 layout groups** for organized visualization  
  - 🔗 **11 relationship types** with different edge styles
  - 🎛️ **Fully configurable** via blueprints/core/visualization.yaml
- **Rich Relationships**: discusses, proves, uses_method, innovates, accomplished, etc.
- **Dynamic Categorization**: Mathematical concepts automatically categorized as math_foundation
- **No Hardcoded Mappings**: All visualization rules defined in YAML blueprints

## Interactive Agent

An intelligent conversational agent that answers questions about research and professional journey using LangChain.

### Setup
```bash
# Ensure API keys are in .env:
# OPENROUTER_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here

# Run the agent
python interactive_agent.py
```

### Features
- Multi-tool architecture with specialized query tools
- Memory management for conversation history
- Semantic search using embeddings
- Knowledge graph integration for deeper insights
- Real-time streaming responses

### Available Tools
1. **search_academic_papers**: Find papers by topic or keywords
2. **search_chronicle_notes**: Search daily work notes
3. **find_research_topics**: Discover research areas
4. **get_research_evolution**: Track topic evolution over time
5. **find_project_connections**: Explore project relationships
6. **semantic_search**: Natural language search
7. **get_collaborations**: Find collaboration patterns

### Example Questions
- "What papers has Vaios written about optimal transport?"
- "Show me his recent work on machine learning"
- "How has his research evolved from mathematics to AI?"
- "What projects involve reinforcement learning?"
- "Find papers related to GANs or neural networks"
- "What did he work on in June 2025?"

## Profile Directory

The `Profile/` directory contains generated academic profile documents:

- **Profile.md**: Comprehensive academic profile including:
  - Executive summary of research expertise
  - Core competencies in theoretical and applied areas
  - Methodological toolkit and computational approaches
  - Key publications and contributions
  - Research impact and future directions

- **cv.md**: Traditional CV format with:
  - Educational background
  - Research experience
  - Publications list
  - Teaching and supervision
  - Skills and expertise

These documents are automatically generated from the database and can be exported for various uses.

## Development Notes (Configuration-Driven Era)

### Configuration & Environment
- Use `uv` for package management
- Store API keys in `.env` file (OPENROUTER_API_KEY and OPENAI_API_KEY required)
- Run all scripts from project root directory
- Monitor OpenRouter usage and costs for LLM extraction

### Configuration System
- **All domain logic in YAML**: blueprints/ directory contains ALL extraction/mapping rules
- **Zero hardcoded schemas**: Database schema generated from blueprints/core/database_schema.yaml
- **Rich type preservation**: Mathematical concepts keep original categories through configuration mappings
- **Validation required**: Always run `--validate-blueprints` before production builds
- **Incremental development**: Add new document types by creating configuration YAML files
- **Version control**: All configuration changes tracked in git for reproducibility

### Database & Processing
- **Configuration-driven builds only**: Use `DB/build_database.py` for all database operations
- **Rich entity categorization**: 24+ node types automatically generated from blueprints
- **Content hashing**: Sync system detects changes efficiently
- **LLM extraction**: Automatic configuration-driven extraction for chronicle files
- **Entity deduplication**: Integrated into all build processes (20 parallel workers)
- **Embedding model**: Using text-embedding-3-large (3072 dimensions) for quality

### Knowledge Graph
- **Complete configuration control**: All visualization rules in blueprints/core/visualization.yaml
- **Rich node types**: math_foundation, research_insight, personal_achievement, etc.
- **Configurable colors**: 28 distinct colors for different entity types
- **No hardcoded mappings**: Everything defined declaratively in blueprints
- **Graph table pre-computation**: Fast visualization with configuration-driven generation

### Best Practices
- **Test with small batches**: Validate configuration changes before full processing
- **Blueprint validation**: Always validate YAML syntax and logic before builds
- **Domain separation**: Keep ALL domain knowledge in blueprints/, NEVER in Python code
- **Graceful error handling**: Malformed documents are skipped with proper logging
- **Modular design**: Each component reads its configuration independently from blueprints

## Architecture Insights

### Why Configuration-First Design?

The system evolved to configuration-centric for several reasons:

1. **Domain Flexibility**: Works with any research field without code changes
2. **Non-programmer Friendly**: Researchers can modify extraction rules via YAML
3. **Reproducible Research**: Exact configurations ensure consistent results
4. **Version Control**: All domain knowledge tracked in git
5. **Collaborative Science**: Teams can share domain-specific configurations

### The Power of Rich Entity Types

Instead of generic "topics", we now have 24+ specialized categories:
- **Fast Categorization**: Automatic classification based on content
- **Precise Visualization**: Each type has distinct colors and behaviors
- **Domain Expertise**: Mathematical concepts, research insights, personal achievements
- **Easy Extensions**: Add new types by editing YAML files

## 🎯 Configuration System: The Future of Knowledge Extraction

### What Makes This Revolutionary:

1. **Complete Domain Agnosticism**: The entire codebase works for ANY research domain without modification
2. **Rich Type Preservation**: From generic "topics" to 24+ specialized entity types
3. **Zero-Code Extension**: Add new document types by creating YAML files
4. **Declarative Configuration**: All logic expressed in readable YAML blueprints
5. **Validation at Every Level**: Schema validation prevents configuration errors
6. **Version-Controlled Domain Knowledge**: All extraction rules tracked in git

**🔮 Implications for the Future:**

- **Research Domains**: Easily adapt to clinical, legal, engineering, or any other field
- **Collaborative Science**: Non-programmers can modify extraction rules
- **Reproducible Research**: Exact blueprint configurations ensure consistent results
- **Community Extensions**: Researchers can share domain-specific blueprints
- **Enterprise Deployment**: Organizations can customize without touching code

**📊 Quantified Success:**
- **1,135 rich nodes** vs 965 generic nodes (18% increase in granularity)
- **24+ entity types** vs 6 generic types (400% increase in categorization)
- **28 visualization colors** vs basic color scheme
- **100% configurable** system vs hardcoded logic
- **Zero code changes** needed for new domains

This configuration-driven architecture transforms the Interactive CV from a clever academic tool into a **universal knowledge extraction platform** that can adapt to any domain while maintaining the sophistication and intelligence that makes it powerful.

The system now embodies the principle: **"Configuration over Code, Blueprints over Business Logic"** - making it both more powerful and more accessible than ever before.

---

*This Interactive CV system transforms a static professional profile into a living, intelligent, and **infinitely extensible** representation of knowledge and expertise.*