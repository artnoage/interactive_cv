# Metadata System Implementation Plan

## Overview
Single-source metadata database with automated chronicle monitoring and manual academic metadata management.

## Architecture Decision
- **SQLite database** for all metadata (single source of truth)
- **File watcher agent** for chronicle updates only
- **Manual process** for academic metadata (one-time extraction)
- **JSON export** for debugging and backup

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

## Next Steps Priority
1. Set up SQLite database with schema
2. Create chronicle extractor with pattern matching
3. Build file watcher for chronicle folder
4. One-time academic metadata extraction
5. Implement basic query API
6. Test with your existing notes
7. Add RAG capabilities