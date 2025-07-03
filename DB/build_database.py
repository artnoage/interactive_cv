#!/usr/bin/env python3
"""
Build database from scratch
Creates a fresh database with complete schema and processes all metadata files
"""

import sqlite3
from pathlib import Path
import argparse
import shutil
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from DB.unified_metadata_populator import UnifiedMetadataPopulator
from DB.chunker import DocumentChunker
from DB.embeddings import EmbeddingGenerator


def create_database_schema(db_path: str):
    """Create fresh database with complete schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Core document tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chronicle_documents (
            id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            date DATE,
            note_type TEXT DEFAULT 'daily',
            content TEXT,
            content_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academic_documents (
            id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            date DATE,
            document_type TEXT DEFAULT 'paper',
            domain TEXT,
            content TEXT,
            content_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Entity tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            role TEXT,
            affiliation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            start_date DATE,
            end_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            type TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            category TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            domain TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Relationships table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            source_type TEXT NOT NULL,
            source_id TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            metadata JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_type, source_id, target_type, target_id, relationship_type)
        )
    """)
    
    # Chunking tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY,
            document_type TEXT NOT NULL,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            section_name TEXT,
            chunk_metadata JSON,
            start_char INTEGER,
            end_char INTEGER,
            token_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(document_type, document_id, chunk_index)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunk_entities (
            chunk_id INTEGER REFERENCES document_chunks(id),
            entity_type TEXT NOT NULL,
            entity_id INTEGER NOT NULL,
            relevance_score FLOAT DEFAULT 1.0,
            PRIMARY KEY (chunk_id, entity_type, entity_id)
        )
    """)
    
    # Embeddings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            embedding BLOB NOT NULL,
            model_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_type, entity_id, model_name)
        )
    """)
    
    # Graph tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graph_nodes (
            id INTEGER PRIMARY KEY,
            node_id TEXT UNIQUE NOT NULL,
            node_type TEXT NOT NULL,
            node_label TEXT NOT NULL,
            attributes JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graph_edges (
            id INTEGER PRIMARY KEY,
            source_node_id TEXT NOT NULL,
            target_node_id TEXT NOT NULL,
            edge_type TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            attributes JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_node_id, target_node_id, edge_type),
            FOREIGN KEY (source_node_id) REFERENCES graph_nodes(node_id),
            FOREIGN KEY (target_node_id) REFERENCES graph_nodes(node_id)
        )
    """)
    
    # Metadata and logging
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extraction_log (
            id INTEGER PRIMARY KEY,
            source_file TEXT NOT NULL,
            extraction_type TEXT NOT NULL,
            extractor_version TEXT,
            entities_extracted INTEGER,
            status TEXT,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_type, source_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_type, target_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_document ON document_chunks(document_type, document_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_entity ON embeddings(entity_type, entity_id)")
    
    # Create backward compatibility view
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS documents AS
        SELECT 
            'chronicle_' || id as unified_id,
            'chronicle' as doc_type,
            id,
            file_path,
            title,
            date,
            note_type,
            NULL as document_type,
            NULL as domain,
            content,
            content_hash,
            created_at,
            modified_at
        FROM chronicle_documents
        UNION ALL
        SELECT 
            'academic_' || id as unified_id,
            'academic' as doc_type,
            id,
            file_path,
            title,
            date,
            NULL as note_type,
            document_type,
            domain,
            content,
            content_hash,
            created_at,
            modified_at
        FROM academic_documents
    """)
    
    conn.commit()
    conn.close()


