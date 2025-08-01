# Interactive CV System

> ⚠️ **WARNING: UNDER ACTIVE DEVELOPMENT** ⚠️  
> This project is experimental and rapidly evolving. Do not install unless you are a glutton for punishment and enjoy debugging complex AI systems. Expect breaking changes, incomplete documentation, and the occasional digital meltdown. You have been warned! 🔥
## Why This Project Exists: The Problem

Traditional CVs are static documents that fail to capture the dynamic interconnections of modern research and professional work. Academic profiles scatter across multiple platforms, personal insights get buried in notes, and the rich relationships between ideas, people, and projects remain invisible.

**The Vision**: Transform scattered professional knowledge into an intelligent, queryable system that understands the deep connections between your work, research, and ideas.

## What This Actually Does

**Interactive CV** is a blueprint-driven knowledge platform that:

1. **Ingests** your academic papers and personal notes
2. **Extracts** structured knowledge using AI agents and configurable YAML blueprints
3. **Builds** a rich knowledge graph with semantic search capabilities
4. **Provides** an intelligent conversational agent that can answer complex questions about your work

**Example queries it can handle:**
- "What's the connection between Research Area X and Research Area Y?"
- "Which researchers have collaborated on Project Z?"
- "How do personal notes relate to published research themes?"
- "What institutions are associated with Topic W?"

## How Blueprints Make It Universal

The key innovation is **configuration over code**. Instead of hardcoding extraction rules for specific domains, the system uses YAML blueprints that define:

- **What to extract** from documents (fields, entities, relationships)
- **How to structure** the knowledge (database schema, entity types)
- **How to visualize** connections (node colors, graph layouts)

This means the same codebase can work for:
- **Academic researchers** (papers, citations, collaborations)
- **Software engineers** (projects, technologies, contributions)  
- **Business professionals** (initiatives, partnerships, outcomes)
- **Creative professionals** (works, influences, techniques)

Just swap out the blueprints, and the entire system adapts to your domain.

## 🏗️ System Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  YAML Blueprints│────▶│ Extraction Agents│────▶│   Database &    │
│  Domain Rules   │     │  Extract Metadata│     │ Knowledge Graph │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
        ┌──────────────────────────────────────────────────────────┐
        │              Interactive CV Agent                        │
        │ ┌──────────────────┐    ┌──────────────────┐            │
        │ │  6 Unified Tools │    │  Pep Talk Coach  │            │
        │ │  • Semantic      │◄──▶│  Quality Control │            │
        │ │  • Navigation    │    │  Tool Enforcement│            │
        │ │  • Details       │    │  Motivational    │            │
        │ │  • Papers        │    │  Coaching        │            │
        │ │  • Manuscript    │    └──────────────────┘            │
        │ │  • Sequential    │                                    │
        │ │    Reasoning     │                                    │
        │ └──────────────────┘                                    │
        └──────────────────────────────────────────────────────────┘
```

## 🎯 How It Works

### 1. **Blueprint-Driven Design** 📐

The system uses **YAML configuration files** to define domain knowledge and extraction rules:

```
blueprints/
├── academic/              # Academic paper configurations
│   ├── extraction_schema.yaml     # 28 extraction fields
│   └── database_mapping.yaml      # 15 entity mappings
├── personal/              # Personal notes configurations  
│   ├── extraction_schema.yaml     # 20 extraction fields
│   └── database_mapping.yaml      # 12 entity mappings
└── core/                  # Domain-agnostic configurations
    ├── database_schema.yaml       # Complete database structure
    ├── visualization.yaml         # Node types, colors, layouts
    └── blueprint_loader.py        # Configuration parser
```

**Key Benefits:**
- **Configuration over code** - Add new domains by editing YAML files
- **Domain flexibility** - Same codebase works for any research field
- **Collaborative development** - Non-programmers can modify extraction rules
- **LLM-compatible** - AI can help generate domain-specific blueprints

### 2. **AI Extraction Agents** 🤖

Specialized agents extract structured metadata from documents using blueprint configurations:

#### **Generic Extractor Agent** (`agents/extractor.py`)
- Processes any document type based on blueprint schemas
- Uses LLM analysis to extract 20-28 fields per document
- Outputs structured JSON metadata for database population

#### **Manuscript Analysis Agent** (`agents/manuscript_agent.py`)
- Deep document analysis with specialized tools
- Full content access for detailed queries
- Multi-tool agent with search, read, and analysis capabilities

#### **Entity Deduplicator Agent** (`agents/entity_deduplicator.py`)
- LLM-powered entity deduplication with 20 parallel workers
- Identifies and merges duplicate concepts across documents
- Maintains entity relationships and preserves data integrity

**Usage:**
```bash
# Extract academic papers using academic blueprints
python agents/extractor.py academic --input academic/ --output raw_data/academic/extracted_metadata/

