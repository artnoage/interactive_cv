"""
Base extractor class for metadata extraction.
Provides common functionality for chronicle and academic extractors.
"""

import hashlib
import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any


class DateJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles date objects."""
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)


class BaseExtractor(ABC):
    """Base class for metadata extractors."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db"):
        self.db_path = db_path
    
    def calculate_hash(self, content: str) -> str:
        """Calculate MD5 hash of content."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with JSON support."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @abstractmethod
    def extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from content. Must be implemented by subclasses."""
        pass
    
    def document_exists(self, file_path: str) -> Optional[int]:
        """Check if document exists and return its ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM documents WHERE file_path = ?", (file_path,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def content_changed(self, file_path: str, new_hash: str) -> bool:
        """Check if content has changed based on hash."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT content_hash FROM documents WHERE file_path = ?", (file_path,))
        result = cursor.fetchone()
        
        conn.close()
        
        if not result:
            return True  # New file
        
        return result[0] != new_hash
    
    def save_metadata(self, file_path: str, doc_type: str, metadata: Dict[str, Any], 
                     content_hash: str, embedding: Optional[bytes] = None):
        """Save metadata to database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if document exists
            doc_id = self.document_exists(file_path)
            
            # Prepare core fields
            title = metadata.get('title', Path(file_path).stem)
            date = metadata.get('date')
            metadata_json = json.dumps(metadata, cls=DateJSONEncoder)
            
            if doc_id:
                # Update existing document
                cursor.execute("""
                    UPDATE documents 
                    SET title = ?, date = ?, content_hash = ?, 
                        metadata = ?, embedding = ?, modified_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (title, date, content_hash, metadata_json, embedding, doc_id))
            else:
                # Insert new document
                cursor.execute("""
                    INSERT INTO documents 
                    (file_path, doc_type, title, date, content_hash, metadata, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (file_path, doc_type, title, date, content_hash, metadata_json, embedding))
                doc_id = cursor.lastrowid
            
            # Update related tables
            assert doc_id is not None, "doc_id should not be None after insert/update"
            self._update_topics(cursor, doc_id, metadata.get('topics', []))
            self._update_people(cursor, doc_id, metadata.get('people', []))
            self._update_projects(cursor, doc_id, metadata.get('projects', []))
            
            conn.commit()
            return doc_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _update_topics(self, cursor: sqlite3.Cursor, doc_id: int, topics: List[str]):
        """Update document-topic relationships."""
        # Clear existing relationships
        cursor.execute("DELETE FROM document_topics WHERE document_id = ?", (doc_id,))
        
        for topic in topics:
            # Insert topic if not exists
            cursor.execute("INSERT OR IGNORE INTO topics (name) VALUES (?)", (topic,))
            
            # Get topic ID
            cursor.execute("SELECT id FROM topics WHERE name = ?", (topic,))
            topic_id = cursor.fetchone()[0]
            
            # Create relationship
            cursor.execute(
                "INSERT INTO document_topics (document_id, topic_id) VALUES (?, ?)",
                (doc_id, topic_id)
            )
    
    def _update_people(self, cursor: sqlite3.Cursor, doc_id: int, people: List[str]):
        """Update document-people relationships."""
        # Clear existing relationships
        cursor.execute("DELETE FROM document_people WHERE document_id = ?", (doc_id,))
        
        for person in people:
            # Insert person if not exists
            cursor.execute("INSERT OR IGNORE INTO people (name) VALUES (?)", (person,))
            
            # Get person ID
            cursor.execute("SELECT id FROM people WHERE name = ?", (person,))
            person_id = cursor.fetchone()[0]
            
            # Create relationship
            cursor.execute(
                "INSERT INTO document_people (document_id, person_id) VALUES (?, ?)",
                (doc_id, person_id)
            )
    
    def _update_projects(self, cursor: sqlite3.Cursor, doc_id: int, projects: List[str]):
        """Update document-project relationships."""
        # Clear existing relationships
        cursor.execute("DELETE FROM document_projects WHERE document_id = ?", (doc_id,))
        
        for project in projects:
            # Insert project if not exists
            cursor.execute("INSERT OR IGNORE INTO projects (name) VALUES (?)", (project,))
            
            # Get project ID
            cursor.execute("SELECT id FROM projects WHERE name = ?", (project,))
            project_id = cursor.fetchone()[0]
            
            # Create relationship
            cursor.execute(
                "INSERT INTO document_projects (document_id, project_id) VALUES (?, ?)",
                (doc_id, project_id)
            )
    
    def process_file(self, file_path: Path) -> Optional[int]:
        """Process a single file and extract metadata."""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Calculate hash
            content_hash = self.calculate_hash(content)
            
            # Check if content changed
            if not self.content_changed(str(file_path), content_hash):
                print(f"Skipping {file_path} - no changes detected")
                return None
            
            # Extract metadata
            metadata = self.extract_metadata(file_path, content)
            
            # Determine document type
            doc_type = self.get_doc_type(file_path)
            
            # Save to database
            doc_id = self.save_metadata(
                str(file_path),
                doc_type,
                metadata,
                content_hash
            )
            
            print(f"Processed {file_path} - ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    @abstractmethod
    def get_doc_type(self, file_path: Path) -> str:
        """Get document type for the file."""
        pass