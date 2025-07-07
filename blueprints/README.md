# Blueprints System

The blueprints system provides a unified, YAML-driven configuration framework for document processing, entity extraction, and database mapping. It enables domain-agnostic knowledge extraction from any document type.

## 🏗️ Architecture

```
blueprints/
├── academic/                   # Academic paper configurations
│   ├── extraction_schema.yaml     # Field definitions for academic papers
│   └── database_mapping.yaml      # Entity mappings for academic content
├── personal/                   # Personal notes configurations
│   ├── extraction_schema.yaml     # Field definitions for personal notes
│   └── database_mapping.yaml      # Entity mappings for personal content
└── core/                       # Domain-agnostic configurations
    ├── blueprint_loader.py         # Blueprint loading system
    ├── database_schema.yaml        # Core database structure
    └── visualization.yaml          # Graph visualization settings
```

## 📋 Blueprint Components

### 1. Extraction Schema (`extraction_schema.yaml`)

Defines structured field definitions for metadata extraction:

- **Field Types**: `string`, `list_of_strings`, `list_of_objects`, `object`
- **Field Sections**: Organized into logical groups (core, technical, analysis, etc.)
- **Validation**: Required fields, default values, enumeration constraints
- **Schema Definitions**: Nested object structures for complex data

### 2. Database Mapping (`database_mapping.yaml`)

Maps extracted metadata to database entities:

- **Entity Mappings**: Field → Database table relationships
- **Entity Types**: 24+ rich entity categories (topics, people, methods, institutions)
- **Relationship Types**: Defines how entities connect in the knowledge graph
- **Category Handling**: Automatic categorization and role assignment
- **Confidence Scores**: Relationship strength indicators

### 3. Core Configuration

#### Database Schema (`database_schema.yaml`)
- Table definitions and relationships
- Entity type hierarchies
- Indexing strategies

#### Visualization (`visualization.yaml`)
- Node type mappings and colors
- Edge styles and relationships
- Graph layout configuration
- Legend and grouping rules

## 🛠️ Blueprint Loader System

The `BlueprintLoader` class provides a unified interface for accessing all configurations:

### Key Features

- **Caching**: Efficient YAML loading with in-memory caching
- **Validation**: Comprehensive blueprint validation
- **Dynamic Models**: Pydantic model generation from schemas
- **Path Resolution**: Automatic project root detection
- **Error Handling**: Detailed error reporting and debugging

### Usage

```python
from blueprints.core.blueprint_loader import BlueprintLoader

# Initialize loader
loader = BlueprintLoader()

# Load extraction schema
schema = loader.get_extraction_schema('academic')

# Load database mappings
mappings = loader.get_database_mapping('academic')

# Get visualization config
viz_config = loader.get_visualization_config()

# Validate all blueprints
errors = loader.validate_blueprints()
```

## 🎯 Document Types

### Academic Papers
- **Focus**: Research papers, publications, academic content
- **Entities**: Authors, institutions, methodologies, topics, applications
- **Relationships**: Citations, collaborations, research domains
- **Fields**: 50+ structured fields across 12 categories

### Personal Notes
- **Focus**: Personal reflections, learning notes, insights
- **Entities**: People, activities, challenges, metrics
- **Relationships**: Personal connections, skill development
- **Fields**: Streamlined field set for personal content

## 🔧 Configuration Management

### Adding New Document Types

1. Create document type directory: `blueprints/new_type/`
2. Add `extraction_schema.yaml` with field definitions
3. Add `database_mapping.yaml` with entity mappings
4. Validate configuration: `python blueprint_loader.py`

### Field Definition Structure

```yaml
field_name:
  type: string|list_of_strings|list_of_objects|object
  description: "Field description"
  required: true|false
  default: default_value
  enum: [option1, option2]  # For enumerated fields
  schema:                   # For object/list_of_objects
    nested_field:
      type: string
      description: "Nested field description"
```

### Entity Mapping Structure

```yaml
entity_mappings:
  field_name:
    target_table: entities|relationships
    entity_type: topic|person|method|institution
    relationship_type: mentions|authored_by|uses_method
    category_handling: override|field|default
    category_override: specific_category
    confidence: 0.0-1.0
```

## 🎨 Visualization Configuration

### Node Types and Colors
- **Topics**: Blue variations (#1f77b4, #aec7e8)
- **People**: Orange variations (#ff7f0e, #ffbb78)
- **Methods**: Green variations (#2ca02c, #98df8a)
- **Institutions**: Red variations (#d62728, #ff9896)
- **Applications**: Purple variations (#9467bd, #c5b0d5)

### Node Sizes
- **Major entities**: 20-25px
- **Standard entities**: 15-20px
- **Minor entities**: 10-15px

## 🚀 Integration Points

### Database Building
```bash
# Build database using blueprints
python DB/build_database.py

# Extract metadata with blueprints
python agents/extractor.py academic --input academic/ --output raw_data/academic/
```

### Agent System
- **Semantic Search**: Leverages entity type information
- **Relationship Navigation**: Uses blueprint-defined relationships
- **Dynamic Querying**: Adapts to blueprint-defined entity categories

### Knowledge Graph
- **Node Styling**: Visualization.yaml defines appearance
- **Edge Relationships**: Database mappings define connections
- **Interactive Filtering**: Blueprint categories enable filtering

## 🔍 Validation and Testing

### Blueprint Validation
```python
# Validate all blueprints
loader = BlueprintLoader()
errors = loader.validate_blueprints()

if errors:
    for blueprint, error_list in errors.items():
        print(f"{blueprint}: {error_list}")
```

### Common Validation Issues
- Missing required files (`extraction_schema.yaml`, `database_mapping.yaml`)
- Invalid YAML syntax
- Missing field definitions
- Incorrect entity type references
- Invalid relationship mappings

## 📈 Performance Considerations

### Caching Strategy
- YAML files cached in memory after first load
- Blueprint loader singleton pattern
- Efficient path resolution

### Scalability
- Supports unlimited document types
- Handles complex nested schemas
- Efficient database mapping generation

## 🎯 Best Practices

1. **Schema Design**: Use clear, descriptive field names
2. **Entity Types**: Follow existing type conventions
3. **Relationships**: Define meaningful connection types
4. **Validation**: Always validate before deployment
5. **Documentation**: Include comprehensive field descriptions
6. **Testing**: Test with representative documents

## 🔧 Troubleshooting

### Common Issues

**Blueprint not found**: Check file paths and naming
**YAML parsing errors**: Validate YAML syntax
**Missing entity types**: Ensure types exist in visualization.yaml
**Relationship errors**: Verify relationship type definitions

### Debug Commands
```bash
# Test blueprint loader
python blueprints/core/blueprint_loader.py

# Validate specific document type
python -c "from blueprints.core.blueprint_loader import BlueprintLoader; loader = BlueprintLoader(); print(loader.get_extraction_schema('academic'))"
```

## 📚 Related Documentation

- **Database Schema**: `DB/README.md`
- **Agent System**: `interactive_agent.py`
- **Knowledge Graph**: `KG/README.md`
- **Visualization**: `serve_ui.py`

The blueprints system is the foundation for universal knowledge extraction, enabling the Interactive CV to work with any document type while maintaining consistent entity relationships and visualization standards.