def build_database(db_path: str, academic_dir: Path, personal_dir: Path, 
                  skip_embeddings: bool = False, skip_graph: bool = False):
    """Build complete database from metadata files"""
    
    # Initialize components
    populator = UnifiedMetadataPopulator(db_path)
    chunker = DocumentChunker(chunk_size=1200, chunk_overlap=200)
    
    print("\n" + "="*60)
    print("BUILDING DATABASE FROM SCRATCH")
    print("="*60)
    
    # Step 1: Populate from metadata
    print("\nStep 1: Importing metadata")
    print("-" * 40)
    
    if academic_dir.exists():
        print(f"Processing academic metadata from {academic_dir}")
        academic_ids = populator.populate_directory(academic_dir, 'academic')
        print(f"✓ Imported {len(academic_ids)} academic documents")
    
    if personal_dir.exists():
        print(f"Processing personal notes metadata from {personal_dir}")
        chronicle_ids = populator.populate_directory(personal_dir, 'chronicle')
        print(f"✓ Imported {len(chronicle_ids)} personal notes")
    
    # Step 2: Create chunks
    print("\nStep 2: Creating document chunks")
    print("-" * 40)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Chunk academic documents
    cursor.execute("SELECT id, content FROM academic_documents WHERE content IS NOT NULL")
    academic_docs = cursor.fetchall()
    
    total_chunks = 0
    total_mappings = 0
    
    for doc_id, content in academic_docs:
        chunk_ids = chunker.chunk_and_store(db_path, doc_id, 'academic', content)
        mappings = chunker.map_entities_to_chunks(db_path, doc_id, 'academic')
        total_chunks += len(chunk_ids)
        total_mappings += mappings
    
    print(f"✓ Academic: {len(academic_docs)} documents → {total_chunks} chunks")
    
    # Chunk personal notes
    cursor.execute("SELECT id, content FROM chronicle_documents WHERE content IS NOT NULL")
    chronicle_docs = cursor.fetchall()
    
    chronicle_chunks = 0
    chronicle_mappings = 0
    
    for doc_id, content in chronicle_docs:
        chunk_ids = chunker.chunk_and_store(db_path, doc_id, 'chronicle', content)
        mappings = chunker.map_entities_to_chunks(db_path, doc_id, 'chronicle')
        chronicle_chunks += len(chunk_ids)
        chronicle_mappings += mappings
    
    print(f"✓ Chronicle: {len(chronicle_docs)} documents → {chronicle_chunks} chunks")
    print(f"✓ Total entity-chunk mappings: {total_mappings + chronicle_mappings}")
    
    conn.close()
    
    # Step 3: Generate embeddings
    if not skip_embeddings:
        print("\nStep 3: Generating embeddings")
        print("-" * 40)
        
        try:
            embedder = EmbeddingGenerator(db_path)
            
            doc_count = embedder.generate_document_embeddings()
            chunk_count = embedder.generate_chunk_embeddings()
            entity_count = embedder.generate_entity_embeddings()
            
            print(f"✓ Generated {doc_count + chunk_count + entity_count} embeddings")
            print(f"  - Documents: {doc_count}")
            print(f"  - Chunks: {chunk_count}")
            print(f"  - Entities: {entity_count}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not generate embeddings: {e}")
            print("   Make sure OPENAI_API_KEY is set in your .env file")
    
    # Step 4: Update graph tables
    if not skip_graph:
        print("\nStep 4: Building knowledge graph")
        print("-" * 40)
        
        try:
            from populate_graph_tables import populate_graph_tables
            populate_graph_tables(db_path)
            print("✓ Graph tables populated")
        except Exception as e:
            print(f"⚠️  Warning: Could not update graph tables: {e}")
    
    # Print final statistics
    print("\n" + "="*60)
    print("DATABASE BUILD COMPLETE")
    print("="*60)
    print_database_stats(db_path)


def print_database_stats(db_path: str):
    """Print database statistics"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    stats = []
    tables = [
        ('academic_documents', 'Academic Documents'),
        ('chronicle_documents', 'Personal Notes'),
        ('topics', 'Topics'),
        ('people', 'People'),
        ('projects', 'Projects'),
        ('institutions', 'Institutions'),
        ('methods', 'Methods'),
        ('applications', 'Applications'),
        ('relationships', 'Relationships'),
        ('document_chunks', 'Document Chunks'),
        ('chunk_entities', 'Chunk-Entity Mappings'),
        ('embeddings', 'Embeddings'),
        ('graph_nodes', 'Graph Nodes'),
        ('graph_edges', 'Graph Edges')
    ]
    
    for table, name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        stats.append((name, count))
    
    conn.close()
    
    print("\nDatabase Statistics:")
    for name, count in stats:
        print(f"{name:.<30} {count:>6}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Build database from scratch')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (will be created in DB folder)')
    parser.add_argument('--backup', action='store_true', 
                       help='Backup existing database before rebuilding')
    parser.add_argument('--academic-dir', type=Path, 
                       default=Path("../raw_data/academic/extracted_metadata"),
                       help='Directory with academic metadata JSONs')
    parser.add_argument('--personal-dir', type=Path,
                       default=Path("../raw_data/personal_notes/extracted_metadata"),
                       help='Directory with personal notes metadata JSONs')
    parser.add_argument('--skip-embeddings', action='store_true',
                       help='Skip embedding generation')
    parser.add_argument('--skip-graph', action='store_true',
                       help='Skip graph table population')
    
    args = parser.parse_args()
    
    # Ensure we're working in the DB directory
    db_path = Path(__file__).parent / args.db
    
    # Backup existing database if requested
    if args.backup and db_path.exists():
        backup_path = db_path.parent / f"{args.db}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backed up existing database to: {backup_path}")
    
    # Remove old database
    if db_path.exists():
        db_path.unlink()
        print(f"✓ Removed existing database: {db_path}")
    
    # Create database with schema
    print(f"✓ Creating new database: {db_path}")
    create_database_schema(str(db_path))
    
    # Build database
    build_database(str(db_path), args.academic_dir, args.personal_dir,
                  args.skip_embeddings, args.skip_graph)
    
    print("\nNext steps:")
    print("1. Generate knowledge graph: python ../KG/knowledge_graph.py metadata.db")
    print("2. View database: cd .. && ./view_database.sh")
    print("3. Test queries: python ../interactive_agent.py")


if __name__ == "__main__":
    main()