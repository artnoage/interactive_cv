#!/usr/bin/env python3
"""
Blueprint-driven metadata populator
Generic populator that works with any document type based on blueprint configurations
"""

import json
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add blueprints to path (robust path resolution)
blueprint_core_path = Path(__file__).parent.parent / "blueprints" / "core"
if str(blueprint_core_path) not in sys.path:
    sys.path.insert(0, str(blueprint_core_path))

try:
    from blueprint_loader import get_blueprint_loader # type: ignore
except ImportError as e:
    print(f"Error importing blueprint_loader: {e}")
    print(f"Blueprint path: {blueprint_core_path}")
    print(f"Path exists: {blueprint_core_path.exists()}")
    raise


class DatabasePopulator:
    """Populates database from extracted metadata JSON files using blueprint configurations"""
    
    def __init__(self, db_path: str = "DB/metadata.db"):
        self.db_path = db_path
        self.blueprint_loader = get_blueprint_loader()
        self._ensure_database()
    
    def _ensure_database(self):
        """Ensure database exists and has proper schema"""
        conn = sqlite3.connect(self.db_path)
        conn.close()
    
    def populate_from_json(self, json_path: Path, doc_type: str) -> Optional[int]:
        """Populate database from a single JSON metadata file using blueprints"""
        
        with open(json_path) as f:
            metadata = json.load(f)
        
        # Load blueprint configurations
        database_mapping = self.blueprint_loader.get_database_mapping(doc_type)
        document_mapping = self.blueprint_loader.get_document_mapping(doc_type)
        special_handling = self.blueprint_loader.get_special_handling(doc_type)
        confidence_scores = self.blueprint_loader.get_relationship_confidence(doc_type)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            # Get document table and ID prefix from blueprint
            doc_table = document_mapping.get('table')
            id_prefix = document_mapping.get('id_prefix', doc_type)
            
            # Get file path for content loading (ensure it's reasonable length)
            raw_file_path = metadata.get('file_path', str(json_path))
            # Truncate if unreasonably long (likely content instead of path)
            if len(raw_file_path) > 255:  # Max reasonable file path
                file_path = str(json_path)  # Fall back to JSON path
                print(f"    Warning: file_path too long ({len(raw_file_path)} chars), using JSON path")
            else:
                file_path = raw_file_path
            
            # Read actual content if available
            content = ""
            content_source = document_mapping.get('content_source')
            
            # For academic documents, try to find the analysis file
            if doc_type == 'academic':
                # Extract base name from metadata JSON file
                base_name = json_path.stem.replace('_metadata', '')
                analysis_path = json_path.parent.parent / 'generated_analyses' / f'{base_name}.md'
                
                if analysis_path.exists():
                    content = analysis_path.read_text()
                    print(f"    Loaded full analysis content from {analysis_path.name} ({len(content)} chars)")
                else:
                    print(f"    Warning: Analysis file not found: {analysis_path}")
                    # Fall back to core_contribution
                    content = metadata.get('core_contribution', metadata.get('summary', ''))
            
            # For other document types, use the configured content source
            elif content_source and content_source in metadata:
                content_value = metadata[content_source]
                # Check if it's a file path or direct content
                if content_source == 'file_path' and isinstance(content_value, str):
                    # Try relative to project root first
                    project_root = Path(__file__).parent.parent
                    source_path = project_root / content_value
                    
                    if not source_path.exists():
                        # Try as absolute path
                        source_path = Path(content_value)
                    
                    if source_path.exists():
                        content = source_path.read_text()
                        print(f"    Loaded content from {source_path.name} ({len(content)} chars)")
                    else:
                        print(f"    Warning: Content file not found: {content_value}")
                        # Fallback content sources
                        content = metadata.get('core_contribution', metadata.get('summary', ''))
                else:
                    # Use the field value directly as content
                    content = str(content_value) if content_value else ""
            
            # Check if document already exists
            cursor.execute(f"SELECT id FROM {doc_table} WHERE file_path = ?", (file_path,))
            existing = cursor.fetchone()
            
            if existing:
                doc_id = existing[0]
                print(f"  Document already exists with ID {doc_id}, updating...")
                # Update existing document using blueprint field mappings
                self._update_document(cursor, doc_table, doc_id, metadata, document_mapping, content)
            else:
                # Insert new document using blueprint field mappings
                doc_id = self._insert_document(cursor, doc_table, metadata, document_mapping, content, file_path)
                print(f"  Created new document with ID {doc_id}")
            
            # Format document ID for relationships
            doc_unified_id = f"{id_prefix}_{doc_id}"
            
            # Clear existing relationships for this document
            cursor.execute("""
                DELETE FROM relationships 
                WHERE source_type = 'document' AND source_id = ?
            """, (doc_unified_id,))
            
            # Process entities using blueprint mappings
            stats = {}
            for field_name, mapping in database_mapping.items():
                if field_name in metadata and metadata[field_name]:
                    entities = metadata[field_name]
                    
                    # Handle different field types based on special handling rules
                    if self._is_object_field(field_name, special_handling):
                        count = self._process_object_entities(
                            cursor, doc_unified_id, entities, mapping, special_handling, confidence_scores
                        )
                    else:
                        count = self._process_string_entities(
                            cursor, doc_unified_id, entities, mapping, confidence_scores
                        )
                    
                    if count > 0:
                        stats[field_name] = count
            
            # Handle special cases (like authors) based on blueprint
            self._handle_special_cases(cursor, doc_unified_id, metadata, doc_type, confidence_scores, stats)
            
            # Log extraction
            cursor.execute("""
                INSERT INTO extraction_log 
                (source_file, extraction_type, extractor_version, entities_extracted, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(json_path),
                f'{doc_type}_json_import',
                'blueprint-v1.0',
                sum(stats.values()),
                'success'
            ))
            
            conn.commit()
            
            # Print summary
            print(f"  ✓ Imported {sum(stats.values())} entities:")
            for entity_type, count in stats.items():
                print(f"    - {entity_type}: {count}")
            
            return doc_id
            
        except Exception as e:
            conn.rollback()
            print(f"  ✗ Error: {e}")
            raise e
        finally:
            conn.close()
    
    def _update_document(self, cursor: sqlite3.Cursor, table: str, doc_id: int, 
                        metadata: Dict[str, Any], document_mapping: Dict[str, Any], content: str):
        """Update existing document using blueprint field mappings"""
        
        field_mappings = document_mapping.get('fields', {})
        
        # Build dynamic update query based on blueprint
        set_clauses = []
        values = []
        
        for db_field, metadata_field in field_mappings.items():
            if isinstance(metadata_field, dict) and 'value' in metadata_field:
                # Static value
                set_clauses.append(f"{db_field} = ?")
                values.append(metadata_field['value'])
            elif metadata_field in metadata:
                # Dynamic value from metadata
                set_clauses.append(f"{db_field} = ?")
                values.append(metadata[metadata_field])
        
        # Always update content and modified timestamp
        set_clauses.extend(["content = ?", "modified_at = CURRENT_TIMESTAMP"])
        values.extend([content, doc_id])
        
        update_query = f"""
            UPDATE {table} 
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """
        
        cursor.execute(update_query, values)
    
    def _insert_document(self, cursor: sqlite3.Cursor, table: str, metadata: Dict[str, Any],
                        document_mapping: Dict[str, Any], content: str, file_path: str) -> int:
        """Insert new document using blueprint field mappings"""
        
        field_mappings = document_mapping.get('fields', {})
        
        # Build dynamic insert query based on blueprint
        columns = ["file_path", "content", "content_hash"]
        values = [file_path, content, str(hash(content))]
        
        for db_field, metadata_field in field_mappings.items():
            columns.append(db_field)
            
            if isinstance(metadata_field, dict) and 'value' in metadata_field:
                # Static value
                values.append(metadata_field['value'])
            elif metadata_field in metadata:
                # Dynamic value from metadata
                values.append(metadata[metadata_field])
            else:
                # Default value
                values.append(None)  # type: ignore  # SQL accepts NULL values
        
        placeholders = ', '.join(['?' for _ in values])
        insert_query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({placeholders})
        """
        
        cursor.execute(insert_query, values)
        return cursor.lastrowid or -1  # Return -1 if None (shouldn't happen with AUTOINCREMENT)
    
    def _is_object_field(self, field_name: str, special_handling: Dict[str, Any]) -> bool:
        """Check if field contains objects based on special handling rules"""
        object_fields = special_handling.get('object_fields', {})
        return field_name in object_fields
    
    def _process_object_entities(self, cursor: sqlite3.Cursor, doc_id: str, entities: List[Dict[str, Any]],
                               mapping, special_handling: Dict[str, Any], confidence_scores: Dict[str, float]) -> int:
        """Process entities that are objects with structured data"""
        
        object_config = special_handling.get('object_fields', {}).get(mapping.metadata_field, {})
        count = 0
        
        for entity in entities:
            if not entity:
                continue
            
            # Extract entity name and metadata based on blueprint configuration
            entity_name = entity.get(object_config.get('name_field', 'name'))
            if not entity_name:
                continue
            
            # Extract additional fields based on blueprint
            entity_data = self._extract_entity_data(entity, mapping, object_config)
            
            # Insert entity
            entity_id = self._insert_entity(cursor, mapping.target_table, entity_name, entity_data, mapping)
            
            if entity_id:
                # Create relationship with confidence from blueprint
                confidence = confidence_scores.get(mapping.relationship_type, mapping.confidence) or 1.0
                self._create_relationship(cursor, doc_id, mapping.entity_type, entity_id, 
                                        mapping.relationship_type, confidence)
                count += 1
        
        return count
    
    def _process_string_entities(self, cursor: sqlite3.Cursor, doc_id: str, entities: List[str],
                               mapping, confidence_scores: Dict[str, float]) -> int:
        """Process entities that are simple strings"""
        
        count = 0
        
        for entity in entities:
            if not entity or not isinstance(entity, str):
                continue
            
            entity_name = entity.strip()
            if not entity_name:
                continue
            
            # Insert entity with category override if specified
            entity_data = {}
            if mapping.category_override:
                if mapping.target_table == 'topics':
                    entity_data['category'] = mapping.category_override
                elif mapping.target_table == 'methods':
                    entity_data['category'] = mapping.category_override
            
            entity_id = self._insert_entity(cursor, mapping.target_table, entity_name, entity_data, mapping)
            
            if entity_id:
                # Create relationship with confidence from blueprint
                confidence = confidence_scores.get(mapping.relationship_type, mapping.confidence) or 1.0
                self._create_relationship(cursor, doc_id, mapping.entity_type, entity_id, 
                                        mapping.relationship_type, confidence)
                count += 1
        
        return count
    
    def _extract_entity_data(self, entity: Dict[str, Any], mapping, object_config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract entity data based on blueprint configuration"""
        
        entity_data = {}
        
        # Handle category/type field
        if mapping.category_handling == 'preserve_original':
            category_field = object_config.get('category_field', 'category')
            if category_field in entity:
                entity_data['category'] = entity[category_field]
        elif mapping.category_override:
            entity_data['category'] = mapping.category_override
        elif mapping.category_field and mapping.category_field in entity:
            entity_data['category'] = entity[mapping.category_field]
        
        # Handle description field
        if mapping.description_field and mapping.description_field in entity:
            entity_data['description'] = entity[mapping.description_field]
        
        # Handle domain field (for applications)
        if mapping.domain_field and mapping.domain_field in entity:
            entity_data['domain'] = entity[mapping.domain_field]
        
        # Handle other table-specific fields
        if mapping.target_table == 'people':
            if 'role' in entity:
                entity_data['role'] = entity['role']
            elif mapping.role_override:
                entity_data['role'] = mapping.role_override
            
            if 'affiliation' in entity:
                entity_data['affiliation'] = entity['affiliation']
        
        elif mapping.target_table == 'institutions':
            if 'type' in entity:
                entity_data['type'] = entity['type']
            if 'location' in entity:
                entity_data['location'] = entity['location']
        
        return entity_data
    
    def _insert_entity(self, cursor: sqlite3.Cursor, table: str, name: str, 
                      entity_data: Dict[str, Any], mapping) -> Optional[int]:
        """Insert entity into appropriate table with conflict handling"""
        
        try:
            if table == 'topics':
                if 'category' in entity_data and 'description' in entity_data:
                    cursor.execute("""
                        INSERT INTO topics (name, category, description) 
                        VALUES (?, ?, ?)
                        ON CONFLICT(name) DO UPDATE SET
                            category = COALESCE(category, excluded.category),
                            description = COALESCE(description, excluded.description)
                    """, (name, entity_data['category'], entity_data['description']))
                elif 'category' in entity_data:
                    cursor.execute("""
                        INSERT INTO topics (name, category) 
                        VALUES (?, ?)
                        ON CONFLICT(name) DO UPDATE SET
                            category = COALESCE(category, excluded.category)
                    """, (name, entity_data['category']))
                else:
                    cursor.execute("INSERT OR IGNORE INTO topics (name) VALUES (?)", (name,))
            
            elif table == 'people':
                role = entity_data.get('role')
                affiliation = entity_data.get('affiliation')
                cursor.execute("""
                    INSERT INTO people (name, role, affiliation) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        role = COALESCE(role, excluded.role),
                        affiliation = COALESCE(affiliation, excluded.affiliation)
                """, (name, role, affiliation))
            
            elif table == 'methods':
                category = entity_data.get('category')
                description = entity_data.get('description')
                cursor.execute("""
                    INSERT INTO methods (name, category, description) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        category = COALESCE(category, excluded.category),
                        description = COALESCE(description, excluded.description)
                """, (name, category, description))
            
            elif table == 'applications':
                domain = entity_data.get('domain')
                description = entity_data.get('description')
                cursor.execute("""
                    INSERT INTO applications (name, domain, description) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        domain = COALESCE(domain, excluded.domain),
                        description = COALESCE(description, excluded.description)
                """, (name, domain, description))
            
            elif table == 'institutions':
                inst_type = entity_data.get('type')
                location = entity_data.get('location')
                cursor.execute("""
                    INSERT INTO institutions (name, type, location) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        type = COALESCE(type, excluded.type),
                        location = COALESCE(location, excluded.location)
                """, (name, inst_type, location))
            
            elif table == 'projects':
                description = entity_data.get('description')
                start_date = entity_data.get('start_date')
                end_date = entity_data.get('end_date')
                cursor.execute("""
                    INSERT INTO projects (name, description, start_date, end_date) 
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        description = COALESCE(description, excluded.description),
                        start_date = COALESCE(start_date, excluded.start_date),
                        end_date = COALESCE(end_date, excluded.end_date)
                """, (name, description, start_date, end_date))
            
            else:
                # Generic table
                cursor.execute(f"INSERT OR IGNORE INTO {table} (name) VALUES (?)", (name,))
            
            # Get entity ID
            cursor.execute(f"SELECT id FROM {table} WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            print(f"Error inserting entity {name} into {table}: {e}")
            return None
    
    def _create_relationship(self, cursor: sqlite3.Cursor, source_id: str, target_type: str, 
                           target_id: int, relationship_type: str, confidence: float):
        """Create relationship between document and entity"""
        
        cursor.execute("""
            INSERT OR IGNORE INTO relationships 
            (source_type, source_id, target_type, target_id, relationship_type, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('document', source_id, target_type, str(target_id), relationship_type, confidence))
    
    def _handle_special_cases(self, cursor: sqlite3.Cursor, doc_unified_id: str, 
                            metadata: Dict[str, Any], doc_type: str, 
                            confidence_scores: Dict[str, float], stats: Dict[str, int]):
        """Handle special cases not covered by standard mappings"""
        
        # Handle authors specially (always high confidence)
        if 'authors' in metadata and isinstance(metadata['authors'], list):
            for author in metadata['authors']:
                if author and isinstance(author, str):
                    cursor.execute("""
                        INSERT OR IGNORE INTO people (name, role)
                        VALUES (?, ?)
                    """, (author, 'author'))
                    
                    cursor.execute("SELECT id FROM people WHERE name = ?", (author,))
                    result = cursor.fetchone()
                    if result:
                        person_id = result[0]
                        confidence = confidence_scores.get('authored_by', 1.0)
                        cursor.execute("""
                            INSERT OR IGNORE INTO relationships
                            (source_type, source_id, target_type, target_id, relationship_type, confidence)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, ('document', doc_unified_id, 'person', str(person_id), 'authored_by', confidence))
                        stats['authors'] = stats.get('authors', 0) + 1
    
    def populate_directory(self, metadata_dir: Path, doc_type: str) -> List[int]:
        """Populate database from all JSON files in a directory"""
        
        json_files = list(metadata_dir.glob("*_metadata.json"))
        print(f"\nFound {len(json_files)} {doc_type} metadata files")
        
        processed_ids = []
        for json_file in json_files:
            print(f"\nProcessing {json_file.name}...")
            try:
                doc_id = self.populate_from_json(json_file, doc_type)
                if doc_id:
                    processed_ids.append(doc_id)
            except Exception as e:
                print(f"  Error processing {json_file}: {e}")
        
        return processed_ids


def main():
    """Test the blueprint-driven populator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Blueprint-driven metadata populator')
    parser.add_argument('--db', type=str, default='metadata.db',
                       help='Path to SQLite database')
    parser.add_argument('--academic', type=Path, 
                       default=Path('raw_data/academic/extracted_metadata'),
                       help='Directory with academic metadata JSON files')
    parser.add_argument('--personal', type=Path,
                       default=Path('raw_data/personal_notes/extracted_metadata'),
                       help='Directory with personal notes metadata JSON files')
    parser.add_argument('--type', choices=['all', 'academic', 'personal'], 
                       default='all',
                       help='Which metadata to populate')
    
    args = parser.parse_args()
    
    populator = DatabasePopulator(args.db)
    
    print(f"Blueprint-Driven Metadata Populator")
    print(f"{'='*60}")
    print(f"Database: {args.db}")
    
    total_docs = 0
    
    # Process academic metadata
    if args.type in ['all', 'academic'] and args.academic.exists():
        print(f"\nProcessing academic metadata from: {args.academic}")
        academic_ids = populator.populate_directory(args.academic, 'academic')
        total_docs += len(academic_ids)
        print(f"\n✓ Processed {len(academic_ids)} academic documents")
    
    # Process personal notes metadata
    if args.type in ['all', 'personal'] and args.personal.exists():
        print(f"\nProcessing personal notes metadata from: {args.personal}")
        personal_ids = populator.populate_directory(args.personal, 'personal')
        total_docs += len(personal_ids)
        print(f"\n✓ Processed {len(personal_ids)} personal note documents")
    
    print(f"\n{'='*60}")
    print(f"Total documents processed: {total_docs}")
    print("\nBlueprint-driven system preserves all metadata including:")
    print("  - Rich entity categories from extraction schemas")
    print("  - Proper relationship types and confidence scores")
    print("  - Flexible field mappings defined in blueprints")
    print("  - Domain-agnostic database operations")


if __name__ == "__main__":
    main()