# Agents

This directory contains specialized AI agents for the Interactive CV project.

## Agent Types

### Academic Workflow
1. **Academic Analyzer** (`academic_analyzer.py`) - Analyzes raw papers → produces structured analyses
2. **Academic Metadata Extractor** (`academic_metadata_extractor.py`) - Extracts metadata to JSON

### Chronicle Workflow
- **Chronicle Metadata Extractor** (`chronicle_metadata_extractor.py`) - Extracts metadata to JSON

## Academic Analyzer (`academic_analyzer.py`)

Analyzes research papers following the methodology in `How_to_analyze.md`.

**Features:**
- Three-phase analysis structure (Reconnaissance, Deep Dive, Synthesis)
- Domain-specific analysis (mathematics, computer_science, physics)
- Critical examination (assumptions, limitations, evidence quality)
- Generates structured markdown analyses
- Thinking patterns and quality assessment

**Usage:**
```python
from agents import AcademicAnalyzer

# Use the default (flash) model
analyzer_flash = AcademicAnalyzer()
# Or use the pro model
analyzer_pro = AcademicAnalyzer(use_pro_model=True)

# Analyze a paper
analysis = analyzer_flash.analyze_file(Path("paper.md"))

# Save as structured markdown
output_path = analyzer_flash.save_analysis(analysis)
```

**Output:** Creates a comprehensive analysis following the three-phase structure, ready for entity extraction.

## Academic Metadata Extractor (`academic_metadata_extractor.py`)

Extracts entities and relationships from paper analyses (not raw papers) to JSON files.

**Features:**
- Works on analyses produced by the Academic Analyzer
- Phase-aware extraction
- Domain-specific entity extraction
- Critical analysis elements (assumptions, limitations)
- Future work and insights extraction

**Usage:**
```python
from agents import AcademicExtractor

# Use the default (flash) model
extractor_flash = AcademicExtractor()
# Or use the pro model
extractor_pro = AcademicExtractor(use_pro_model=True)

metadata = extractor_flash.process_file(Path("paper_analysis.md"))
```

## Chronicle Metadata Extractor (`chronicle_metadata_extractor.py`)

Extracts metadata from daily, weekly, and monthly notes to JSON files.

**Features:**
- Multi-type support (daily, weekly, monthly)
- Template-aligned extraction
- Automatic note type detection
- Common fields + type-specific fields
- Outputs JSON files for modular workflow

**Usage:**
```python
from agents import ChronicleMetadataExtractor

# Use the default (flash) model
extractor = ChronicleMetadataExtractor()

# Process a file and save to JSON
output_path = extractor.process_file(
    Path("daily_note.md"), 
    Path("output_dir")
)
```

## Workflow Examples

### Academic Paper Processing
```python
# Step 1: Analyze the paper
analyzer_flash = AcademicAnalyzer()
analysis = analyzer_flash.analyze_file(Path("raw_paper.md"))
analysis_path = analyzer_flash.save_analysis(analysis)

# Step 2: Extract entities from the analysis
extractor_flash = AcademicExtractor()
entities = extractor_flash.process_file(analysis_path)

# Example with pro model
analyzer_pro = AcademicAnalyzer(use_pro_model=True)
analysis_pro = analyzer_pro.analyze_file(Path("raw_paper.md"))
extractor_pro = AcademicExtractor(use_pro_model=True)
entities_pro = extractor_pro.process_file(analysis_path)
```

### Chronicle Note Processing
```python
# Direct extraction from notes to JSON
extractor = ChronicleMetadataExtractor()
output_path = extractor.process_file(
    Path("2025-01-15.md"),
    Path("output_metadata")
)

# Batch processing
python scripts/extract_personal_notes_metadata.py
```

## Configuration

All agents require:
- `OPENROUTER_API_KEY` in your `.env` file
- Python packages: langchain, openai, pydantic

## Schema Files

- **Chronicle**: `raw_data/chronicle/extraction_config_simple.yaml`
- **Academic**: `raw_data/academic/extraction_schema.json`

## Integration Points

These agents integrate with:
- Metadata database system
- Knowledge graph generation
- RAG pipeline for queries
- Sync scripts for automation