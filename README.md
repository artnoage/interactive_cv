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
- "What's the connection between my work on optimal transport and machine learning?"
- "Which collaborators have I worked with on reinforcement learning projects?"
- "How do my personal learning goals align with my published research?"
- "What institutions are associated with my stochastic control work?"

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

**Current Database:**
- **19 documents**: 12 academic papers + 7 personal notes
- **1,135 entities**: 745 topics, 181 people, 132 methods, 24 institutions
- **1,249 relationships**: Categorized by type (discusses, proves, uses_method, etc.)
- **Rich categorization**: 24+ entity types instead of generic "topics"

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

#### **The Pep Talk Coach v2: Smart Quality Assurance** 🎯

A **revolutionary quality control system** designed to make cheaper models (like Gemini Flash) perform at Claude-level quality through motivational coaching:

**The Problem:** Cheaper models tend to be lazy with tool usage:
- Say "I'll search for..." instead of actually searching
- Give up easily with "I cannot find..." responses  
- Ignore available tools and provide generic answers
- Poor instruction following compared to premium models

**The Solution:** Pep Talk Coach intercepts and fixes these issues:

**How It Works:**
1. **Intercepts responses** before they reach the user
2. **Detects bad patterns**: "I'll search for...", "I cannot find...", institution IDs
3. **Provides creative coaching** using high-temperature LLM generation
4. **Enforces tool usage** - won't let planning statements through
5. **Asks specific questions** like "Did you take into account the fallback info?"
6. **Loop prevention** - Allows up to 4 coaching attempts before giving up

**Patterns It Catches:**
- **Procrastination**: "I'll search for...", "Let me find...", "I need to..."
- **Negativity**: "I cannot find...", "Unable to retrieve...", "Entity not found..."
- **Technical errors**: Institution IDs instead of real names
- **Complex questions**: Suggests using `sequential_reasoning` for cross-domain analysis

**Results:**
- **Gemini Flash + Pep Talk Coach**: Cost-effective with excellent Q&A performance
- **Claude Models**: Exceptional tool usage and instruction following - best results
- **Without Coach**: Even premium models can be lazy and provide incomplete answers

**Performance Hierarchy:**
1. **Claude + Pep Talk Coach**: Highest quality, best for complex analysis
2. **Gemini Flash + Pep Talk Coach**: Excellent value, 90% of Claude quality at 1/10th cost  
3. **Any model without Coach**: Inconsistent, prone to lazy responses

The Pep Talk Coach democratizes access to high-quality AI interactions regardless of model budget!

#### **Advanced Prompting System**

**Action-First Rules:**
- ❌ FORBIDDEN: "I'll search for...", "Let me look for...", "To answer this, I will..."
- ✅ REQUIRED: Use tools immediately without announcing intentions

**Mandatory Search Protocol:**
1. ALWAYS use `semantic_search` with relevant keywords IMMEDIATELY  
2. Use `get_entity_details` to examine promising results
3. ONLY if searches fail completely, use profile fallback information
4. NEVER give generic answers without searching first

**Sequential Reasoning Triggers:**
- Questions with "connection between", "how does X relate to Y" 
- Cross-domain analysis needs
- Theoretical-practical bridges
- Complex multi-step reasoning requirements

**Fallback Strategy:**
- If database searches return incomplete data (like institution IDs)
- Use comprehensive profile information from `Profile/Profile_Prompt.md`
- NEVER say "I cannot find" - always provide complete answers

## 🚀 Quick Start

### 1. Profile Setup (Required)
```bash
# Edit your profile with personal/professional information
nano Profile/Profile_Prompt.md
```

### 2. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Add your keys:
# OPENROUTER_API_KEY=your_key_here  
# OPENAI_API_KEY=your_key_here
```

### 3. Build Knowledge Base
```bash
# Complete database build using blueprints
python DB/build_database.py

# This automatically:
# - Validates blueprint configurations
# - Extracts metadata from all documents
# - Creates semantic embeddings  
# - Builds knowledge graph
# - Deduplicates entities
```

### 4. Run the Interactive Agent
```bash
# Default model (Gemini Flash)
python interactive_agent.py

# Use Claude for best instruction following (recommended)
AGENT_MODEL=claude python interactive_agent.py


# Use Pro model for sophisticated analysis
AGENT_MODEL=pro python interactive_agent.py
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

## 📊 Current System Status

### **Database Statistics**
- ✅ **19 documents processed**: 12 academic papers + 7 personal notes
- ✅ **1,135 entities**: Rich categorization with 24+ distinct types
- ✅ **1,249 relationships**: Typed connections between entities
- ✅ **Full content loaded**: Academic papers (20-29k chars), Personal notes (1.6-5.4k chars)
- ✅ **High-quality embeddings**: OpenAI text-embedding-3-large, 3072 dimensions

### **Agent Performance**
- ✅ **Best scores ever achieved** with Pep Talk Coach system
- ✅ **Real MCP integration** - Actual JSON-RPC subprocess communication
- ✅ **Action-first responses** - No more "I'll search for..." lazy patterns
- ✅ **Cross-domain analysis** - Handles very hard questions with structured reasoning
- ✅ **Quality assurance** - Automated coaching prevents tool usage issues

### **Knowledge Graph**
- ✅ **Rich node types**: `math_foundation` (203), `person` (181), `research_insight` (93)
- ✅ **Advanced categorization**: Methods by type (theoretical, computational, analytical)
- ✅ **Personal integration**: `personal_achievement`, `personal_learning`, `challenge`
- ✅ **Visualization ready**: 28 distinct colors, grouped layouts

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

### **Knowledge Graph Visualization**
```bash
# Generate rich knowledge graph
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# Launch web UI with chat integration
./start_ui.sh

# With database viewer
./start_ui.sh --with-datasette
```

