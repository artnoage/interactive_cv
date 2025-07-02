# Metadata System Implementation Plan

## Overview
Single-source metadata database with automated chronicle monitoring and manual academic metadata management.

## Architecture Decision
- **SQLite database** for all metadata (single source of truth)
- **File watcher agent** for chronicle updates only (or integrate with existing sync)
- **Manual process** for academic metadata (one-time extraction)
- **JSON export** for debugging and backup

## 🎯 Integration Note: Sync Method Alternative
Instead of running a separate file watcher daemon, consider integrating with the existing `.sync` workflow:
- After `rsync` completes, run metadata extraction on new/changed files
- Single command (`chronicle`) handles both file sync and metadata update
- Simpler workflow, no daemon management needed

## Detailed Implementation Steps

### Phase 1: Database Setup

1. **Install Required Packages**
   ```bash
   pip install sqlite3  # Usually included with Python
   pip install watchdog  # For file monitoring
   pip install sqlalchemy  # For ORM (optional but recommended)
   pip install alembic  # For database migrations
   pip install pydantic  # For data validation
   ```

2. **Create Database Schema**
   ```sql
   -- metadata.db schema
   CREATE TABLE documents (
       id INTEGER PRIMARY KEY,
       file_path TEXT UNIQUE NOT NULL,
       doc_type TEXT NOT NULL,  -- 'chronicle' or 'academic'
       title TEXT,
       date DATE,
       created_at TIMESTAMP,
       modified_at TIMESTAMP,
       content_hash TEXT,  -- To detect changes
       metadata JSON,  -- Flexible JSON field
       embedding BLOB  -- Store vector embeddings
   );

   CREATE TABLE topics (
       id INTEGER PRIMARY KEY,
       name TEXT UNIQUE NOT NULL
   );

   CREATE TABLE document_topics (
       document_id INTEGER,
       topic_id INTEGER,
       FOREIGN KEY (document_id) REFERENCES documents(id),
       FOREIGN KEY (topic_id) REFERENCES topics(id)
   );

   CREATE TABLE people (
       id INTEGER PRIMARY KEY,
       name TEXT UNIQUE NOT NULL
   );

   CREATE TABLE document_people (
       document_id INTEGER,
       person_id INTEGER,
       FOREIGN KEY (document_id) REFERENCES documents(id),
       FOREIGN KEY (person_id) REFERENCES people(id)
   );

   CREATE TABLE projects (
       id INTEGER PRIMARY KEY,
       name TEXT UNIQUE NOT NULL
   );

   CREATE TABLE document_projects (
       document_id INTEGER,
       project_id INTEGER,
       FOREIGN KEY (document_id) REFERENCES documents(id),
       FOREIGN KEY (project_id) REFERENCES projects(id)
   );
   ```

### Phase 2: Metadata Extraction Scripts

1. **Create Base Extractor Class** (`extractors/base.py`)
   - Hash calculation for change detection
   - Common metadata structure
   - Database connection handling

2. **Chronicle Metadata Extractor** (`extractors/chronicle.py`)
   - Parse frontmatter YAML
   - Extract patterns:
     - #hashtags → topics
     - @mentions → people
     - [[wiki-links]] → references
     - Project names from content
   - Calculate content hash
   - Store in database

3. **Academic Metadata Extractor** (`extractors/academic.py`)
   - Parse paper titles and authors
   - Extract key concepts from analysis
   - Identify mathematical methods
   - Link collaborators
   - One-time bulk extraction

### Phase 3: File Watcher Agent

1. **Create Watcher Service** (`watcher/chronicle_monitor.py`)
   ```python
   class ChronicleWatcher:
       def __init__(self, db_path, chronicle_path):
           self.db = Database(db_path)
           self.chronicle_path = chronicle_path
           self.observer = Observer()
           
       def on_modified(self, event):
           if event.src_path.endswith('.md'):
               # Calculate hash
               # Compare with stored hash
               # If different, extract metadata
               # Update database
               
       def on_created(self, event):
           # Extract metadata
           # Insert into database
   ```

2. **Implement Change Detection**
   - MD5 hash of file content
   - Compare with stored hash
   - Only process if changed
   - Log all operations

3. **Create Daemon Script** (`run_watcher.py`)
   - Runs continuously
   - Handles errors gracefully
   - Logs to file
   - Can run as systemd service

### Phase 4: Query Interface

1. **Create Query API** (`query/api.py`)
   ```python
   class MetadataQuery:
       def find_by_topic(self, topic: str):
           # Return all documents with topic
           
       def find_by_person(self, person: str):
           # Return all interactions
           
       def find_by_date_range(self, start, end):
           # Return chronicle entries
           
       def get_project_timeline(self, project: str):
           # Return chronological project mentions
   ```

2. **RAG Integration** (`query/rag.py`)
   - Load embeddings from database
   - Similarity search
   - Combine with metadata filters
   - Return relevant chunks

### Phase 5: Initial Data Population

1. **One-time Academic Import**
   ```bash
   python scripts/import_academic.py --path academic/
   ```

2. **Chronicle History Import**
   ```bash
   python scripts/import_chronicle.py --path chronicle/
   ```

3. **Verify Import**
   - Check document counts
   - Validate metadata extraction
   - Test queries

### Phase 6: Monitoring & Maintenance

1. **Create Status Dashboard** (`monitor/status.py`)
   - Last update times
   - Document counts by type
   - Recent changes
   - Error logs

2. **Backup Strategy**
   - Daily SQLite backup
   - JSON export of metadata
   - Store in `.backup/` directory

3. **Update Procedures**
   - Manual academic updates
   - Force re-extraction command
   - Database migrations with Alembic

## Directory Structure
```
/interactive_cv/
  /metadata_system/
    /extractors/
      - __init__.py
      - base.py
      - chronicle.py
      - academic.py
    /watcher/
      - __init__.py
      - chronicle_monitor.py
    /query/
      - __init__.py
      - api.py
      - rag.py
    /scripts/
      - setup_db.py
      - import_academic.py
      - import_chronicle.py
    /monitor/
      - status.py
    /logs/
      - watcher.log
      - extraction.log
    metadata.db
    run_watcher.py
    requirements.txt
```

## Implementation Status

### ✅ Completed
1. **Database Setup**: SQLite database with full schema for documents, topics, people, projects
2. **Chronicle Metadata Extraction**: LLM-based extraction with optimized prompts
3. **File Watcher**: Automated monitoring with change detection (can be replaced with sync integration)
4. **Academic Metadata Import**: All 12 papers imported with comprehensive metadata
5. **Document Chunking**: 113 semantic chunks created from academic analyses
6. **Embeddings System**: OpenAI embeddings for all documents and chunks
7. **Semantic Search**: Working similarity search at document and chunk level

### 🚧 Remaining Tasks
1. **Query API**: REST/GraphQL interface for programmatic access
2. **RAG Pipeline**: Connect search results to LLM for intelligent responses
3. **Web Interface**: Frontend for interactive CV queries
4. **Sync Integration**: Consider adding metadata update to chronicle sync script

## Current System Capabilities
- **18 documents**: 12 academic papers + 6 chronicle notes
- **113 chunks**: Semantic sections from academic papers
- **163 topics**: Spanning research areas and practical work
- **Embeddings**: All content has vector embeddings for semantic search
- **Database**: Everything stored in `metadata_system/metadata.db`

## Next Steps
1. Build Query API for external access
2. Implement RAG pipeline using existing embeddings
3. Create web interface for users to interact with your CV
4. Optional: Integrate metadata updates into chronicle sync workflow