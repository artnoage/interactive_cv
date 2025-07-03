# Agents System Summary

## Overview

The `agents/` directory contains specialized AI agents for the Interactive CV project:

### Academic Workflow (Two-Step Process)
1. **Academic Analyzer** → Analyzes raw papers to produce structured analyses
2. **Academic Extractor** → Extracts entities and relationships from analyses

### Chronicle Workflow
- **Chronicle Extractor** → Directly extracts metadata from daily/weekly/monthly notes

## Key Changes Made

### 1. Renamed Folder
- `data_extractors/` → `agents/`
- Updated all imports and references

### 2. Created Academic Analyzer
- New agent that follows `How_to_analyze.md` methodology
- Three-phase analysis structure (Reconnaissance, Deep Dive, Synthesis)
- Domain-specific analysis for mathematics, computer science, and physics
- Produces structured markdown analyses

### 3. Updated Academic Extractor
- Now works on analyses (not raw papers)
- Phase-aware extraction
- Added fields: domain, assumptions, limitations, future_work, key_insights
- Aligned with the analysis guide structure

### 4. Cleaned Up
- Removed: config_driven_extractor.py, demo_extractors.py, config_relationship_example.py
- Removed: duplicate extraction_config.yaml
- Kept only essential agents

## Workflow Example

```python
# Step 1: Analyze a paper
analyzer = AcademicAnalyzer()
analysis = analyzer.analyze_file(Path("paper.md"))
analysis_path = analyzer.save_analysis(analysis)

# Step 2: Extract entities from the analysis
extractor = AcademicExtractor()
entities = extractor.process_file(analysis_path)
```

## Config Files
- **Academic**: `raw_data/academic/extraction_schema.json` (updated with new entities)
- **Chronicle**: `raw_data/chronicle/extraction_config_simple.yaml`

## Test Results
Successfully tested the workflow:
- ✓ Academic Analyzer produces comprehensive analyses
- ✓ Academic Extractor extracts entities from analyses
- ✓ Detected domain: computer_science
- ✓ Extracted limitations, future work, key insights
- ✓ Chronicle extractor supports daily/weekly/monthly notes