### **Chronicle Sync (Personal Notes)**
```bash
chronicle              # Regular sync with metadata extraction
chronicle-dry          # Preview changes
chronicle-force        # Force re-extraction
```

**Note**: In my case, I also sync my daily notes with Obsidian. The system automatically pulls from my Obsidian Chronicles folder (`/home/artnoage/OneDrive/Second_Mind/Second Mind/Chronicles`) and processes them alongside academic papers, creating a unified knowledge base that spans both research and personal insights.

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
├── mcp_subfolder/                # MCP Sequential Thinking system
│   ├── client/mcp_client.py     # MCP client implementation
│   └── server/sequential_thinking_server.py  # MCP server
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

### **Knowledge Graph Visualization**
```bash
# Generate rich knowledge graph
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# Launch web UI with chat integration
./start_ui.sh

# With database viewer
./start_ui.sh --with-datasette
```

### **Chronicle Sync (Personal Notes)**
```bash
chronicle              # Regular sync with metadata extraction
chronicle-dry          # Preview changes
chronicle-force        # Force re-extraction
```

## 🧪 Testing & Evaluation

The system includes a comprehensive testing framework with 35 curated questions across multiple difficulty levels and categories.

### **Comprehensive Test Suite**

The merged `test_agent_comprehensive.py` provides extensive evaluation capabilities:

```bash
# Quick evaluation (3 random questions)
python test_agent_comprehensive.py --quick

# Full baseline evaluation (all 35 questions with enhanced reporting)
python test_agent_comprehensive.py --all --baseline --save

# Random subset evaluation
python test_agent_comprehensive.py --random 10

# Category-specific testing
python test_agent_comprehensive.py --category cross_domain
python test_agent_comprehensive.py --category single_paper
python test_agent_comprehensive.py --category personal_notes
python test_agent_comprehensive.py --category cross_paper

# Difficulty-specific testing
python test_agent_comprehensive.py --difficulty hard
python test_agent_comprehensive.py --difficulty very_hard

# Test specific questions by ID
python test_agent_comprehensive.py --questions 1 5 10 15

# Model comparison on same questions
python test_agent_comprehensive.py --compare-models --questions 5
```

### **Model Selection for Testing**

```bash
# Use Claude model (best instruction following, highest quality)
python test_agent_comprehensive.py --all --claude --baseline

# Use Pro model (better performance than Flash)
python test_agent_comprehensive.py --all --pro --baseline

# Use Flash model (fastest, excellent with Pep Talk Coach)
python test_agent_comprehensive.py --all --flash --baseline
```

### **Advanced Testing Options**

```bash
# Baseline evaluation with custom output
python test_agent_comprehensive.py --all --baseline --claude --output-file my_results.json

# Verbose output with detailed analysis
python test_agent_comprehensive.py --random 5 --pro --verbose

# Summary-only output (no individual question details)
python test_agent_comprehensive.py --all --summary-only

# Save results automatically for baseline and full evaluations
python test_agent_comprehensive.py --all --baseline  # Auto-saves
python test_agent_comprehensive.py --random 10 --save  # Manual save
python test_agent_comprehensive.py --quick --no-save  # Force no save
```

### **Test Categories**

- **single_paper**: Questions about individual papers and their content
- **personal_notes**: Questions about personal insights and learning
- **cross_paper**: Questions requiring information from multiple papers
- **cross_domain**: Complex questions bridging multiple research domains

### **Difficulty Levels**

- **easy**: Basic factual questions about papers and people
- **medium**: Questions requiring semantic search and entity relationships
- **hard**: Multi-hop queries requiring graph navigation and reasoning
- **very_hard**: Complex cross-domain analysis requiring sequential reasoning

### **Baseline Evaluation Features**

The `--baseline` flag provides enhanced reporting including:

- **Performance breakdown** by quality categories (excellent, good, satisfactory, poor, incorrect)
- **Category analysis** showing performance across question types
- **Optimization recommendations** based on average scores
- **Best/worst performing questions** for focused improvement
- **Model-specific reports** with timestamps and metadata
- **Comprehensive metrics** including timing and tool usage

### **Example Testing Workflows**

```bash
# Development workflow: Quick test with different models
python test_agent_comprehensive.py --quick --flash
python test_agent_comprehensive.py --quick --claude

# Performance evaluation: Full baseline with Claude
python test_agent_comprehensive.py --all --baseline --claude

# Model comparison: Test same questions across models
python test_agent_comprehensive.py --compare-models --questions 10

# Category analysis: Test specific areas
python test_agent_comprehensive.py --category cross_domain --baseline --pro

# Difficulty progression: Test harder questions with better models
python test_agent_comprehensive.py --difficulty easy --flash
python test_agent_comprehensive.py --difficulty very_hard --claude
```

### **Understanding Test Results**

**Score Ranges:**
- **90-100**: Excellent - Complete, accurate, well-structured answers
- **70-89**: Good - Mostly correct with minor gaps or issues
- **50-69**: Satisfactory - Adequate but missing important details
- **20-49**: Poor - Significant issues or incomplete information
- **0-19**: Incorrect - Wrong or very incomplete answers

**Performance Targets:**
- **Flash + Pep Talk Coach**: ~70-80/100 average (excellent value)
- **Claude + Pep Talk Coach**: ~85-95/100 average (highest quality)
- **Without Pep Talk Coach**: ~50-60/100 average (inconsistent)

### **Manual Interactive Testing**

```bash
# Test interactively with different models
AGENT_MODEL=claude python interactive_agent.py
AGENT_MODEL=flash python interactive_agent.py

# Test with specific queries from test suite
python interactive_agent.py
> What's the connection between optimal transport and my machine learning work?
> Which institutions have I collaborated with on stochastic control research?
```
