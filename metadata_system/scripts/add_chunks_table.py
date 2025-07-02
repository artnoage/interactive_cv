#!/usr/bin/env python3
"""
Add document_chunks table to existing database for storing paper sections.
"""

import sqlite3
from pathlib import Path

def add_chunks_table(db_path: str = "metadata_system/metadata.db"):
    """Add chunks table to existing database."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create chunks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_type TEXT,  -- 'section', 'theorem', 'method', etc.
            chunk_title TEXT,
            chunk_content TEXT,
            embedding BLOB,
            chunk_order INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
        )
        """)
        
        # Create indexes
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_document_id 
        ON document_chunks(document_id)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_type 
        ON document_chunks(chunk_type)
        """)
        
        conn.commit()
        print("✅ Successfully added document_chunks table")
        
        # Verify table was created
        cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='document_chunks'
        """)
        
        if cursor.fetchone():
            print("✅ Table verified")
        else:
            print("❌ Table creation failed")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    add_chunks_table()