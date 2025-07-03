# Agents

This directory contains specialized AI agents for the Interactive CV project.

## Agent Types

### Academic Workflow
1. **Academic Analyzer** (`academic_analyzer.py`) - Analyzes raw papers → produces structured analyses
2. **Academic Extractor** (`academic_extractor.py`) - Extracts entities/relationships from analyses

### Chronicle Workflow
- **Chronicle Extractor** (`chronicle_extractor.py`) - Extracts metadata from daily/weekly/monthly notes

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

analyzer = AcademicAnalyzer()

# Analyze a paper
analysis = analyzer.analyze_file(Path("paper.md"))

# Save as structured markdown
output_path = analyzer.save_analysis(analysis)
```

**Output:** Creates a comprehensive analysis following the three-phase structure, ready for entity extraction.

## Academic Extractor (`academic_extractor.py`)

Extracts entities and relationships from paper analyses (not raw papers).

**Features:**
- Works on analyses produced by the Academic Analyzer
- Phase-aware extraction
- Domain-specific entity extraction
- Critical analysis elements (assumptions, limitations)
- Future work and insights extraction

**Usage:**
```python
from agents import AcademicExtractor

extractor = AcademicExtractor()
metadata = extractor.process_file(Path("paper_analysis.md"))
```

## Chronicle Extractor (`chronicle_extractor.py`)

Extracts metadata from daily, weekly, and monthly notes.

**Features:**
- Multi-type support (daily, weekly, monthly)
- Template-aligned extraction
- Automatic note type detection
- Common fields + type-specific fields

**Usage:**
```python
from agents import SimpleMetadataExtractor

extractor = SimpleMetadataExtractor()
metadata = extractor.process_file(Path("daily_note.md"))
```

## Workflow Examples

### Academic Paper Processing
```python
# Step 1: Analyze the paper
analyzer = AcademicAnalyzer()
analysis = analyzer.analyze_file(Path("raw_paper.md"))
analysis_path = analyzer.save_analysis(analysis)

# Step 2: Extract entities from the analysis
extractor = AcademicExtractor()
entities = extractor.process_file(analysis_path)
```

### Chronicle Note Processing
```python
# Direct extraction from notes
extractor = SimpleMetadataExtractor()
metadata = extractor.process_file(Path("2025-01-15.md"))
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