# Extract personal notes using personal blueprints
python agents/extractor.py personal --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/
```

### 3. **Database & Knowledge Graph Generation** 🗄️

Blueprint-driven database construction creates a rich knowledge representation:

```bash
# Build complete database from blueprints
python DB/build_database.py

# The build process automatically:
# - Validates all blueprint configurations
# - Creates database schema from blueprints/core/database_schema.yaml
# - Imports metadata with rich type preservation (24+ node types)
# - Creates semantic chunks with entity mappings
# - Generates high-quality embeddings (text-embedding-3-large)
# - Deduplicates entities with LLM verification
# - Builds knowledge graph with visualization support
```

### 4. **The Interactive CV Agent** 🎯

The main conversational agent that provides intelligent access to your professional knowledge.

#### **Core Architecture**

The agent uses **LangGraph** for sophisticated workflow orchestration with two main components:

1. **Main Agent**: Uses 6 unified tools with semantic intelligence
2. **Pep Talk Coach v2**: Smart quality assurance that only intervenes for non-informative responses

#### **The 6 Unified Tools** 🛠️

**1. `semantic_search`** - Embedding-powered search across ALL entity types
- Uses OpenAI text-embedding-3-large (3072 dimensions)
- Finds relevant entities regardless of exact term matching
- Handles synonyms and related concepts automatically
- Returns mixed results (documents, topics, people, methods, etc.)

**2. `navigate_relationships`** - Knowledge graph traversal
- Forward mode: Follow relationships (e.g., paper → topics it discusses)
- Reverse mode: Find sources (e.g., topic → papers that discuss it) 
- Relationship filtering by type or comprehensive exploration
- Essential for multi-hop queries and connection discovery

**3. `get_entity_details`** - Full entity information retrieval
- Works with any entity type (papers, people, topics, methods, etc.)
- Returns complete attributes, metadata, and relationships
- Provides rich context for detailed analysis

**4. `list_available_papers`** - Paper catalog access
- Shows complete list of papers in the system
- Useful for understanding available research scope
- Helps users know what papers exist for deeper queries

**5. `consult_manuscript`** - Deep document analysis (META TOOL)
- **Manuscript Agent integration** for original document access
- Specialized multi-tool agent with file reading capabilities
- Used when database search isn't detailed enough
- Provides access to full paper content and specific passages

**6. `sequential_reasoning`** - Structured analysis (META TOOL)
- **Real MCP (Model Context Protocol) integration**
- Step-by-step reasoning for complex cross-domain questions
- JSON-RPC communication with dedicated MCP server subprocess
- Handles multi-domain connections and theoretical-practical bridges
- **Implementation**: Spawns a subprocess running `sequential_thinking_server.py` that:
  - Accepts structured reasoning requests via JSON-RPC
  - Performs systematic step-by-step analysis using LLM
  - Returns structured insights with evidence chains
  - Particularly effective for "connection between X and Y" questions

#### **The Pep Talk Coach: Quality Assurance** 🎯

**Problem**: Cheaper models (like Gemini Flash) tend to be lazy - they say "I'll search for..." instead of actually searching, or give up with "I cannot find..." responses.

**Solution**: The Pep Talk Coach intercepts these lazy responses and forces the agent to actually use its tools. It detects bad patterns and provides motivational coaching until the agent delivers real results.

**Impact**: Makes Gemini Flash perform at 90% of Claude's quality at 1/10th the cost.


## 🚀 Quick Start for Mathematicians

*Note: More document types and blueprints for other disciplines coming soon!*

### 1. Environment Setup
```bash
# Install dependencies (recommended: use uv for faster installation)
pip install -r requirements.txt
# or with uv:
uv pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env and add your keys:
# OPENROUTER_API_KEY=your_key_here  # Required for LLM agents
# OPENAI_API_KEY=your_key_here      # Required for embeddings
```

### 2. Add Your Research Papers
```bash
# Create directories if they don't exist
mkdir -p academic/
mkdir -p personal_notes/

# Add your papers to the academic folder
# Supported formats: PDF, Markdown (.md), LaTeX (.tex)
cp your_paper.pdf academic/
cp your_paper.md academic/
```

### 3. Process Your Papers
```bash
# Step 1: Analyze papers to extract deep insights
python agents/academic_analyzer.py --input academic/ --output raw_data/academic/generated_analyses/

# Step 2: Extract structured metadata from analyses
python agents/extractor.py academic \
  --input raw_data/academic/generated_analyses/ \
  --output raw_data/academic/extracted_metadata/

