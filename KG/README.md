# Knowledge Graph (KG) System

This directory contains the configuration-driven knowledge graph generation system for the Interactive CV project.

## Overview

The KG system transforms research data from the SQLite database into interactive, explorable knowledge graphs using a revolutionary **configuration-driven architecture** that separates visualization logic from implementation code.

## System Architecture

### Configuration-Driven Design
```
YAML Blueprints → Database Entities → Rich Knowledge Graph → Interactive Visualization
```

**Key Innovation**: Zero hardcoded visualization rules - everything defined in YAML blueprints.

### Core Components

#### 1. **graph_builder.py** - Blueprint-Driven Graph Generator
**Purpose**: Creates interactive knowledge graphs from database entities using configuration-driven architecture.

**Key Features**:
- **Blueprint-driven**: Uses YAML configuration files to determine node types, colors, and relationships
- **Rich entity categorization**: Supports 24+ node types (math_foundation, research_insight, personal_achievement, etc.)
- **Database integration**: Reads from SQLite database tables (academic_documents, chronicle_documents, topics, people, etc.)
- **Configurable visualization**: Colors, sizes, and edge styles defined in blueprints
- **Graph statistics**: Provides detailed statistics about nodes and edges
- **Domain agnostic**: Works with any research domain through configuration

**Core Classes**:
- `GraphBuilder`: Main orchestrator that generates vis.js compatible JSON
- Integrates with blueprint system for configuration-driven behavior

#### 2. **knowledge_graph.json** - Generated Graph Output
**Format**: JSON with nodes and links structure compatible with vis.js

**Structure**:
```json
{
  "nodes": [
    {
      "id": "topic_123",
      "type": "math_foundation", 
      "label": "Optimal Transport",
      "color": "#FF6B6B",
      "size": 25,
      "metadata": {...}
    }
  ],
  "links": [
    {
      "source": "academic_1",
      "target": "topic_123", 
      "type": "discusses",
      "strength": 0.8
    }
  ],
  "metadata": {
    "version": "2.0",
    "total_nodes": 1135,
    "node_types": {...}
  }
}
```

## Rich Entity Types (24+ Categories)

The system supports sophisticated entity categorization through blueprint configurations:

### Mathematical & Research Entities
- **math_foundation** (203 nodes): Core mathematical concepts like "Optimal Transport"
- **research_area** (47): Research domains and fields
- **research_insight** (93): Key insights and discoveries
- **theoretical_method** (25): Proof techniques, analytical approaches
- **computational_method** (2): Numerical and algorithmic techniques
- **analytical_method** (22): Analysis and evaluation methods
- **algorithmic_method** (23): Specific algorithms and procedures

### Personal & Professional Entities
- **personal_achievement** (71): Work accomplishments and progress
- **person** (181): Authors, researchers, collaborators
- **institution** (24): Universities and organizations
- **project** (13): Research and development projects
- **application** (21): Real-world use cases

### Document & Content Entities
- **paper** (12): Academic documents
- **personal_note** (7): Personal notes and logs

### Research Process Entities
- **future_direction** (79): Research directions and next steps
- **innovation** (39): Novel contributions and breakthroughs
- **limitation** (36): Constraints and boundaries
- **assumption** (48): Underlying assumptions

## Configuration System

### Blueprint Integration
The system reads visualization rules from:
- **Path**: `blueprints/core/visualization.yaml`
- **Dependencies**: `blueprint_loader.py` for configuration parsing

### Key Configurations
1. **Node Type Mappings**: How database categories map to visualization types
2. **Color Scheme**: 28 distinct colors for different entity types
3. **Edge Styles**: 11 relationship types with different visual styles
4. **Layout Groups**: 7 organized visualization groupings

### Example Configuration
```yaml
# blueprints/core/visualization.yaml
node_types:
  math_foundation:
    color: "#FF6B6B"
    size: 25
    description: "Core mathematical concepts"
  research_insight:
    color: "#4ECDC4"
    size: 20
    description: "Key research insights"

relationship_types:
  discusses:
    color: "#333333"
    style: "solid"
  proves:
    color: "#FF9999"
    style: "dashed"
```

#### 3. **analyze_knowledge_graph.py** - Graph Analysis Tool

**Purpose**: Analyzes knowledge graphs and extracts detailed information about entities and relationships for comparison and debugging purposes.

**Key Features**:
- **Statistical Analysis**: Provides detailed statistics about node types, relationship types, and connectivity
- **Entity Distribution**: Shows count and percentage of each entity type
- **Relationship Mapping**: Analyzes relationship patterns and connection strengths
- **Comparison Ready**: Outputs formatted data suitable for comparing different graph versions
- **Debugging Support**: Helps identify issues with graph structure and data quality

**Usage**:
```bash
# Analyze a knowledge graph
python KG/analyze_knowledge_graph.py KG/knowledge_graph.json

# Analyze and compare multiple graphs
python KG/analyze_knowledge_graph.py KG/knowledge_graph.json web_ui/knowledge_graph.json
```

#### 4. **prune_knowledge_graph.py** - Graph Pruning Tool

