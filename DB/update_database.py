#!/usr/bin/env python3
"""
Incremental database updater
Updates existing database with new documents and changes
"""

import sqlite3
import sys
from pathlib import Path
import argparse
import json

# Add parent and blueprints to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Add blueprints to path (robust path resolution)
blueprint_core_path = Path(__file__).parent.parent / "blueprints" / "core"
if str(blueprint_core_path) not in sys.path:
    sys.path.insert(0, str(blueprint_core_path))

try:
    from blueprint_loader import get_blueprint_loader  # type: ignore
except ImportError as e:
    print(f"Error importing blueprint_loader: {e}")
    print(f"Blueprint path: {blueprint_core_path}")
    raise

from DB.populator import DatabasePopulator
from DB.utils.chunker import DocumentChunker
from DB.utils.embeddings import EmbeddingGenerator
from KG.graph_builder import GraphBuilder


def get_existing_documents(db_path: str):
    """Get list of existing documents in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    existing_docs = {}
    
    # Get academic documents
    cursor.execute("SELECT id, file_path FROM academic_documents")
    for doc_id, file_path in cursor.fetchall():
        existing_docs[file_path] = ('academic', doc_id)
    
    # Get chronicle documents
    cursor.execute("SELECT id, file_path FROM chronicle_documents")
    for doc_id, file_path in cursor.fetchall():
        existing_docs[file_path] = ('chronicle', doc_id)
    
    conn.close()
    return existing_docs


def check_embedding_model_version(db_path: str):
    """Check if embeddings need to be regenerated due to model change"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check for old model embeddings
    cursor.execute("""
        SELECT COUNT(*) FROM embeddings 
        WHERE embedding_model = 'text-embedding-3-small'
        OR embedding_model IS NULL
    """)
    old_count = cursor.fetchone()[0]
    
    conn.close()
    return old_count > 0


def update_database(db_path: str, skip_embeddings: bool = False, skip_graph: bool = False, 
                   skip_deduplication: bool = False):
    """Update existing database with new documents and changes"""
    
    blueprint_loader = get_blueprint_loader()
    
    print("\n" + "="*60)
    print("INCREMENTAL DATABASE UPDATE")
    print("="*60)
    
    # Step 1: Check for new documents
    print("\nStep 1: Checking for new documents")
    print("-" * 40)
    
    existing_docs = get_existing_documents(db_path)
    print(f"Found {len(existing_docs)} existing documents in database")
    
    populator = DatabasePopulator(db_path)
    
    # Process all document types found in blueprints
    new_doc_count = 0
    new_doc_ids = []
    
    for doc_type in blueprint_loader.list_document_types():
        # Use absolute paths relative to project root
        project_root = Path(__file__).parent.parent
        metadata_dir = project_root / f"raw_data/{doc_type}/extracted_metadata"
        if doc_type == 'personal':
            metadata_dir = project_root / "raw_data/personal_notes/extracted_metadata"
        
        if metadata_dir.exists():
            json_files = list(metadata_dir.glob("*_metadata.json"))
            new_files = []
            
            # Check which files are new
            for json_file in json_files:
                # Check if this document already exists
                with open(json_file) as f:
                    metadata = json.load(f)
                
                # Get file path
                file_path = metadata.get('file_path', str(json_file))
                if len(file_path) > 255:  # Truncate if too long
                    file_path = str(json_file)
                
                if file_path not in existing_docs:
                    new_files.append(json_file)
            
            if new_files:
                print(f"\nFound {len(new_files)} new {doc_type} documents")
                for json_file in new_files:
                    print(f"  Processing {json_file.name}...")
                    try:
                        doc_id = populator.populate_from_json(json_file, doc_type)
                        if doc_id:
                            new_doc_ids.append((doc_type, doc_id))
                            new_doc_count += 1
                    except Exception as e:
                        print(f"    Error processing {json_file}: {e}")
    
    print(f"\n✓ Added {new_doc_count} new documents")
    
    # Step 2: Update chunks for new documents
    if new_doc_ids:
        print("\nStep 2: Creating chunks for new documents")
        print("-" * 40)
        
        chunker = DocumentChunker(chunk_size=800, chunk_overlap=150, min_chunk_size=300)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        total_chunks = 0
        total_mappings = 0
        
        for doc_type, doc_id in new_doc_ids:
            # Get document content
            table = 'academic_documents' if doc_type == 'academic' else 'chronicle_documents'
            cursor.execute(f"SELECT content FROM {table} WHERE id = ?", (doc_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                content = result[0]
                # Map doc_type to database document type
                db_doc_type = 'chronicle' if doc_type == 'personal' else doc_type
                
                chunk_ids = chunker.chunk_and_store(db_path, doc_id, db_doc_type, content)
                mappings = chunker.map_entities_to_chunks(db_path, doc_id, db_doc_type)
                
                total_chunks += len(chunk_ids)
                total_mappings += mappings
                print(f"  {doc_type} doc {doc_id}: {len(chunk_ids)} chunks, {mappings} mappings")
        
        print(f"✓ Created {total_chunks} new chunks with {total_mappings} entity mappings")
        conn.close()
    
    # Step 3: Check and update embeddings
    if not skip_embeddings:
        print("\nStep 3: Checking embeddings")
        print("-" * 40)
        
        try:
            embedder = EmbeddingGenerator(db_path)
            
            # Check if we need to regenerate due to model change
            if check_embedding_model_version(db_path):
                print("⚠️  Old embedding model detected, regenerating ALL embeddings...")
                doc_count = embedder.generate_document_embeddings()
                chunk_count = embedder.generate_chunk_embeddings()
                entity_count = embedder.generate_entity_embeddings()
                print(f"✓ Regenerated all {doc_count + chunk_count + entity_count} embeddings")
            else:
                # Just generate embeddings for new content
                print("  Generating embeddings for new content...")
                
                # Generate embeddings for new documents
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                new_embeddings = 0
                
                # New document embeddings
                for doc_type, doc_id in new_doc_ids:
                    entity_id = f"{doc_type}_{doc_id}"
                    
                    cursor.execute("""
                        SELECT COUNT(*) FROM embeddings 
                        WHERE entity_type = 'document' AND entity_id = ?
                    """, (entity_id,))
                    
                    if cursor.fetchone()[0] == 0:
                        # Generate embedding for this document
                        text = embedder.prepare_document_text(doc_id, doc_type)
                        if text:
                            embedding = embedder.generate_embedding(text)
                            embedder.store_embedding('document', entity_id, embedding)
                            new_embeddings += 1
                
                # Generate chunk embeddings for new documents
                chunk_count = embedder.generate_chunk_embeddings()
                
                # Generate entity embeddings for any new entities
                entity_count = embedder.generate_entity_embeddings()
                
                conn.close()
                print(f"✓ Generated {new_embeddings + chunk_count + entity_count} new embeddings")
                
        except Exception as e:
            print(f"⚠️  Warning: Could not generate embeddings: {e}")
            print("   Make sure OPENAI_API_KEY is set in your .env file")
    
    # Step 4: Entity deduplication for new entities
    if not skip_deduplication and new_doc_count > 0:
        print("\nStep 4: Entity deduplication for new entities")
        print("-" * 40)
        print("  Running deduplication with blueprint-driven entities...")
        
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "../agents/entity_deduplicator.py", 
                "--db", "metadata.db",  # Specify correct path when running from DB dir
                "--parallel-workers", "20", "--merge"
            ], cwd="DB", capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Entity deduplication completed")
                # Show summary from stdout
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-10:]:
                        if line.strip() and ('Total:' in line or 'removed' in line or 'merged' in line):
                            print(f"  {line}")
            else:
                print("⚠️  Deduplication encountered issues")
                print(f"  Return code: {result.returncode}")
                
                # Show detailed error information
                if result.stderr:
                    print("\n  Error details:")
                    print("-" * 40)
                    for line in result.stderr.strip().split('\n')[:10]:
                        print(f"  {line}")
                    print("-" * 40)
                
                # Also show any stdout that might contain error info
                if result.stdout:
                    print("\n  Output before error:")
                    print("-" * 40)
                    for line in result.stdout.strip().split('\n')[-5:]:
                        print(f"  {line}")
                    print("-" * 40)
        except Exception as e:
            print(f"⚠️  Could not run deduplication: {e}")
    
    # Step 5: Update knowledge graph
    if not skip_graph:
        print("\nStep 5: Updating knowledge graph")
        print("-" * 40)
        
        try:
            graph_builder = GraphBuilder(db_path)
            graph_data = graph_builder.export_graph("KG/knowledge_graph.json")
            
            print(f"✓ Updated knowledge graph:")
            print(f"  - Nodes: {graph_data['metadata']['total_nodes']}")
            print(f"  - Edges: {graph_data['metadata']['total_edges']}")
            print(f"  - Node types: {len(graph_data['metadata']['node_types'])}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not update knowledge graph: {e}")