# Step 3: (Optional) Add personal research notes
# Place any .md files with personal insights in personal_notes/
# Then extract their metadata:
python agents/extractor.py personal \
  --input personal_notes/ \
  --output raw_data/personal_notes/extracted_metadata/
```

### 4. Build Your Knowledge Base
```bash
# Build the complete database from extracted metadata
python DB/build_database.py

# This automatically:
# - Imports all extracted metadata
# - Creates semantic embeddings for search
# - Builds a knowledge graph of your research
# - Deduplicates entities (people, topics, methods)
# - Generates interactive visualizations
```

### 5. Interact with Your Research
```bash
# Run the interactive agent
python interactive_agent.py

# Example questions you can ask:
# > "What are the main research areas covered in these papers?"
# > "How does Paper A's methodology relate to Paper B?"
# > "Which researchers collaborated on Topic X?"
# > "What computational methods are discussed in the corpus?"
```

### 6. Explore Visually (Optional)
```bash
# Launch the web interface
./start_ui.sh

# Visit http://localhost:5000 to:
# - See an interactive graph of your research
# - Chat with your papers through the web UI
# - Explore connections between topics and collaborators
```

## 🎛️ System Configuration

### **Model Selection**
```bash
export AGENT_MODEL=claude    # Best instruction following, highest quality
export AGENT_MODEL=flash     # Excellent with Pep Talk Coach, best value (default)
export AGENT_MODEL=pro       # Most sophisticated analysis
```

**Recommendation**: Use `claude` for critical analysis, `flash` for daily use with excellent results.

### **Blueprint Customization**
Edit YAML files in `blueprints/` to modify:
- **Extraction schemas** (`extraction_schema.yaml`) - What fields to extract
- **Database mappings** (`database_mapping.yaml`) - How fields map to entities
- **Visualization rules** (`core/visualization.yaml`) - Node types, colors, layouts
- **Database schema** (`core/database_schema.yaml`) - Table structure, indexes

### **Adding New Research Domains**
1. Create `blueprints/new_domain/extraction_schema.yaml`
2. Create `blueprints/new_domain/database_mapping.yaml` 
3. Update `blueprints/core/visualization.yaml` with new node types
4. Run `python DB/build_database.py --validate-blueprints`
5. System automatically validates and builds new domain support


## 🔧 Advanced Usage

### **Database Management**
```bash
# Incremental updates (only new documents)
python DB/update_database.py

# View database contents
./view_database.sh

# Comprehensive analysis
python DB/utils/query_comprehensive.py
```

### **Knowledge Graph Generation & Visualization**

#### Generate Full Knowledge Graph
```bash
# Generate complete knowledge graph with all entities
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json
```

#### Create Focused Web UI Version
```bash
# Prune the graph for cleaner web visualization
python KG/prune_knowledge_graph.py KG/knowledge_graph.json web_ui/knowledge_graph.json \
  --exclude-entities person personal_achievement personal_learning personal_note \
    challenge future_direction assumption limitation general_concept general_topic \
    theoretical_method analytical_method algorithmic_method computational_method \
    general_method tool project math_foundation \
  --exclude-relationships accomplished learned plans faced_challenge mentions \
    relates_to suggests_future_work makes_assumption has_limitation discovered \
    discovers affiliated_with authored_by proves \
  --remove-isolated
```

#### Launch Interactive Visualization
```bash
# Start the web UI
./start_ui.sh

# With database viewer
./start_ui.sh --with-datasette
```

### **Chronicle Sync (Personal Notes from Obsidian)**

Chronicle is a custom synchronization system that pulls personal notes from Obsidian:

```bash
chronicle              # Regular sync with metadata extraction
chronicle-dry          # Preview changes
chronicle-force        # Force re-extraction
chronicle-status       # Check sync configuration
```

**Setup** (Optional - only if you use Obsidian for personal notes):
1. Configure your Obsidian vault path in `.sync/chronicle_sync.py`
2. The sync script will:
   - Pull notes from your Obsidian Chronicles folder
   - Copy them to `personal_notes/` directory
   - Extract metadata using the personal blueprint configuration
   - Update the database with new personal insights

**Note**: This feature is optional. You can manually add markdown files to `personal_notes/` instead.

## 📁 Project Structure

```
interactive_cv/
├── blueprints/                    # YAML configuration system
│   ├── academic/                 # Academic paper blueprints
│   ├── personal/                 # Personal notes blueprints
│   └── core/                     # Domain-agnostic blueprints
├── agents/                       # AI extraction and analysis agents
│   ├── extractor.py             # Generic blueprint-driven extractor
│   ├── manuscript_agent.py       # Deep document analysis agent
│   └── entity_deduplicator.py    # LLM-powered deduplication
├── mcp_subfolder/                # Model Context Protocol for structured reasoning
│   ├── client/mcp_client.py     # JSON-RPC client for agent communication
│   └── server/sequential_thinking_server.py  # Subprocess server for step-by-step analysis
├── DB/                           # Database management system
│   ├── build_database.py        # Complete blueprint-driven builder
│   ├── update_database.py       # Incremental updates
│   └── utils/                    # Database utilities and analysis
├── KG/                           # Knowledge graph generation
│   └── graph_builder.py         # Rich visualization graph builder
├── RAG/                          # Semantic search system
│   └── semantic_search.py       # Embedding-based search engine
├── Profile/                      # Centralized profile system
│   └── profile_loader.py        # Profile management
├── interactive_agent.py          # Main conversational agent
├── serve_ui.py                   # Web interface server
└── web_ui/                       # Visualization interface
    └── index.html                # Interactive graph visualization
