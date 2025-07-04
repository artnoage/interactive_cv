#!/usr/bin/env python3
"""
Verify database entities before deduplication.
Shows statistics, samples, and potential duplicates.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import difflib
from collections import defaultdict


def get_connection(db_path: str) -> sqlite3.Connection:
    """Get database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_entity_statistics(db_path: str) -> Dict[str, int]:
    """Get counts for each entity type."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    stats = {}
    tables = [
        ('topics', 'Topics'),
        ('people', 'People'),
        ('projects', 'Projects'),
        ('institutions', 'Institutions'),
        ('methods', 'Methods'),
        ('applications', 'Applications')
    ]
    
    for table, label in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[label] = cursor.fetchone()[0]
    
    conn.close()
    return stats


def find_exact_duplicates(db_path: str) -> Dict[str, List[Tuple[str, int]]]:
    """Find exact duplicates (case-insensitive)."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    duplicates = {}
    tables = ['topics', 'people', 'projects', 'institutions', 'methods', 'applications']
    
    for table in tables:
        cursor.execute(f"""
            SELECT LOWER(name) as lower_name, COUNT(*) as cnt, 
                   GROUP_CONCAT(name || ' (id:' || id || ')', ' | ') as items
            FROM {table}
            GROUP BY LOWER(name)
            HAVING cnt > 1
            ORDER BY cnt DESC
        """)
        
        table_dups = []
        for row in cursor.fetchall():
            table_dups.append((row['items'], row['cnt']))
        
        if table_dups:
            duplicates[table] = table_dups
    
    conn.close()
    return duplicates


