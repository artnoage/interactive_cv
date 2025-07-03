# Scripts Directory

This directory contains utility scripts for metadata extraction.

## Active Scripts

### extract_personal_notes_metadata.py
Extracts metadata from personal notes using the ChronicleMetadataExtractor.
- Generates JSON metadata files for chronicle notes
- Part of the modular extraction workflow
- Run before database population

**Usage:**
```bash
python scripts/extract_personal_notes_metadata.py

# Options:
--input     # Input directory (default: raw_data/personal_notes)
--output    # Output directory (default: raw_data/personal_notes/extracted_metadata)
--pattern   # File pattern to match (default: *.md)
--dry-run   # Show what would be processed without extracting
```

### extract_academic_metadata.py
Extracts metadata from academic papers using the two-step workflow:
1. Analyzes papers using AcademicAnalyzer
2. Extracts metadata from analyses using AcademicExtractor

**Usage:**
```bash
python scripts/extract_academic_metadata.py

# Options:
--input          # Input directory with papers (default: raw_data/academic/Transcript_MDs)
--analyses       # Directory for analyses (default: raw_data/academic/generated_analyses)
--output         # Output directory (default: raw_data/academic/extracted_metadata)
--use-pro        # Use pro model instead of flash
--skip-analysis  # Skip analysis phase (use existing analyses)
--dry-run        # Show what would be processed without extracting
```

## Workflow

The recommended workflow is:

1. **Extract Metadata** (if needed):
   ```bash
   # For personal notes only (academic already extracted)
   python scripts/extract_personal_notes_metadata.py
   ```

2. **Build or Update Database**:
   ```bash
   # Fresh build
   cd DB && python build_database.py
   
   # Or incremental update
   cd DB && python update_database.py
   ```

## Note

All other processing scripts have been moved to the DB folder:
- Database building: `DB/build_database.py`
- Database updates: `DB/update_database.py`
- Chunking: handled automatically by DB scripts
- Embeddings: handled automatically by DB scripts

See the main CLAUDE.md for complete documentation.