**Purpose**: Creates focused, filtered versions of knowledge graphs by excluding specified entity types and relationship types, with automatic isolated node removal.

**Key Features**:
- **Entity Type Filtering**: Exclude specific entity types (e.g., personal elements, technical details)
- **Relationship Type Filtering**: Remove specific relationship types (e.g., process metadata, weak connections)
- **Isolated Node Removal**: Automatically removes orphaned nodes with no connections
- **Structural Focus**: Transform detailed graphs into cleaner, more focused versions
- **Web UI Optimization**: Create lighter graphs optimized for visualization performance

**Usage**:
```bash
# Basic pruning with entity exclusion
python KG/prune_knowledge_graph.py input.json output.json \
  --exclude-entities person personal_achievement \
  --exclude-relationships authored_by affiliated_with

# Comprehensive pruning with isolated node removal
python KG/prune_knowledge_graph.py KG/knowledge_graph.json web_ui/knowledge_graph.json \
  --exclude-entities person personal_achievement personal_learning math_foundation \
  --exclude-relationships authored_by proves mentions \
  --remove-isolated

# Configuration-style pruning (see config_style_pruning_params.txt for full example)
python KG/prune_knowledge_graph.py KG/knowledge_graph.json web_ui/knowledge_graph.json \
  --exclude-entities person personal_achievement personal_learning personal_note challenge future_direction assumption limitation general_concept general_topic theoretical_method analytical_method algorithmic_method computational_method general_method tool project math_foundation \
  --exclude-relationships accomplished learned plans faced_challenge mentions relates_to suggests_future_work makes_assumption has_limitation discovered discovers affiliated_with authored_by proves \
  --remove-isolated
```

#### 5. **graph_matching_ideas.md** - Advanced Graph Theory Documentation

**Purpose**: Documents mathematical approaches for finding structurally similar subgraphs, particularly for matching academic knowledge graphs to reference structures.

**Content**:
- **Subgraph Isomorphism**: Mathematical foundations for graph matching
- **Similarity Metrics**: Distance measures and scoring functions for graph comparison
- **Algorithm Exploration**: Various approaches to graph matching problems
- **Use Cases**: Applications for knowledge graph similarity and structure analysis

#### 6. **config_style_pruning_params.txt** - Pruning Configuration Documentation

**Purpose**: Documents the exact parameters and rationale for creating web UI-optimized knowledge graphs from full research graphs.

**Content**:
- **Pruning Commands**: Complete command-line examples with all parameters
- **Entity Type Rationale**: Explanation of why specific entity types are excluded/included
- **Relationship Type Logic**: Reasoning behind relationship filtering decisions
- **Performance Results**: Statistics on graph size reduction and optimization outcomes
- **Philosophy**: Structural focus vs. process focus approach to graph design

**Key Achievement**: Transforms 1,081 entities into 119 focused entities (11% retention) while maintaining graph connectivity and core research relationships.

## Usage

### Command Line Interface
```bash
# Generate knowledge graph from database
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json

# Validate blueprint configurations
python KG/graph_builder.py --validate-blueprints

# Custom database path
python KG/graph_builder.py /path/to/custom.db --output custom_graph.json
```

### Integration with Build Process
```bash
# Integrated into database build process (Step 5)
python DB/build_database.py  # Includes knowledge graph generation

# Skip graph generation
python DB/build_database.py --skip-graph
```

### Python API
```python
from KG.graph_builder import GraphBuilder

# Initialize with database path
builder = GraphBuilder("DB/metadata.db")

# Generate graph
graph_data = builder.build_graph()

# Save to file
builder.save_graph(graph_data, "KG/knowledge_graph.json")
```

## Integration Points

### 1. Database Integration
**Source**: Reads from `/DB/metadata.db` SQLite database

**Tables Processed**:
- `academic_documents` → paper nodes
- `chronicle_documents` → personal_note nodes
- `topics`, `people`, `projects`, `institutions`, `methods`, `applications` → entity nodes
- `relationships` → graph edges

### 2. Web UI Integration
**Consumer**: `web_ui/index.html` loads the knowledge graph for interactive visualization

**Technology**: Uses vis.js network visualization library

**Features**:
- Interactive graph exploration
- Node and edge filtering
- Dynamic layout algorithms
- Zoom and pan capabilities
- Node/edge selection and highlighting

### 3. RAG System Integration
**Consumer**: `RAG/graph_enhanced_query.py` uses the knowledge graph for intelligent querying

**Technology**: NetworkX for graph analysis and traversal

**Features**:
- Related topic discovery
- Graph-based query enhancement
- Connection strength analysis
- Semantic relationship exploration

### 4. Build Process Integration
**Called from**: `DB/build_database.py` (Step 5 of database build process)

**Trigger**: Generated after database population and entity processing

**Optional**: Can be skipped with `--skip-graph` flag

## Current Statistics

### Graph Scale
- **Total Nodes**: 1,135 with 24+ distinct types
- **Total Edges**: 1,249 relationships
- **Node Types**: 24+ specialized categories
- **Relationship Types**: 11 distinct relationship types