```

## 🤝 Contributing

The blueprint-driven architecture makes contributions easy:

1. **Add new document types** by creating YAML blueprint files
2. **Modify extraction schemas** without touching Python code  
3. **Customize visualizations** by editing `visualization.yaml`
4. **Extend database schema** via `database_schema.yaml`
5. **Train agents on new domains** using blueprint configurations

## 🔮 Future Possibilities

### Domain Expansion
- **Blueprint library** for different professions (engineering, medicine, law, arts)
- **Industry-specific templates** with pre-configured extraction schemas
- **Cross-domain blueprint mixing** for interdisciplinary professionals

### Application Ideas
- **"Chat with Your Documents" app** - Use the same semantic search and agent system for any document collection
- **Team knowledge bases** - Multiple people contributing to shared knowledge graphs
- **Research collaboration networks** - Connect researchers with similar interests across institutions
- **Personal learning assistants** - Track learning progress and suggest connections

### Technical Enhancements  
- **Citation network analysis** with academic graph exploration
- **Automated content discovery** from academic databases and repositories
- **Multi-modal support** for images, presentations, and videos
- **Real-time synchronization** with external platforms (ORCID, Google Scholar, LinkedIn)

---

## Key Innovation: Blueprint + Agent + MCP Architecture

This system represents a **novel approach** to knowledge management:

1. **Configuration-Driven**: Domain knowledge lives in YAML files, not code
2. **Agent Orchestration**: Specialized AI agents handle different aspects  
3. **MCP Integration**: Real Model Context Protocol for structured reasoning
4. **Quality Assurance**: Smart Pep Talk Coach v2 ensures quality without blocking good answers
5. **Semantic Intelligence**: Embedding-first search with graph navigation
6. **Universal Adaptability**: Works for any research domain via blueprints

**Result**: A powerful, flexible, and intelligent professional knowledge platform that adapts to any domain while maintaining exceptional query performance and response quality.


## 🧪 Testing & Evaluation

The system includes a comprehensive testing framework with questions across multiple difficulty levels and categories.

### **Quick Testing**

```bash
# Quick evaluation (3 random questions)
python test_agent_comprehensive.py --quick

# Full evaluation (all questions)
python test_agent_comprehensive.py --all --baseline

# Test specific categories
python test_agent_comprehensive.py --category cross_domain
python test_agent_comprehensive.py --category single_paper
```

### **Model Performance**

**Best to Good Performance:**
- **Claude + Pep Talk Coach**: Highest quality, best instruction following
- **Flash + Pep Talk Coach**: Excellent value, cost-effective with great results  
- **Pro + Pep Talk Coach**: Sophisticated analysis capabilities
- **Without Pep Talk Coach**: Inconsistent, prone to lazy responses

```bash
# Test with different models
python test_agent_comprehensive.py --all --claude --baseline
python test_agent_comprehensive.py --all --flash --baseline
python test_agent_comprehensive.py --all --pro --baseline
```

### **Test Categories & Difficulty**

**Categories:**
- **single_paper**: Individual paper analysis
- **personal_notes**: Personal insights and learning
- **cross_paper**: Multi-paper connections
- **cross_domain**: Complex interdisciplinary questions

**Difficulty Levels:**
- **easy**: Basic factual questions
- **medium**: Semantic search and relationships
- **hard**: Multi-hop reasoning and navigation
- **very_hard**: Complex cross-domain analysis

### **Interactive Testing**

```bash
# Test the agent directly
AGENT_MODEL=claude python interactive_agent.py

# Example queries
> What's the connection between Topic A and Topic B in the research?
> Which institutions has Person X collaborated with on Subject Y?
> What methods were used in Paper Z?
> How does Theory M relate to Application N?
```
