"""
Base extractor class for the normalized database schema.
Uses the unified relationships table and enhanced entity tables.
"""

import hashlib
import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class DateJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles date objects."""
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)


class BaseExtractor(ABC):
    """Base class for metadata extractors using v2 schema with normalized relationships."""
    
    def __init__(self, db_path: str = "DB/metadata.db"):
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
    
    @abstractmethod
    def get_doc_type(self, file_path: Path) -> str:
        """Get document type. Must be implemented by subclasses."""
        pass
    
    def get_table_name(self, doc_type: str) -> str:
        """Get the appropriate table name based on document type."""
        if doc_type == 'chronicle':
            return 'chronicle_documents'
        elif doc_type == 'academic':
            return 'academic_documents'
        else:
            raise ValueError(f"Unknown document type: {doc_type}")
    
    def document_exists(self, file_path: str, doc_type: str) -> Optional[int]:
        """Check if document exists in the appropriate table and return its ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table = self.get_table_name(doc_type)
        cursor.execute(f"SELECT id FROM {table} WHERE file_path = ?", (file_path,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def content_changed(self, file_path: str, doc_type: str, new_hash: str) -> bool:
        """Check if content has changed based on hash."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table = self.get_table_name(doc_type)
        cursor.execute(f"SELECT content_hash FROM {table} WHERE file_path = ?", (file_path,))
        result = cursor.fetchone()
        
        conn.close()
        
        if not result:
            return True  # New file
        
        return result[0] != new_hash
    
    def save_metadata(self, file_path: str, doc_type: str, metadata: Dict[str, Any], 
                     content_hash: str, content: Optional[str] = None,
                     embedding: Optional[bytes] = None):
        """Save metadata to the appropriate document table and update relationships."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Get the appropriate table
            table = self.get_table_name(doc_type)
            
            # Check if document exists
            doc_id = self.document_exists(file_path, doc_type)
            
            # Prepare core fields
            title = metadata.get('title', Path(file_path).stem)
            date = metadata.get('date')
            
            # Additional fields based on document type
            extra_fields = {}
            if doc_type == 'chronicle':
                extra_fields['note_type'] = metadata.get('note_type', 'daily')
            elif doc_type == 'academic':
                extra_fields['document_type'] = metadata.get('document_type', 'paper')
                extra_fields['domain'] = metadata.get('domain')
            
            if doc_id:
                # Update existing document
                base_query = f"""
                    UPDATE {table} 
                    SET title = ?, date = ?, content_hash = ?, 
                        content = ?, modified_at = CURRENT_TIMESTAMP
                """
                params = [title, date, content_hash, content]
                
                # Add extra fields
                for field, value in extra_fields.items():
                    base_query += f", {field} = ?"
                    params.append(value)
                
                base_query += " WHERE id = ?"
                params.append(doc_id)
                
                cursor.execute(base_query, params)
            else:
                # Insert new document
                fields = ['file_path', 'title', 'date', 'content_hash', 'content']
                values = [file_path, title, date, content_hash, content]
                
                # Add extra fields
                for field, value in extra_fields.items():
                    fields.append(field)
                    values.append(value)
                
                placeholders = ', '.join(['?' for _ in values])
                field_names = ', '.join(fields)
                
                cursor.execute(f"""
                    INSERT INTO {table} ({field_names})
                    VALUES ({placeholders})
                """, values)
                doc_id = cursor.lastrowid
            
            # Format document ID for relationships
            doc_unified_id = f"{doc_type}_{doc_id}"
            
            # Update relationships using the unified table
            assert doc_id is not None, "doc_id should not be None after insert/update"
            
            # Clear existing relationships for this document
            cursor.execute("""
                DELETE FROM relationships 
                WHERE source_type = 'document' AND source_id = ?
            """, (doc_unified_id,))
            
            # Process all entity relationships
            self._process_entities(cursor, doc_unified_id, metadata)
            
            # Save embedding if provided
            if embedding:
                self._save_embedding(cursor, 'document', doc_unified_id, embedding)
            
            # Update extraction log
            self._log_extraction(cursor, file_path, doc_type, metadata)
            
            conn.commit()
            return doc_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _process_entities(self, cursor: sqlite3.Cursor, doc_id: str, metadata: Dict[str, Any]):
        """Process all entities and create relationships."""
        
        # Map of metadata keys to entity types and relationship types
        entity_mappings = [
            ('topics', 'topic', 'mentions'),
            ('people', 'person', 'authored_by'),
            ('projects', 'project', 'part_of'),
            ('institutions', 'institution', 'affiliated_with'),
            ('methods', 'method', 'uses_method'),
            ('algorithms', 'method', 'uses_method'),  # algorithms are methods
            ('applications', 'application', 'has_application'),
            ('mathematical_concepts', 'topic', 'discusses'),  # math concepts are topics
            ('assumptions', 'assumption', 'makes_assumption'),
            ('limitations', 'limitation', 'has_limitation'),
            ('future_work', 'future_work', 'suggests_future_work')
        ]
        
        for metadata_key, entity_type, rel_type in entity_mappings:
            if metadata_key in metadata:
                entities = metadata[metadata_key]
                if isinstance(entities, list):
                    self._create_entity_relationships(
                        cursor, doc_id, entities, entity_type, rel_type
                    )
        
        # Handle special relationships
        if 'builds_on' in metadata and isinstance(metadata['builds_on'], list):
            self._create_entity_relationships(
                cursor, doc_id, metadata['builds_on'], 'topic', 'builds_on'
            )
        
        if 'enables' in metadata and isinstance(metadata['enables'], list):
            self._create_entity_relationships(
                cursor, doc_id, metadata['enables'], 'topic', 'enables'
            )
    
    def _create_entity_relationships(self, cursor: sqlite3.Cursor, doc_id: str,
                                   entities: List[Any], entity_type: str, rel_type: str):
        """Create relationships between document and entities."""
        
        # Get the appropriate entity table
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications',
            'assumption': 'topics',  # Store as topics with category
            'limitation': 'topics',  # Store as topics with category
            'future_work': 'topics'  # Store as topics with category
        }
        
        entity_table = table_map.get(entity_type)
        if not entity_table:
            return  # Skip unknown entity types
        
        for entity in entities:
            if not entity or not isinstance(entity, (str, dict)):
                continue
            
            # Handle entity that might have additional metadata
            if isinstance(entity, dict):
                entity_name = entity.get('name', str(entity))
                entity_metadata = entity
            else:
                entity_name = str(entity)
                entity_metadata = None
            
            # Insert entity if not exists
            if entity_type in ['assumption', 'limitation', 'future_work']:
                # These are stored as topics with a category
                cursor.execute("""
                    INSERT OR IGNORE INTO topics (name, category) 
                    VALUES (?, ?)
                """, (entity_name, entity_type))
                cursor.execute("SELECT id FROM topics WHERE name = ?", (entity_name,))
            else:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO {entity_table} (name) 
                    VALUES (?)
                """, (entity_name,))
                cursor.execute(f"SELECT id FROM {entity_table} WHERE name = ?", (entity_name,))
            
            entity_id = cursor.fetchone()[0]
            
            # Create relationship
            cursor.execute("""
                INSERT OR IGNORE INTO relationships 
                (source_type, source_id, target_type, target_id, relationship_type, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                'document', doc_id, entity_type, str(entity_id), rel_type,
                json.dumps(entity_metadata) if entity_metadata else None
            ))
    
    def _save_embedding(self, cursor: sqlite3.Cursor, entity_type: str, 
                       entity_id: str, embedding: bytes):
        """Save embedding for an entity."""
        cursor.execute("""
            INSERT OR REPLACE INTO embeddings_v2 
            (entity_type, entity_id, embedding, model_name)
            VALUES (?, ?, ?, ?)
        """, (entity_type, entity_id, embedding, 'text-embedding-3-small'))
    
    def _log_extraction(self, cursor: sqlite3.Cursor, file_path: str, 
                       extraction_type: str, metadata: Dict[str, Any]):
        """Log the extraction process."""
        # Count entities extracted
        entity_count = sum(len(v) for k, v in metadata.items() 
                          if isinstance(v, list) and k not in ['date', 'title'])
        
        cursor.execute("""
            INSERT INTO extraction_log 
            (source_file, extraction_type, extractor_version, 
             entities_extracted, status)
            VALUES (?, ?, ?, ?, ?)
        """, (file_path, extraction_type, 'v2.0', entity_count, 'success'))
    
    def process_file(self, file_path: Path) -> Optional[int]:
        """Process a single file and extract metadata."""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Calculate hash
            content_hash = self.calculate_hash(content)
            
            # Determine document type
            doc_type = self.get_doc_type(file_path)
            
            # Check if content changed
            if not self.content_changed(str(file_path), doc_type, content_hash):
                print(f"Skipping {file_path} - no changes detected")
                return None
            
            # Extract metadata
            metadata = self.extract_metadata(file_path, content)
            
            # Save to database
            doc_id = self.save_metadata(
                str(file_path),
                doc_type,
                metadata,
                content_hash,
                content
            )
            
            print(f"Processed {file_path} - Document ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            raise
    
    def update_graph_tables(self):
        """Update the pre-computed graph tables after extraction."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # This would typically be called after a batch of extractions
            # to update the graph_nodes and graph_edges tables
            print("Updating graph tables...")
            
            # Clear and rebuild graph tables
            cursor.execute("DELETE FROM graph_nodes")
            cursor.execute("DELETE FROM graph_edges")
            
            # Rebuild nodes from all entities
            # ... (implementation would go here)
            
            conn.commit()
            print("Graph tables updated")
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _extract_date_from_path(self, file_path: Path) -> Optional[str]:
        """Extract date from file path (for daily notes)."""
        import re
        match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.stem)
        if match:
            return match.group(1)
        return None