def print_update_summary(db_path: str):
    """Print summary of database after update"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\nDatabase Update Summary:")
    print("="*40)
    
    # Document counts
    cursor.execute("SELECT COUNT(*) FROM academic_documents")
    academic_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM chronicle_documents")
    chronicle_count = cursor.fetchone()[0]
    
    # Entity counts
    cursor.execute("SELECT COUNT(*) FROM topics")
    topic_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM people")
    people_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM methods")
    method_count = cursor.fetchone()[0]
    
    # Processing counts
    cursor.execute("SELECT COUNT(*) FROM document_chunks")
    chunk_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM embeddings")
    embedding_count = cursor.fetchone()[0]
    
    print(f"Documents:")
    print(f"  - Academic: {academic_count}")
    print(f"  - Personal: {chronicle_count}")
    print(f"Entities:")
    print(f"  - Topics: {topic_count}")
    print(f"  - People: {people_count}")
    print(f"  - Methods: {method_count}")
    print(f"Processing:")
    print(f"  - Chunks: {chunk_count}")
    print(f"  - Embeddings: {embedding_count}")
    
    conn.close()


def main():
    """Main entry point for incremental database updater"""
    parser = argparse.ArgumentParser(description='Update existing database with new documents')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (in DB folder)')
    parser.add_argument('--skip-embeddings', action='store_true',
                       help='Skip embedding generation/updates')
    parser.add_argument('--skip-graph', action='store_true',
                       help='Skip knowledge graph update')
    parser.add_argument('--no-deduplication', action='store_true',
                       help='Skip entity deduplication')
    
    args = parser.parse_args()
    
    # Ensure we're working with the correct database path
    db_path = Path(__file__).parent / args.db
    
    if not db_path.exists():
        print(f"✗ Database not found: {db_path}")
        print("  Please run build_database.py first to create the database")
        return 1
    
    print(f"✓ Updating database: {db_path}")
    
    # Run incremental update
    update_database(str(db_path), args.skip_embeddings, args.skip_graph, args.no_deduplication)
    
    # Print summary
    print_update_summary(str(db_path))
    
    print("\n" + "="*60)
    print("INCREMENTAL UPDATE COMPLETE")
    print("="*60)
    print("Next steps:")
    print("1. View database: cd .. && ./view_database.sh")
    print("2. Test graph: open web_ui/index.html")
    print("3. Test queries: python ../interactive_agent.py")


if __name__ == "__main__":
    main()