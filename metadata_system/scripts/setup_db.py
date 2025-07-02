#!/usr/bin/env python3
"""
Database setup script for Interactive CV metadata system.
Creates SQLite database with schema for documents, topics, people, and projects.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

def create_database(db_path: str = "metadata.db"):
    """Create SQLite database with the required schema."""
    
    # Ensure parent directory exists
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE NOT NULL,
        doc_type TEXT NOT NULL CHECK(doc_type IN ('chronicle', 'academic')),
        title TEXT,
        date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        content_hash TEXT,
        metadata JSON,
        embedding BLOB
    )
    """)
    
    # Create topics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    
    # Create document_topics junction table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_topics (
        document_id INTEGER,
        topic_id INTEGER,
        PRIMARY KEY (document_id, topic_id),
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
        FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
    )
    """)
    
    # Create people table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    
    # Create document_people junction table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_people (
        document_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (document_id, person_id),
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
    )
    """)
    
    # Create projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    
    # Create document_projects junction table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_projects (
        document_id INTEGER,
        project_id INTEGER,
        PRIMARY KEY (document_id, project_id),
        FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    )
    """)
    
    # Create indexes for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_file_path ON documents(file_path)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_doc_type ON documents(doc_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_documents_date ON documents(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_name ON topics(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_people_name ON people(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name)")
    
    # Create trigger to update modified_at timestamp
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS update_documents_modified_at 
    AFTER UPDATE ON documents
    BEGIN
        UPDATE documents SET modified_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END
    """)
    
    # Commit changes
    conn.commit()
    
    # Verify tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"Database created at: {os.path.abspath(db_path)}")
    print(f"Created tables: {[table[0] for table in tables]}")
    
    # Close connection
    conn.close()
    
    return db_path


def verify_schema(db_path: str = "metadata.db"):
    """Verify the database schema is correct."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check all tables exist
    expected_tables = [
        'documents', 'topics', 'document_topics',
        'people', 'document_people', 
        'projects', 'document_projects'
    ]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    actual_tables = [row[0] for row in cursor.fetchall()]
    
    missing_tables = set(expected_tables) - set(actual_tables)
    if missing_tables:
        print(f"WARNING: Missing tables: {missing_tables}")
        return False
    
    print("✓ All required tables exist")
    
    # Check document table columns
    cursor.execute("PRAGMA table_info(documents)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}
    
    required_columns = {
        'id': 'INTEGER',
        'file_path': 'TEXT',
        'doc_type': 'TEXT',
        'title': 'TEXT',
        'date': 'DATE',
        'created_at': 'TIMESTAMP',
        'modified_at': 'TIMESTAMP',
        'content_hash': 'TEXT',
        'metadata': 'JSON',
        'embedding': 'BLOB'
    }
    
    for col, dtype in required_columns.items():
        if col not in columns:
            print(f"WARNING: Missing column '{col}' in documents table")
            return False
    
    print("✓ Documents table schema is correct")
    
    conn.close()
    return True


if __name__ == "__main__":
    import sys
    
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else "metadata_system/metadata.db"
    
    # Create database
    created_path = create_database(db_path)
    
    # Verify schema
    if verify_schema(created_path):
        print("\n✅ Database setup completed successfully!")
    else:
        print("\n❌ Database setup had issues. Please check the warnings above.")