### Visualization Features
- **🎨 28 distinct colors** for different node types
- **📊 7 layout groups** for organized visualization
- **🔗 11 relationship types** with different edge styles
- **🎛️ Fully configurable** via blueprints/core/visualization.yaml

### Rich Entity Distribution
- **Math Foundation**: 203 nodes (core mathematical concepts)
- **People**: 181 nodes (authors, researchers, collaborators)
- **Research Insights**: 93 nodes (key insights and discoveries)
- **Personal Achievements**: 71 nodes (work accomplishments)
- **Future Directions**: 79 nodes (research directions)
- **Research Areas**: 47 nodes (domains and fields)
- **And more...**

## Dependencies

### Python Dependencies
- `sqlite3` - Database connectivity
- `json` - JSON handling
- `pathlib` - Path manipulation
- `logging` - Logging functionality
- Blueprint system (`blueprint_loader`)

### External Dependencies
- Blueprint configuration files in `blueprints/core/`
- SQLite database with proper schema
- NetworkX (for RAG integration)
- vis.js (for web visualization)

## Configuration Files

### Required Blueprints
- **`blueprints/core/visualization.yaml`**: Node types, colors, and relationship styles
- **`blueprints/core/database_schema.yaml`**: Database schema definitions

### Database Schema Requirements
The system expects specific database tables:
- Document tables: `academic_documents`, `chronicle_documents`
- Entity tables: `topics`, `people`, `projects`, `institutions`, `methods`, `applications`
- Relationship table: `relationships`
- Graph tables: `graph_nodes`, `graph_edges` (optional, for pre-computed graphs)

## Error Handling

The system includes comprehensive error handling:
- **Blueprint validation**: Ensures configuration files are valid
- **Database connectivity**: Handles missing or corrupted database files
- **Missing entities**: Gracefully handles missing entity references
- **JSON serialization**: Proper handling of complex data types
- **File I/O**: Robust file reading/writing with error recovery

## Performance Considerations

### Optimization Features
- **Pre-computed relationships**: Database stores graph structure for fast access
- **Efficient querying**: SQL queries optimized for graph generation
- **Memory management**: Processes large graphs without memory issues
- **JSON optimization**: Efficient serialization for web consumption

### Scalability
- **Large graphs**: Handles 1000+ nodes efficiently
- **Complex relationships**: Supports complex many-to-many relationships
- **Extensible**: New entity types don't impact performance
- **Configurable**: Can adjust node/edge limits via configuration

## Future Enhancements

### Planned Features
1. **Dynamic graph updates**: Real-time graph updates as database changes
2. **Enhanced filtering**: Advanced filtering based on entity metadata
3. **Graph analytics**: Built-in graph analysis metrics
4. **Export formats**: Additional export formats (GraphML, DOT, etc.)
5. **Visualization themes**: Multiple color schemes and layouts

### Configuration Extensions
- **Custom node shapes**: Shape customization via blueprints
- **Animation settings**: Configurable animation behaviors
- **Clustering algorithms**: Different node grouping strategies
- **Edge bundling**: Visual edge bundling for cleaner graphs

## Troubleshooting

### Common Issues

1. **Empty graph generated**
   - **Cause**: Database might be empty or missing required tables
   - **Solution**: Run `python DB/build_database.py` first

2. **Blueprint validation errors**
   - **Cause**: Invalid YAML syntax in configuration files
   - **Solution**: Check YAML syntax and required fields

3. **Missing entity references**
   - **Cause**: Database inconsistencies or missing foreign key relationships
   - **Solution**: Run database verification tools

4. **Performance issues with large graphs**
   - **Cause**: Too many nodes/edges for efficient visualization
   - **Solution**: Use filtering or sampling in configuration

### Debug Commands
```bash
# Validate blueprint configurations
python KG/graph_builder.py --validate-blueprints

# Check database schema
python DB/utils/query_comprehensive.py

# Verify entity relationships
python DB/utils/verify_entities.py
```

## 📚 Related Documentation

- **[Main Project README](../README.md)**: Overall system architecture and quick start guide
- **[Database System](../DB/README.md)**: How entities are stored and processed before visualization
- **[AI Agents](../agents/README.md)**: How documents are analyzed to create the entities
- **[Web UI](../web_ui/README.md)**: How to interact with the generated knowledge graphs

## Architecture Benefits

### Why Configuration-Driven?

1. **Domain Flexibility**: Works with any research field without code changes
2. **Non-programmer Friendly**: Researchers can modify visualization rules via YAML
3. **Reproducible Research**: Exact configurations ensure consistent results
4. **Version Control**: All visualization logic tracked in git
5. **Collaborative Science**: Teams can share domain-specific visualization configurations

### The Power of Rich Entity Types

Instead of generic "topics", we now have 24+ specialized categories:
- **Fast Categorization**: Automatic classification based on content
- **Precise Visualization**: Each type has distinct colors and behaviors
- **Domain Expertise**: Mathematical concepts, research insights, personal achievements
- **Easy Extensions**: Add new types by editing YAML files

---

*The KG system transforms static research data into living, interactive knowledge graphs that reveal the hidden connections and patterns in academic and professional work.*