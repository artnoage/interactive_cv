# Scripts Directory

This directory previously contained utility scripts for the Interactive CV system. With the implementation of the **configuration-driven architecture**, most functionality has been moved to the main components.

## Migration to Configuration-Driven Architecture

The following scripts have been **replaced by configuration-driven components**:

### ❌ Removed (Obsolete)
- `extract_academic_metadata.py` → Use `agents/extractor.py academic`
- `extract_personal_notes_metadata.py` → Use `agents/extractor.py personal`

### ✅ New Configuration-Driven Alternatives

**Extract Metadata:**
```bash
# Academic papers (uses blueprints/academic/ configurations)
python agents/extractor.py academic \
  --input academic/ --output raw_data/academic/extracted_metadata/

# Personal notes (uses blueprints/personal/ configurations)  
python agents/extractor.py personal \
  --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/
```

**Build Database:**
```bash
# Complete configuration-driven build with rich entity types
python DB/build_database.py --validate-blueprints
```

**Generate Knowledge Graph:**
```bash
# Rich graph with 24+ node types using configuration blueprints
python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json
```

## Configuration System Benefits

The new configuration-driven architecture provides:

1. **Rich Entity Types**: 24+ distinct node types instead of generic categories
2. **Zero Code Changes**: Add new document types via YAML configuration
3. **Domain Agnosticism**: Same code works for any research field
4. **Configuration Validation**: YAML schema validation prevents errors
5. **Complete Flexibility**: All extraction and visualization rules in blueprints

## Legacy Compatibility

The configuration system maintains backward compatibility with existing data and workflows while providing significantly enhanced functionality.

For detailed usage instructions, see the main README.md and CLAUDE.md files.