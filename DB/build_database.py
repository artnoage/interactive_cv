#!/usr/bin/env python3
"""
Database builder
Uses configuration blueprints to build database from scratch
"""

import sqlite3
import sys
from pathlib import Path
import argparse
import shutil
from datetime import datetime

# Add parent and blueprints to path for imports
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "blueprints" / "core"))

from blueprint_loader import get_blueprint_loader
from DB.populator import DatabasePopulator
from DB.chunker import DocumentChunker
from DB.embeddings import EmbeddingGenerator
from KG.graph_builder import GraphBuilder


def create_database_schema(db_path: str):
    """Create database schema from blueprint configuration"""
    
    blueprint_loader = get_blueprint_loader()
    schema_config = blueprint_loader.get_database_schema()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Creating database schema from blueprints...")
        
        # Create document tables
        document_tables = schema_config.get('document_tables', {})
        for table_name, table_config in document_tables.items():
            columns = []
            for col_name, col_config in table_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('unique'):
                    col_def += " UNIQUE"
                if col_config.get('default'):
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT '{default_val}'"
                
                columns.append(col_def)
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: {table_name}")
        
        # Create entity tables
        entity_tables = schema_config.get('entity_tables', {})
        for table_name, table_config in entity_tables.items():
            columns = []
            for col_name, col_config in table_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('unique'):
                    col_def += " UNIQUE"
                if col_config.get('default'):
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT '{default_val}'"
                
                columns.append(col_def)
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: {table_name}")
        
        # Create relationship table
        relationships_config = schema_config.get('relationship_table', {}).get('relationships', {})
        if relationships_config:
            columns = []
            for col_name, col_config in relationships_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('default') is not None:
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT {default_val}"
                
                columns.append(col_def)
            
            # Add unique constraint
            constraints = relationships_config.get('constraints', {})
            for constraint_name, constraint_config in constraints.items():
                if constraint_config['type'] == 'UNIQUE':
                    constraint_cols = ', '.join(constraint_config['columns'])
                    columns.append(f"UNIQUE({constraint_cols})")
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS relationships (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: relationships")
        
        # Create processing tables
        processing_tables = schema_config.get('processing_tables', {})
        for table_name, table_config in processing_tables.items():
            columns = []
            for col_name, col_config in table_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('default'):
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT {default_val}"
                
                columns.append(col_def)
            
            # Add constraints
            constraints = table_config.get('constraints', {})
            for constraint_name, constraint_config in constraints.items():
                if constraint_config['type'] == 'UNIQUE':
                    constraint_cols = ', '.join(constraint_config['columns'])
                    columns.append(f"UNIQUE({constraint_cols})")
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: {table_name}")
        
        # Create vector tables
        vector_tables = schema_config.get('vector_tables', {})
        for table_name, table_config in vector_tables.items():
            columns = []
            for col_name, col_config in table_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('unique'):
                    col_def += " UNIQUE"
                if col_config.get('default'):
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT {default_val}"
                
                columns.append(col_def)
            
            # Add constraints
            constraints = table_config.get('constraints', {})
            for constraint_name, constraint_config in constraints.items():
                if constraint_config['type'] == 'UNIQUE':
                    constraint_cols = ', '.join(constraint_config['columns'])
                    columns.append(f"UNIQUE({constraint_cols})")
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: {table_name}")
        
        # Create metadata tables
        metadata_tables = schema_config.get('metadata_tables', {})
        for table_name, table_config in metadata_tables.items():
            columns = []
            for col_name, col_config in table_config['columns'].items():
                col_def = f"{col_name} {col_config['type']}"
                
                if col_config.get('primary_key'):
                    col_def += " PRIMARY KEY"
                if col_config.get('auto_increment'):
                    col_def += " AUTOINCREMENT"
                if col_config.get('not_null'):
                    col_def += " NOT NULL"
                if col_config.get('default'):
                    default_val = col_config['default']
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT '{default_val}'"
                
                columns.append(col_def)
            
            columns_str = ',\n    '.join(columns)
            create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n)"
            cursor.execute(create_sql)
            print(f"  ✓ Created table: {table_name}")
        
        # Create indexes
        indexes = schema_config.get('indexes', {})
        for index_name, index_config in indexes.items():
            table = index_config['table']
            columns = ', '.join(index_config['columns'])
            create_index_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({columns})"
            cursor.execute(create_index_sql)
            print(f"  ✓ Created index: {index_name}")
        
        conn.commit()
        print("✓ Database schema created successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error creating schema: {e}")
        raise
    finally:
        conn.close()


