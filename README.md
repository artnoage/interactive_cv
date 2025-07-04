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
│   ├── populator.py                   # Generic metadata populator
│   ├── chunker.py                     # Document chunking
│   ├── embeddings.py                  # Vector embeddings
│   ├── populate_graph_tables.py       # Graph table population
│   └── query_comprehensive.py         # Database exploration
├── KG/                   # Knowledge Graph system
│   ├── graph_builder.py               # Rich knowledge graph generator
│   └── graph_enhanced_query.py        # Intelligent queries
├── .sync/                # Chronicle sync system
├── interactive_agent.py  # Conversational AI interface
└── web_ui/              # Visualization interface
```

## 🔍 Rich Entity Types & Knowledge Graph

### Knowledge Graph Statistics (Latest)
- **Total Nodes**: 1,135 with 24 distinct types
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

## 📊 Current Status (2025-01-04 - Blueprint Update)

### Database Statistics
- **19 documents**: 12 academic papers + 7 personal notes
- **Entities with Rich Categories**:
  - **745 topics**: Categorized by domain (math_foundation, research_area, etc.)
  - **181 people**: Authors and collaborators
  - **132 methods**: Theoretical, computational, analytical categories
  - **24 institutions**: Universities and organizations
  - **21 applications**: Real-world use cases
  - **13 projects**: Research initiatives
- **1,249 relationships**: Categorized by type (discusses, proves, uses_method, etc.)
- **Document chunks**: Semantic segmentation for RAG

### Processing Pipeline Status
✅ **Blueprint-driven architecture** - Complete domain separation
✅ **Rich entity type preservation** - 24+ node types instead of generic "topics"
✅ **Academic paper analysis and extraction**
✅ **Configurable database population**
✅ **Semantic chunking with entity mapping**
✅ **High-quality embeddings** with text-embedding-3-large
✅ **Integrated entity deduplication**
✅ **Blueprint-driven knowledge graph** with rich visualization
⏳ Interactive web UI completion

## 🛠️ Blueprint System Usage

### 1. Build Database with Blueprints

```bash
# Complete build with validation
python DB/build_database.py --validate-blueprints

# Options:
# --backup              # Backup existing database
# --skip-embeddings     # Skip embedding generation  
# --skip-graph          # Skip knowledge graph generation
# --no-deduplication    # Skip automatic deduplication
# --db custom.db        # Use custom database name
```

### 2. Extract Metadata Using Blueprints

```bash
# Extract academic papers (uses academic blueprints)
python agents/extractor.py academic \
  --input academic/ --output raw_data/academic/extracted_metadata/

# Extract personal notes (uses personal blueprints)
python agents/extractor.py personal \
  --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/
```

### 3. Generate Rich Knowledge Graph

```bash
# Generate graph with rich node types
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# View rich visualization
open web_ui/index.html
```

### 4. Validate Blueprint Configurations

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
- [ ] Web API (REST/GraphQL) for remote queries
- [ ] Interactive web UI completion
- [ ] Real-time RAG pipeline integration
- [ ] Export to various CV formats (PDF, JSON, etc.)

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