def find_similar_entities(db_path: str, table: str, threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    """Find similar entities using string similarity."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Get all entities
    cursor.execute(f"SELECT id, name FROM {table} ORDER BY name")
    entities = [(row['id'], row['name']) for row in cursor.fetchall()]
    
    similar = []
    
    # Compare each pair
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            id1, name1 = entities[i]
            id2, name2 = entities[j]
            
            # Calculate similarity
            ratio = difflib.SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
            
            if ratio >= threshold and ratio < 1.0:  # Exclude exact matches
                similar.append((f"{name1} (id:{id1})", f"{name2} (id:{id2})", ratio))
    
    conn.close()
    return sorted(similar, key=lambda x: x[2], reverse=True)


def get_entity_samples(db_path: str, table: str, limit: int = 10) -> List[Dict]:
    """Get random sample of entities."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Get random samples
    cursor.execute(f"""
        SELECT * FROM {table}
        ORDER BY RANDOM()
        LIMIT ?
    """, (limit,))
    
    samples = []
    for row in cursor.fetchall():
        sample = {}
        for col in columns:
            if row[col] is not None:
                sample[col] = row[col]
        samples.append(sample)
    
    conn.close()
    return samples


def check_long_entities(db_path: str, max_length: int = 50) -> Dict[str, List[str]]:
    """Find entities with unusually long names."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    long_entities = {}
    tables = ['topics', 'people', 'projects', 'institutions', 'methods', 'applications']
    
    for table in tables:
        cursor.execute(f"""
            SELECT name FROM {table}
            WHERE LENGTH(name) > ?
            ORDER BY LENGTH(name) DESC
            LIMIT 10
        """, (max_length,))
        
        long_names = [row['name'] for row in cursor.fetchall()]
        if long_names:
            long_entities[table] = long_names
    
    conn.close()
    return long_entities


def verify_database(db_path: str) -> bool:
    """Run comprehensive database verification."""
    print("\n" + "="*70)
    print("DATABASE ENTITY VERIFICATION")
    print("="*70)
    
    # 1. Entity Statistics
    print("\n1. ENTITY STATISTICS")
    print("-" * 40)
    stats = get_entity_statistics(db_path)
    total = 0
    for entity_type, count in stats.items():
        print(f"{entity_type:.<20} {count:>6}")
        total += count
    print(f"{'TOTAL':.<20} {total:>6}")
    
    # 2. Exact Duplicates
    print("\n\n2. EXACT DUPLICATES (case-insensitive)")
    print("-" * 40)
    duplicates = find_exact_duplicates(db_path)
    if duplicates:
        for table, dups in duplicates.items():
            print(f"\n{table.upper()}:")
            for items, count in dups[:5]:  # Show top 5
                print(f"  {count}x: {items}")
    else:
        print("No exact duplicates found!")
    
    # 3. Similar Entities
    print("\n\n3. SIMILAR ENTITIES (fuzzy matching)")
    print("-" * 40)
    tables_to_check = ['topics', 'people', 'methods']
    for table in tables_to_check:
        similar = find_similar_entities(db_path, table, threshold=0.75)
        if similar:
            print(f"\n{table.upper()} (showing top 5):")
            for name1, name2, score in similar[:5]:
                print(f"  {score:.2f}: {name1} <-> {name2}")
    
    # 4. Long Entity Names
    print("\n\n4. SUSPICIOUSLY LONG ENTITY NAMES")
    print("-" * 40)
    long_entities = check_long_entities(db_path, max_length=60)
    if long_entities:
        for table, names in long_entities.items():
            print(f"\n{table.upper()}:")
            for name in names[:3]:  # Show top 3
                print(f"  [{len(name)} chars] {name[:80]}...")
    else:
        print("No suspiciously long names found!")
    
    # 5. Sample Entities
    print("\n\n5. RANDOM ENTITY SAMPLES")
    print("-" * 40)
    tables = ['topics', 'people', 'projects']
    for table in tables:
        samples = get_entity_samples(db_path, table, limit=5)
        print(f"\n{table.upper()} (5 random samples):")
        for sample in samples:
            name = sample.get('name', 'N/A')
            attrs = []
            for key, val in sample.items():
                if key not in ['id', 'name', 'created_at'] and val:
                    attrs.append(f"{key}={val}")
            attr_str = f" ({', '.join(attrs)})" if attrs else ""
            print(f"  - {name}{attr_str}")
    
    # Ask for confirmation
    print("\n" + "="*70)
    response = input("\nDoes the database look correct? (y/n): ")
    return response.lower() == 'y'


def export_duplicate_report(db_path: str, output_file: str = "duplicate_report.txt"):
    """Export detailed duplicate report to file."""
    with open(output_file, 'w') as f:
        f.write("ENTITY DUPLICATE REPORT\n")
        f.write("="*70 + "\n\n")
        
        # Exact duplicates
        f.write("EXACT DUPLICATES\n")
        f.write("-"*40 + "\n")
        duplicates = find_exact_duplicates(db_path)
        for table, dups in duplicates.items():
            f.write(f"\n{table.upper()}:\n")
            for items, count in dups:
                f.write(f"  {count}x: {items}\n")
        
        # Similar entities
        f.write("\n\nSIMILAR ENTITIES\n")
        f.write("-"*40 + "\n")
        tables = ['topics', 'people', 'projects', 'methods', 'institutions', 'applications']
        for table in tables:
            similar = find_similar_entities(db_path, table, threshold=0.7)
            if similar:
                f.write(f"\n{table.upper()}:\n")
                for name1, name2, score in similar:
                    f.write(f"  {score:.3f}: {name1} <-> {name2}\n")
    
    print(f"\nDuplicate report exported to: {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify database entities')
    parser.add_argument('--db', default="metadata.db", 
                       help='Database filename (in DB folder)')
    parser.add_argument('--export', action='store_true',
                       help='Export duplicate report to file')
    
    args = parser.parse_args()
    
    # Ensure we're working in the DB directory
    db_path = Path(__file__).parent / args.db
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return 1
    
    try:
        if args.export:
            export_duplicate_report(str(db_path))
        else:
            result = verify_database(str(db_path))
            if not result:
                print("\nVerification failed or cancelled by user")
                return 1
            print("\nDatabase verified successfully!")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())