def build_database(db_path: str, skip_embeddings: bool = False, skip_graph: bool = False, 
                  skip_deduplication: bool = False):
    """Build complete database using blueprint-driven components"""
    
    blueprint_loader = get_blueprint_loader()
    
    print("\n" + "="*60)
    print("BLUEPRINT-DRIVEN DATABASE BUILD")
    print("="*60)
    
    # Step 1: Populate from metadata using blueprints
    print("\nStep 1: Importing metadata (blueprint-driven)")
    print("-" * 50)
    
    populator = DatabasePopulator(db_path)
    
    # Process all document types found in blueprints
    total_docs = 0
    for doc_type in blueprint_loader.list_document_types():
        metadata_dir = Path(f"raw_data/{doc_type}/extracted_metadata")
        if doc_type == 'personal':
            metadata_dir = Path("raw_data/personal_notes/extracted_metadata")
        
        if metadata_dir.exists():
            print(f"\nProcessing {doc_type} metadata from {metadata_dir}")
            doc_ids = populator.populate_directory(metadata_dir, doc_type)
            total_docs += len(doc_ids)
            print(f"✓ Imported {len(doc_ids)} {doc_type} documents")
    
    print(f"\n✓ Total documents imported: {total_docs}")
    
    # Step 2: Create document chunks
    print("\nStep 2: Creating document chunks")
    print("-" * 40)
    
    chunker = DocumentChunker(chunk_size=1200, chunk_overlap=200)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    total_chunks = 0
    total_mappings = 0
    
    # Chunk all document types
    for doc_type in blueprint_loader.list_document_types():
        document_mapping = blueprint_loader.get_document_mapping(doc_type)
        table = document_mapping.get('table')
        
        if table:
            cursor.execute(f"SELECT id, content FROM {table} WHERE content IS NOT NULL")
            docs = cursor.fetchall()
            
            doc_chunks = 0
            doc_mappings = 0
            
            for doc_id, content in docs:
                chunk_ids = chunker.chunk_and_store(db_path, doc_id, doc_type, content)
                mappings = chunker.map_entities_to_chunks(db_path, doc_id, doc_type)
                doc_chunks += len(chunk_ids)
                doc_mappings += mappings
            
            total_chunks += doc_chunks
            total_mappings += doc_mappings
            print(f"✓ {doc_type.title()}: {len(docs)} documents → {doc_chunks} chunks")
    
    print(f"✓ Total entity-chunk mappings: {total_mappings}")
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
    
    # Step 4: Entity deduplication
    if not skip_deduplication:
        print("\nStep 4: Entity deduplication")
        print("-" * 40)
        print("  Ensuring entity embeddings are generated...")
        print("  Running deduplication with blueprint-driven entities...")
        
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "../agents/entity_deduplicator.py", 
                "--parallel-workers", "20", "--merge"
            ], cwd="DB", capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Entity deduplication completed")
                print(result.stdout.split('\n')[-5:])  # Show last few lines
            else:
                print("⚠️  Deduplication encountered issues")
                print(result.stderr[:500])  # Show first part of error
        except Exception as e:
            print(f"⚠️  Could not run deduplication: {e}")
    
    # Step 5: Generate knowledge graph
    if not skip_graph:
        print("\nStep 5: Generating blueprint-driven knowledge graph")
        print("-" * 50)
        
        try:
            graph_builder = GraphBuilder(db_path)
            graph_data = graph_builder.export_graph("KG/knowledge_graph.json")
            
            print(f"✓ Generated knowledge graph:")
            print(f"  - Nodes: {graph_data['metadata']['total_nodes']}")
            print(f"  - Edges: {graph_data['metadata']['total_edges']}")
            print(f"  - Node types: {len(graph_data['metadata']['node_types'])}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not generate knowledge graph: {e}")


def print_database_stats(db_path: str):
    """Print database statistics"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get blueprint configuration for table list
    blueprint_loader = get_blueprint_loader()
    schema_config = blueprint_loader.get_database_schema()
    
    print("\nDatabase Statistics:")
    
    # Document tables
    doc_tables = schema_config.get('document_tables', {})
    for table_name, table_config in doc_tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        description = table_config.get('description', table_name)
        print(f"{description:.<30} {count:>6}")
    
    # Entity tables
    entity_tables = schema_config.get('entity_tables', {})
    for table_name, table_config in entity_tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        description = table_config.get('description', table_name)
        print(f"{description:.<30} {count:>6}")
    
    # Other important tables
    other_tables = ['relationships', 'document_chunks', 'chunk_entities', 'embeddings']
    for table in other_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:.<30} {count:>6}")
        except:
            pass
    
    conn.close()


def main():
    """Main entry point for blueprint-driven database builder"""
    parser = argparse.ArgumentParser(description='Build database using blueprint system')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (will be created in DB folder)')
    parser.add_argument('--backup', action='store_true', 
                       help='Backup existing database before rebuilding')
    parser.add_argument('--skip-embeddings', action='store_true',
                       help='Skip embedding generation')
    parser.add_argument('--skip-graph', action='store_true',
                       help='Skip knowledge graph generation')
    parser.add_argument('--no-deduplication', action='store_true',
                       help='Skip entity deduplication')
    parser.add_argument('--validate-blueprints', action='store_true',
                       help='Validate blueprint configurations before building')
    
    args = parser.parse_args()
    
    # Validate blueprints if requested
    if args.validate_blueprints:
        blueprint_loader = get_blueprint_loader()
        errors = blueprint_loader.validate_blueprints()
        if errors:
            print("Blueprint validation errors:")
            for blueprint, error_list in errors.items():
                print(f"  {blueprint}: {error_list}")
            return 1
        else:
            print("✓ All blueprints are valid!")
    
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
    
    # Create database with blueprint-driven schema
    print(f"✓ Creating new database: {db_path}")
    create_database_schema(str(db_path))
    
    # Build database using blueprint system
    build_database(str(db_path), args.skip_embeddings, args.skip_graph, args.no_deduplication)
    
    # Print statistics
    print_database_stats(str(db_path))
    
    print("\n" + "="*60)
    print("BLUEPRINT-DRIVEN BUILD COMPLETE")
    print("="*60)
    print("Next steps:")
    print("1. View database: cd .. && ./view_database.sh")
    print("2. Test graph: open web_ui/index.html")
    print("3. Test queries: python ../interactive_agent.py")
    print("\nBlueprint system features:")
    print("- All domain knowledge externalized to YAML blueprints")
    print("- Database schema generated from core/database_schema.yaml")
    print("- Entity mappings defined in academic/personal blueprints")
    print("- Visualization rules in core/visualization.yaml")


if __name__ == "__main__":
    main()