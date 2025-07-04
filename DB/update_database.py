#!/usr/bin/env python3
"""
Update existing database with new documents
Only processes documents that aren't already in the database
"""

import sqlite3
from pathlib import Path
import argparse
import json
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from DB.unified_metadata_populator import UnifiedMetadataPopulator
from DB.chunker import DocumentChunker
from DB.embeddings import EmbeddingGenerator


def get_existing_files(db_path: str, doc_type: str) -> set:
    """Get set of file paths already in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    table = f"{doc_type}_documents"
    cursor.execute(f"SELECT file_path FROM {table}")
    existing = {row[0] for row in cursor.fetchall()}
    
    conn.close()
    return existing


def find_new_metadata_files(metadata_dir: Path, existing_files: set) -> list:
    """Find metadata JSON files not yet in database"""
    new_files = []
    
    if not metadata_dir.exists():
        return new_files
    
    for json_file in metadata_dir.glob("*_metadata.json"):
        # Load metadata to check source file
        with open(json_file, 'r') as f:
            metadata = json.load(f)
        
        source_file = metadata.get('source_file', '')
        if source_file and source_file not in existing_files:
            new_files.append(json_file)
    
    return new_files


def update_document_chunks(db_path: str, doc_id: int, doc_type: str, chunker: DocumentChunker):
    """Create chunks for a single document"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get document content
    table = f"{doc_type}_documents"
    cursor.execute(f"SELECT content FROM {table} WHERE id = ?", (doc_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        content = result[0]
        chunk_ids = chunker.chunk_and_store(db_path, doc_id, doc_type, content)
        mappings = chunker.map_entities_to_chunks(db_path, doc_id, doc_type)
        
        conn.close()
        return len(chunk_ids), mappings
    
    conn.close()
    return 0, 0


def update_document_embeddings(embedder: EmbeddingGenerator, doc_id: int, doc_type: str):
    """Generate embeddings for a single document and its chunks"""
    # Document embedding
    entity_id = f"{doc_type}_{doc_id}"
    text = embedder.prepare_document_text(doc_id, doc_type)
    if text:
        embedding = embedder.generate_embedding(text)
        embedder.store_embedding('document', entity_id, embedding)
    
    # Chunk embeddings
    conn = embedder.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id FROM document_chunks 
        WHERE document_type = ? AND document_id = ?
    """, (doc_type, doc_id))
    
    chunk_ids = [row['id'] for row in cursor.fetchall()]
    conn.close()
    
    for chunk_id in chunk_ids:
        entity_id = f"chunk_{chunk_id}"
        text = embedder.prepare_chunk_text(chunk_id)
        if text:
            embedding = embedder.generate_embedding(text)
            embedder.store_embedding('chunk', entity_id, embedding)
    
    return 1 + len(chunk_ids)  # document + chunks


def update_entity_embeddings(embedder: EmbeddingGenerator, doc_id: int, doc_type: str):
    """Generate embeddings for entities related to a document"""
    conn = embedder.get_connection()
    cursor = conn.cursor()
    
    # Get entities related to this document
    unified_id = f"{doc_type}_{doc_id}"
    cursor.execute("""
        SELECT DISTINCT target_type, target_id 
        FROM relationships
        WHERE source_type = 'document' AND source_id = ?
    """, (unified_id,))
    
    entities = cursor.fetchall()
    conn.close()
    
    count = 0
    for entity_type, entity_id in entities:
        entity_str_id = f"{entity_type}_{entity_id}"
        
        # Check if embedding already exists
        conn = embedder.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM embeddings 
            WHERE entity_type = ? AND entity_id = ?
        """, (entity_type, entity_str_id))
        
        exists = cursor.fetchone()
        conn.close()
        
        if not exists:
            text = embedder.prepare_entity_text(entity_type, int(entity_id))
            if text:
                embedding = embedder.generate_embedding(text)
                embedder.store_embedding(entity_type, entity_str_id, embedding)
                count += 1
    
    return count


def update_database(db_path: str, academic_dir: Path, personal_dir: Path,
                   skip_embeddings: bool = False, skip_graph: bool = False, skip_deduplication: bool = False):
    """Update database with new documents only"""
    
    print("\n" + "="*60)
    print("UPDATING DATABASE WITH NEW DOCUMENTS")
    print("="*60)
    
    # Initialize components
    populator = UnifiedMetadataPopulator(db_path)
    chunker = DocumentChunker(chunk_size=1200, chunk_overlap=200)
    
    # Track statistics
    total_new_docs = 0
    total_new_chunks = 0
    total_new_mappings = 0
    total_new_embeddings = 0
    
    # Process academic documents
    print("\nChecking for new academic documents...")
    existing_academic = get_existing_files(db_path, 'academic')
    new_academic_files = find_new_metadata_files(academic_dir, existing_academic)
    
    if new_academic_files:
        print(f"Found {len(new_academic_files)} new academic documents")
        
        for json_file in new_academic_files:
            doc_id = populator.populate_from_json(json_file, 'academic')
            if doc_id:
                print(f"  ✓ Imported: {json_file.name}")
                total_new_docs += 1
                
                # Create chunks
                chunks, mappings = update_document_chunks(db_path, doc_id, 'academic', chunker)
                total_new_chunks += chunks
                total_new_mappings += mappings
                
                # Generate embeddings
                if not skip_embeddings:
                    try:
                        embedder = EmbeddingGenerator(db_path)
                        emb_count = update_document_embeddings(embedder, doc_id, 'academic')
                        emb_count += update_entity_embeddings(embedder, doc_id, 'academic')
                        total_new_embeddings += emb_count
                    except Exception as e:
                        print(f"    ⚠️  Warning: Could not generate embeddings: {e}")
    else:
        print("No new academic documents found")
    
    # Process personal notes
    print("\nChecking for new personal notes...")
    existing_chronicle = get_existing_files(db_path, 'chronicle')
    new_chronicle_files = find_new_metadata_files(personal_dir, existing_chronicle)
    
    if new_chronicle_files:
        print(f"Found {len(new_chronicle_files)} new personal notes")
        
        for json_file in new_chronicle_files:
            doc_id = populator.populate_from_json(json_file, 'chronicle')
            if doc_id:
                print(f"  ✓ Imported: {json_file.name}")
                total_new_docs += 1
                
                # Create chunks
                chunks, mappings = update_document_chunks(db_path, doc_id, 'chronicle', chunker)
                total_new_chunks += chunks
                total_new_mappings += mappings
                
                # Generate embeddings
                if not skip_embeddings:
                    try:
                        embedder = EmbeddingGenerator(db_path)
                        emb_count = update_document_embeddings(embedder, doc_id, 'chronicle')
                        emb_count += update_entity_embeddings(embedder, doc_id, 'chronicle')
                        total_new_embeddings += emb_count
                    except Exception as e:
                        print(f"    ⚠️  Warning: Could not generate embeddings: {e}")
    else:
        print("No new personal notes found")
    
    # Check and regenerate embeddings if using old model
    if not skip_embeddings:
        print("\nChecking embedding model version...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if we have embeddings with the old model
        cursor.execute("""
            SELECT DISTINCT model_name FROM embeddings
        """)
        models = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if 'text-embedding-3-small' in models:
            print("Found embeddings with old model (text-embedding-3-small)")
            print("Regenerating ALL embeddings with new model (text-embedding-3-large)...")
            
            try:
                # Delete old embeddings
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM embeddings WHERE model_name = 'text-embedding-3-small'")
                conn.commit()
                conn.close()
                
                # Regenerate all embeddings
                embedder = EmbeddingGenerator(db_path)
                doc_count = embedder.generate_document_embeddings()
                chunk_count = embedder.generate_chunk_embeddings()
                entity_count = embedder.generate_entity_embeddings()
                
                total_new_embeddings += doc_count + chunk_count + entity_count
                print(f"✓ Regenerated {doc_count} document, {chunk_count} chunk, and {entity_count} entity embeddings")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not regenerate embeddings: {e}")
    
    # Run deduplication if there are new documents or entities
    if not skip_deduplication and total_new_docs > 0:
        print("\nRunning entity deduplication...")
        try:
            # Import here to avoid circular dependencies
            sys.path.append(str(Path(__file__).parent.parent))
            from agents.entity_deduplicator import EntityDeduplicator
            
            deduplicator = EntityDeduplicator(db_path)
            
            # First ensure entity embeddings exist
            if not skip_embeddings:
                print("  Ensuring entity embeddings are up to date...")
                embedder = EmbeddingGenerator(db_path)
                entity_count = embedder.generate_entity_embeddings()
                if entity_count > 0:
                    print(f"  ✓ Generated {entity_count} entity embeddings")
            
            # Run deduplication
            print("  Running deduplication with 20 parallel workers...")
            deduplicator.deduplicate_all(dry_run=False, use_clustering=True, parallel_workers=20)
            print("✓ Entity deduplication complete")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not deduplicate entities: {e}")
            print("   You can run deduplication manually with:")
            print("   python agents/entity_deduplicator.py --parallel-workers 20 --merge")
    
    # Update graph tables if needed
    if not skip_graph and (total_new_docs > 0 or not skip_deduplication):
        print("\nUpdating knowledge graph...")
        try:
            from DB.populate_graph_tables import populate_graph_tables
            populate_graph_tables(db_path)
            print("✓ Graph tables updated")
        except Exception as e:
            print(f"⚠️  Warning: Could not update graph tables: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("UPDATE SUMMARY")
    print("="*60)
    
    if total_new_docs > 0:
        print(f"✓ Processed {total_new_docs} new documents")
        print(f"✓ Created {total_new_chunks} chunks")
        print(f"✓ Created {total_new_mappings} entity-chunk mappings")
        if not skip_embeddings:
            print(f"✓ Generated {total_new_embeddings} embeddings")
    else:
        print("No new documents to process - database is up to date!")
    
    # Print current statistics
    print("\nCurrent Database Statistics:")
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
        ('document_chunks', 'Document Chunks'),
        ('embeddings', 'Embeddings')
    ]
    
    for table, name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        stats.append((name, count))
    
    conn.close()
    
    for name, count in stats:
        print(f"{name:.<30} {count:>6}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Update database with new documents')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (in DB folder)')
    parser.add_argument('--academic-dir', type=Path, 
                       default=Path("../raw_data/academic/extracted_metadata"),
                       help='Directory with academic metadata JSONs')
    parser.add_argument('--personal-dir', type=Path,
                       default=Path("../raw_data/personal_notes/extracted_metadata"),
                       help='Directory with personal notes metadata JSONs')
    parser.add_argument('--skip-embeddings', action='store_true',
                       help='Skip embedding generation')
    parser.add_argument('--skip-graph', action='store_true',
                       help='Skip graph table update')
    parser.add_argument('--no-deduplication', action='store_true',
                       help='Skip entity deduplication')
    
    args = parser.parse_args()
    
    # Ensure we're working in the DB directory
    db_path = Path(__file__).parent / args.db
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run build_database.py first to create the database")
        return 1
    
    # Update database
    update_database(str(db_path), args.academic_dir, args.personal_dir,
                   args.skip_embeddings, args.skip_graph, args.no_deduplication)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())