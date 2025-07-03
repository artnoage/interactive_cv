#!/usr/bin/env python3
"""
Migration script to transform the current database to the new v2 schema.
This script:
1. Creates new normalized tables
2. Migrates existing data
3. Creates graph tables
4. Removes redundant structures
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
import hashlib
from datetime import datetime

class DatabaseMigration:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
    
    def backup_database(self):
        """Create a backup before migration"""
        backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Creating backup at {backup_path}...")
        
        backup_conn = sqlite3.connect(backup_path)
        with backup_conn:
            self.conn.backup(backup_conn)
        backup_conn.close()
        print("✓ Backup created")
    
    def create_new_tables(self):
        """Create all new v2 tables"""
        print("\nCreating new tables...")
        
        # Read and execute the schema from DATABASE_SCHEMA_V2.md
        schema_sql = """
        -- Enhanced entity tables
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            description TEXT,
            paper_reference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            domain TEXT,
            description TEXT,
            impact_level TEXT CHECK(impact_level IN ('theoretical', 'experimental', 'production')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Update existing entity tables with new columns
        -- Topics
        ALTER TABLE topics ADD COLUMN category TEXT;
        ALTER TABLE topics ADD COLUMN description TEXT;
        ALTER TABLE topics ADD COLUMN parent_topic_id INTEGER REFERENCES topics(id);
        ALTER TABLE topics ADD COLUMN hierarchy_level INTEGER DEFAULT 0;
        
        -- People
        ALTER TABLE people ADD COLUMN email TEXT;
        ALTER TABLE people ADD COLUMN affiliation TEXT;
        ALTER TABLE people ADD COLUMN role TEXT;
        ALTER TABLE people ADD COLUMN expertise TEXT;
        ALTER TABLE people ADD COLUMN orcid TEXT;
        
        -- Projects
        ALTER TABLE projects ADD COLUMN description TEXT;
        ALTER TABLE projects ADD COLUMN status TEXT CHECK(status IN ('active', 'completed', 'paused', 'planned'));
        ALTER TABLE projects ADD COLUMN project_type TEXT;
        ALTER TABLE projects ADD COLUMN start_date DATE;
        ALTER TABLE projects ADD COLUMN end_date DATE;
        ALTER TABLE projects ADD COLUMN outcomes TEXT;
        
        -- Institutions
        ALTER TABLE institutions ADD COLUMN type TEXT;
        ALTER TABLE institutions ADD COLUMN location TEXT;
        ALTER TABLE institutions ADD COLUMN website TEXT;
        
        -- Document chunks table
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY,
            document_type TEXT NOT NULL,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            start_char INTEGER,
            end_char INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(document_type, document_id, chunk_index)
        );
        
        -- Enhanced embeddings table
        CREATE TABLE IF NOT EXISTS embeddings_v2 (
            id INTEGER PRIMARY KEY,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            embedding BLOB NOT NULL,
            model_name TEXT NOT NULL DEFAULT 'text-embedding-3-small',
            model_version TEXT,
            dimensions INTEGER DEFAULT 1536,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type, entity_id, model_name)
        );
        
        -- Graph tables
        CREATE TABLE IF NOT EXISTS graph_nodes (
            node_id TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            label TEXT NOT NULL,
            attributes JSON,
            degree INTEGER DEFAULT 0,
            pagerank_score FLOAT,
            betweenness_centrality FLOAT,
            community_id INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type, entity_id)
        );
        
        CREATE TABLE IF NOT EXISTS graph_edges (
            edge_id INTEGER PRIMARY KEY,
            source_node_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
            target_node_id TEXT NOT NULL REFERENCES graph_nodes(node_id),
            relationship_type TEXT NOT NULL,
            weight FLOAT DEFAULT 1.0,
            attributes JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_node_id, target_node_id, relationship_type)
        );
        
        -- Extraction log
        CREATE TABLE IF NOT EXISTS extraction_log (
            id INTEGER PRIMARY KEY,
            source_file TEXT NOT NULL,
            extraction_type TEXT NOT NULL,
            extractor_version TEXT,
            entities_extracted INTEGER,
            relationships_extracted INTEGER,
            status TEXT CHECK(status IN ('success', 'partial', 'failed')),
            error_message TEXT,
            duration_seconds FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_embeddings_v2_lookup ON embeddings_v2(entity_type, entity_id);
        CREATE INDEX IF NOT EXISTS idx_chunks_lookup ON document_chunks(document_type, document_id);
        CREATE INDEX IF NOT EXISTS idx_edges_source ON graph_edges(source_node_id);
        CREATE INDEX IF NOT EXISTS idx_edges_target ON graph_edges(target_node_id);
        CREATE INDEX IF NOT EXISTS idx_nodes_type ON graph_nodes(entity_type);
        CREATE INDEX IF NOT EXISTS idx_nodes_pagerank ON graph_nodes(pagerank_score DESC);
        """
        
        # Execute schema in parts to handle existing columns gracefully
        for statement in schema_sql.split(';'):
            if statement.strip():
                try:
                    self.cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e):
                        continue  # Column already exists, skip
                    else:
                        raise
        
        print("✓ New tables created")
    
    def migrate_relationships(self):
        """Consolidate all relationships into the unified table"""
        print("\nMigrating relationships...")
        
        # Get existing relationships from junction tables
        junction_tables = [
            ('document_topics', 'document', 'topic', 'mentions'),
            ('document_people', 'document', 'person', 'authored_by'),
            ('document_projects', 'document', 'project', 'part_of'),
            ('document_institutions', 'document', 'institution', 'affiliated_with')
        ]
        
        for table_name, source_type, target_type, rel_type in junction_tables:
            try:
                # Check if table exists
                self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if not self.cursor.fetchone():
                    continue
                
                # Get document type for proper ID formatting
                if 'chronicle' in table_name:
                    doc_prefix = 'chronicle_'
                elif 'academic' in table_name:
                    doc_prefix = 'academic_'
                else:
                    # Handle generic document tables
                    self.cursor.execute(f"""
                        SELECT DISTINCT d.document_id, 
                               CASE 
                                   WHEN cd.id IS NOT NULL THEN 'chronicle_' || d.document_id
                                   WHEN ad.id IS NOT NULL THEN 'academic_' || d.document_id
                                   ELSE 'unknown_' || d.document_id
                               END as formatted_id,
                               t.{target_type}_id
                        FROM {table_name} d
                        LEFT JOIN chronicle_documents cd ON d.document_id = cd.id
                        LEFT JOIN academic_documents ad ON d.document_id = ad.id
                        JOIN (SELECT * FROM {table_name}) t ON d.document_id = t.document_id
                    """)
                    
                    for row in self.cursor.fetchall():
                        self.cursor.execute("""
                            INSERT OR IGNORE INTO relationships 
                            (source_type, source_id, target_type, target_id, relationship_type)
                            VALUES (?, ?, ?, ?, ?)
                        """, ('document', row['formatted_id'], target_type, str(row[f'{target_type}_id']), rel_type))
                    continue
                
                # Simple case for typed document tables
                self.cursor.execute(f"SELECT * FROM {table_name}")
                for row in self.cursor.fetchall():
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO relationships 
                        (source_type, source_id, target_type, target_id, relationship_type)
                        VALUES (?, ?, ?, ?, ?)
                    """, ('document', f"{doc_prefix}{row['document_id']}", 
                          target_type, str(row[f'{target_type}_id']), rel_type))
                    
            except Exception as e:
                print(f"  Warning: Could not migrate {table_name}: {e}")
        
        # Migrate from existing relationships table if it has different structure
        try:
            self.cursor.execute("SELECT * FROM relationships LIMIT 1")
            existing_rel = self.cursor.fetchone()
            if existing_rel and 'source_type' in existing_rel.keys():
                print("  Existing relationships table already in correct format")
        except:
            pass
        
        print("✓ Relationships migrated")
    
    def migrate_embeddings(self):
        """Migrate embeddings to new format"""
        print("\nMigrating embeddings...")
        
        try:
            # Check if embeddings table exists
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'")
            if not self.cursor.fetchone():
                print("  No embeddings table found, skipping")
                return
            
            # Migrate document embeddings
            self.cursor.execute("""
                INSERT OR IGNORE INTO embeddings_v2 (entity_type, entity_id, embedding, model_name)
                SELECT 
                    'document',
                    CASE 
                        WHEN cd.id IS NOT NULL THEN 'chronicle_' || e.document_id
                        WHEN ad.id IS NOT NULL THEN 'academic_' || e.document_id
                        ELSE 'unknown_' || e.document_id
                    END,
                    e.embedding,
                    'text-embedding-3-small'
                FROM embeddings e
                LEFT JOIN chronicle_documents cd ON e.document_id = cd.id
                LEFT JOIN academic_documents ad ON e.document_id = ad.id
                WHERE e.chunk_index = 0  -- Full document embeddings only
            """)
            
            # Migrate chunk embeddings
            self.cursor.execute("""
                INSERT OR IGNORE INTO embeddings_v2 (entity_type, entity_id, embedding, model_name)
                SELECT 
                    'chunk',
                    'chunk_' || e.document_id || '_' || e.chunk_index,
                    e.embedding,
                    'text-embedding-3-small'
                FROM embeddings e
                WHERE e.chunk_index > 0  -- Chunks only
            """)
            
            print("✓ Embeddings migrated")
            
        except Exception as e:
            print(f"  Warning: Could not migrate embeddings: {e}")
    
    def extract_methods_and_applications(self):
        """Extract methods and applications from existing metadata"""
        print("\nExtracting methods and applications...")
        
        methods_set = set()
        applications_set = set()
        
        # Extract from academic documents
        self.cursor.execute("SELECT id, metadata FROM academic_documents WHERE metadata IS NOT NULL")
        for row in self.cursor.fetchall():
            try:
                metadata = json.loads(row['metadata'])
                
                # Extract methods
                if 'methods' in metadata:
                    methods_set.update(metadata['methods'])
                if 'algorithms' in metadata:
                    methods_set.update(metadata['algorithms'])
                
                # Extract applications
                if 'applications' in metadata:
                    applications_set.update(metadata['applications'])
                    
            except json.JSONDecodeError:
                continue
        
        # Insert methods
        for method in methods_set:
            if method and isinstance(method, str):
                self.cursor.execute("""
                    INSERT OR IGNORE INTO methods (name, category)
                    VALUES (?, ?)
                """, (method, 'algorithm'))
        
        # Insert applications
        for app in applications_set:
            if app and isinstance(app, str):
                self.cursor.execute("""
                    INSERT OR IGNORE INTO applications (name, domain)
                    VALUES (?, ?)
                """, (app, 'general'))
        
        print(f"✓ Extracted {len(methods_set)} methods and {len(applications_set)} applications")
    
    def build_graph_tables(self):
        """Populate graph nodes and edges from relationships"""
        print("\nBuilding graph tables...")
        
        # Clear existing graph data
        self.cursor.execute("DELETE FROM graph_nodes")
        self.cursor.execute("DELETE FROM graph_edges")
        
        # Helper function to create node ID
        def make_node_id(entity_type: str, entity_id: str) -> str:
            if entity_type == 'document':
                return f"doc_{entity_id}"
            else:
                return f"{entity_type}_{entity_id}"
        
        # Collect all entities and create nodes
        entities = []
        
        # Documents
        self.cursor.execute("SELECT unified_id, title FROM documents")
        for row in self.cursor.fetchall():
            entities.append(('document', row['unified_id'], row['title'] or row['unified_id']))
        
        # Topics
        self.cursor.execute("SELECT id, name FROM topics")
        for row in self.cursor.fetchall():
            entities.append(('topic', str(row['id']), row['name']))
        
        # People
        self.cursor.execute("SELECT id, name FROM people")
        for row in self.cursor.fetchall():
            entities.append(('person', str(row['id']), row['name']))
        
        # Projects
        self.cursor.execute("SELECT id, name FROM projects")
        for row in self.cursor.fetchall():
            entities.append(('project', str(row['id']), row['name']))
        
        # Institutions
        self.cursor.execute("SELECT id, name FROM institutions")
        for row in self.cursor.fetchall():
            entities.append(('institution', str(row['id']), row['name']))
        
        # Methods
        self.cursor.execute("SELECT id, name FROM methods")
        for row in self.cursor.fetchall():
            entities.append(('method', str(row['id']), row['name']))
        
        # Applications
        self.cursor.execute("SELECT id, name FROM applications")
        for row in self.cursor.fetchall():
            entities.append(('application', str(row['id']), row['name']))
        
        # Insert nodes
        for entity_type, entity_id, label in entities:
            node_id = make_node_id(entity_type, entity_id)
            self.cursor.execute("""
                INSERT OR IGNORE INTO graph_nodes (node_id, entity_type, entity_id, label)
                VALUES (?, ?, ?, ?)
            """, (node_id, entity_type, entity_id, label))
        
        # Create edges from relationships
        self.cursor.execute("SELECT * FROM relationships")
        edge_id = 1
        for row in self.cursor.fetchall():
            source_node = make_node_id(row['source_type'], row['source_id'])
            target_node = make_node_id(row['target_type'], row['target_id'])
            
            # Check if both nodes exist
            self.cursor.execute("SELECT 1 FROM graph_nodes WHERE node_id IN (?, ?)", 
                              (source_node, target_node))
            if len(self.cursor.fetchall()) == 2:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO graph_edges 
                    (edge_id, source_node_id, target_node_id, relationship_type)
                    VALUES (?, ?, ?, ?)
                """, (edge_id, source_node, target_node, row['relationship_type']))
                edge_id += 1
        
        # Calculate node degrees
        self.cursor.execute("""
            UPDATE graph_nodes
            SET degree = (
                SELECT COUNT(*) FROM graph_edges 
                WHERE source_node_id = graph_nodes.node_id 
                   OR target_node_id = graph_nodes.node_id
            )
        """)
        
        print("✓ Graph tables populated")
    
    def create_views(self):
        """Create helpful views"""
        print("\nCreating views...")
        
        # Documents view already exists, ensure it's correct
        self.cursor.execute("DROP VIEW IF EXISTS documents")
        self.cursor.execute("""
            CREATE VIEW documents AS
            SELECT 
                'chronicle_' || id as unified_id,
                'chronicle' as doc_type,
                id as original_id,
                file_path,
                title,
                date,
                content,
                content_hash,
                created_at,
                modified_at
            FROM chronicle_documents
            UNION ALL
            SELECT 
                'academic_' || id as unified_id,
                'academic' as doc_type,
                id as original_id,
                file_path,
                title,
                date,
                content,
                content_hash,
                created_at,
                modified_at
            FROM academic_documents
        """)
        
        print("✓ Views created")
    
    def cleanup_old_structures(self):
        """Remove redundant tables and columns"""
        print("\nCleaning up old structures...")
        
        # Drop old junction tables (after confirming migration)
        old_tables = [
            'document_topics',
            'document_people', 
            'document_projects',
            'document_institutions',
            'semantic_relationships',
            'semantic_concepts'
        ]
        
        for table in old_tables:
            try:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  Dropped {table}")
            except Exception as e:
                print(f"  Warning: Could not drop {table}: {e}")
        
        # Drop old embeddings table
        self.cursor.execute("DROP TABLE IF EXISTS embeddings")
        
        print("✓ Cleanup completed")
    
    def verify_migration(self):
        """Verify the migration was successful"""
        print("\nVerifying migration...")
        
        # Check key tables exist
        required_tables = [
            'chronicle_documents', 'academic_documents', 'topics', 'people',
            'projects', 'institutions', 'methods', 'applications',
            'relationships', 'graph_nodes', 'graph_edges', 'embeddings_v2'
        ]
        
        for table in required_tables:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not self.cursor.fetchone():
                print(f"  ❌ Missing table: {table}")
                return False
            else:
                # Get row count
                self.cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
                count = self.cursor.fetchone()['cnt']
                print(f"  ✓ {table}: {count} rows")
        
        return True
    
    def run_migration(self):
        """Run the complete migration"""
        print("Starting database migration to v2...")
        print("=" * 60)
        
        try:
            # Start transaction
            self.conn.execute("BEGIN TRANSACTION")
            
            # Backup first
            self.backup_database()
            
            # Run migration steps
            self.create_new_tables()
            self.migrate_relationships()
            self.migrate_embeddings()
            self.extract_methods_and_applications()
            self.build_graph_tables()
            self.create_views()
            
            # Verify before cleanup
            if self.verify_migration():
                self.cleanup_old_structures()
                print("\n✅ Migration completed successfully!")
            else:
                raise Exception("Migration verification failed")
                
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("Rolling back changes...")
            self.conn.rollback()
            raise


def main():
    """Run the migration"""
    import sys
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "metadata.db"
    
    if not Path(db_path).exists():
        print(f"Error: Database {db_path} not found")
        return
    
    print(f"Migrating database: {db_path}")
    response = input("This will modify your database. Continue? (y/N): ")
    
    if response.lower() != 'y':
        print("Migration cancelled")
        return
    
    with DatabaseMigration(db_path) as migration:
        migration.run_migration()


if __name__ == "__main__":
    main()