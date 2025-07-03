#!/usr/bin/env python3
"""
Unified metadata populator for the database
Reads JSON metadata files from both academic and chronicle extractors
and populates the normalized database
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse


class UnifiedMetadataPopulator:
    """Populates database from extracted metadata JSON files"""
    
    def __init__(self, db_path: str = "DB/metadata.db"):
        self.db_path = db_path
        self._ensure_database()
    
    def _ensure_database(self):
        """Ensure database exists and has proper schema"""
        conn = sqlite3.connect(self.db_path)
        conn.close()
    
    def populate_from_json(self, json_path: Path, doc_type: str) -> Optional[int]:
        """Populate database from a single JSON metadata file"""
        
        with open(json_path) as f:
            metadata = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            # Determine document table and get file path
            if doc_type == 'academic':
                table = 'academic_documents'
                # Academic metadata has file_path pointing to the analysis
                file_path = metadata.get('file_path', str(json_path))
                
                # Read the actual analysis content if available
                analysis_path = Path(file_path)
                if analysis_path.exists():
                    content = analysis_path.read_text()
                else:
                    content = metadata.get('core_contribution', '')
                
            else:  # chronicle
                table = 'chronicle_documents'
                file_path = metadata.get('file_path', str(json_path))
                
                # Read the actual note content if available
                note_path = Path(file_path)
                if note_path.exists():
                    content = note_path.read_text()
                else:
                    content = metadata.get('summary', '')
            
            # Check if document already exists
            cursor.execute(f"SELECT id FROM {table} WHERE file_path = ?", (file_path,))
            existing = cursor.fetchone()
            
            if existing:
                doc_id = existing[0]
                print(f"  Document already exists with ID {doc_id}, updating...")
                # Update existing document
                if doc_type == 'academic':
                    cursor.execute(f"""
                        UPDATE {table} 
                        SET title = ?, date = ?, content = ?, modified_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (
                        metadata.get('title', 'Unknown'),
                        metadata.get('date', metadata.get('year', datetime.now().date().isoformat())),
                        content,
                        doc_id
                    ))
                else:  # chronicle
                    cursor.execute(f"""
                        UPDATE {table} 
                        SET title = ?, date = ?, note_type = ?, content = ?, modified_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (
                        metadata.get('title', 'Unknown'),
                        metadata.get('date', datetime.now().date().isoformat()),
                        metadata.get('note_type', 'daily'),
                        content,
                        doc_id
                    ))
            else:
                # Insert new document
                if doc_type == 'academic':
                    cursor.execute(f"""
                        INSERT INTO {table} (file_path, title, date, document_type, domain, content, content_hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        file_path,
                        metadata.get('title', 'Unknown'),
                        metadata.get('date', metadata.get('year', datetime.now().date().isoformat())),
                        metadata.get('document_type', 'analysis'),
                        metadata.get('domain', 'mathematics'),
                        content,
                        str(hash(content))
                    ))
                else:  # chronicle
                    cursor.execute(f"""
                        INSERT INTO {table} (file_path, title, date, note_type, content, content_hash)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        file_path,
                        metadata.get('title', 'Unknown'),
                        metadata.get('date', datetime.now().date().isoformat()),
                        metadata.get('note_type', 'daily'),
                        content,
                        str(hash(content))
                    ))
                doc_id = cursor.lastrowid
                print(f"  Created new document with ID {doc_id}")
            
            # Format document ID for relationships
            doc_unified_id = f"{doc_type}_{doc_id}"
            
            # Clear existing relationships for this document
            cursor.execute("""
                DELETE FROM relationships 
                WHERE source_type = 'document' AND source_id = ?
            """, (doc_unified_id,))
            
            # Process entities and create relationships
            entity_mappings = [
                ('topics', 'topic', 'discusses'),
                ('people', 'person', 'mentions'),
                ('projects', 'project', 'part_of'),
                ('institutions', 'institution', 'affiliated_with'),
                ('methods', 'method', 'uses_method'),
                ('tools', 'method', 'uses_method'),  # Tools stored as methods
                ('applications', 'application', 'has_application'),
                ('papers', 'topic', 'references'),  # Papers as topics
            ]
            
            # Academic-specific mappings
            if doc_type == 'academic':
                entity_mappings.extend([
                    ('mathematical_concepts', 'topic', 'discusses'),
                    ('research_areas', 'topic', 'discusses'),
                    ('algorithms', 'method', 'uses_method'),
                    ('assumptions', 'topic', 'makes_assumption'),
                    ('limitations', 'topic', 'has_limitation'),
                    ('future_work', 'topic', 'suggests_future_work'),
                    ('theoretical_results', 'topic', 'proves'),
                ])
            else:  # Chronicle-specific
                entity_mappings.extend([
                    ('accomplishments', 'topic', 'accomplished'),
                    ('insights', 'topic', 'discovered'),
                    ('learning', 'topic', 'learned'),
                    ('challenges', 'topic', 'faced_challenge'),
                    ('future_work', 'topic', 'plans'),
                ])
            
            # Process each entity type
            stats = {}
            for metadata_key, entity_type, rel_type in entity_mappings:
                if metadata_key in metadata:
                    entities = metadata[metadata_key]
                    if isinstance(entities, list):
                        count = self._create_entity_relationships(
                            cursor, doc_unified_id, entities, entity_type, rel_type
                        )
                        if count > 0:
                            stats[metadata_key] = count
            
            # Log extraction
            cursor.execute("""
                INSERT INTO extraction_log 
                (source_file, extraction_type, extractor_version, entities_extracted, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                str(json_path),
                f'{doc_type}_json_import',
                'v2.0',
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
    
    def _create_entity_relationships(self, cursor: sqlite3.Cursor, doc_id: str,
                                   entities: List[Any], entity_type: str, rel_type: str) -> int:
        """Create relationships between document and entities"""
        
        # Map entity types to tables
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications',
        }
        
        # Special handling for chronicle-specific entities stored as topics
        if entity_type == 'topic' and rel_type in ['accomplished', 'discovered', 'learned', 'faced_challenge', 'plans']:
            category_map = {
                'accomplished': 'accomplishment',
                'discovered': 'insight',
                'learned': 'learning',
                'faced_challenge': 'challenge',
                'plans': 'future_work'
            }
            category = category_map.get(rel_type, entity_type)
        else:
            category = None
        
        entity_table = table_map.get(entity_type, 'topics')
        count = 0
        
        for entity in entities:
            if not entity:
                continue
            
            # Handle entity that might be a dict or string
            if isinstance(entity, dict):
                entity_name = entity.get('name', str(entity))
            else:
                entity_name = str(entity)
            
            # Insert entity if not exists
            if category:  # Topics with category
                cursor.execute("""
                    INSERT OR IGNORE INTO topics (name, category) 
                    VALUES (?, ?)
                """, (entity_name, category))
            else:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO {entity_table} (name) 
                    VALUES (?)
                """, (entity_name,))
            
            # Get entity ID
            if category:
                cursor.execute("SELECT id FROM topics WHERE name = ? AND category = ?", 
                             (entity_name, category))
            else:
                cursor.execute(f"SELECT id FROM {entity_table} WHERE name = ?", 
                             (entity_name,))
            
            result = cursor.fetchone()
            if result:
                entity_id = result[0]
                
                # Create relationship
                cursor.execute("""
                    INSERT OR IGNORE INTO relationships 
                    (source_type, source_id, target_type, target_id, relationship_type)
                    VALUES (?, ?, ?, ?, ?)
                """, ('document', doc_id, entity_type, str(entity_id), rel_type))
                
                count += 1
        
        return count
    
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
    
    def update_graph_tables(self):
        """Update the pre-computed graph tables after import"""
        try:
            from KG.knowledge_graph import update_graph_tables
            print("\nUpdating knowledge graph tables...")
            update_graph_tables(self.db_path)
            print("✓ Graph tables updated successfully")
        except Exception as e:
            print(f"✗ Error updating graph tables: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Populate database from metadata JSON files')
    parser.add_argument('--db', default="DB/metadata.db", help='Database path')
    parser.add_argument('--academic-dir', type=Path, 
                       default=Path("raw_data/academic/extracted_metadata"),
                       help='Directory with academic metadata JSONs')
    parser.add_argument('--chronicle-dir', type=Path,
                       default=Path("raw_data/chronicle/extracted_metadata"),
                       help='Directory with chronicle metadata JSONs')
    parser.add_argument('--skip-academic', action='store_true', 
                       help='Skip academic metadata')
    parser.add_argument('--skip-chronicle', action='store_true',
                       help='Skip chronicle metadata')
    parser.add_argument('--update-graph', action='store_true',
                       help='Update graph tables after import')
    
    args = parser.parse_args()
    
    populator = UnifiedMetadataPopulator(args.db)
    
    total_processed = 0
    
    # Process academic metadata
    if not args.skip_academic and args.academic_dir.exists():
        print(f"{'='*60}")
        print(f"Processing academic metadata from {args.academic_dir}")
        print(f"{'='*60}")
        academic_ids = populator.populate_directory(args.academic_dir, 'academic')
        total_processed += len(academic_ids)
        print(f"\n✓ Processed {len(academic_ids)} academic documents")
    
    # Process chronicle metadata
    if not args.skip_chronicle and args.chronicle_dir.exists():
        print(f"\n{'='*60}")
        print(f"Processing chronicle metadata from {args.chronicle_dir}")
        print(f"{'='*60}")
        chronicle_ids = populator.populate_directory(args.chronicle_dir, 'chronicle')
        total_processed += len(chronicle_ids)
        print(f"\n✓ Processed {len(chronicle_ids)} chronicle documents")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: Successfully processed {total_processed} documents")
    print(f"{'='*60}")
    
    # Update graph tables if requested
    if args.update_graph:
        populator.update_graph_tables()


if __name__ == "__main__":
    main()