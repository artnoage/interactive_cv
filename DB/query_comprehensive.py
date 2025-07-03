#!/usr/bin/env python3
"""Comprehensive query of the v2 metadata database."""

import sqlite3
import json
from pathlib import Path
from collections import defaultdict

def format_json_field(field_value):
    """Format JSON field for display."""
    if field_value:
        try:
            data = json.loads(field_value)
            if isinstance(data, list):
                return ', '.join(data[:3]) + ('...' if len(data) > 3 else '')
            elif isinstance(data, dict):
                return str(data)
            else:
                return str(data)
        except:
            return str(field_value)
    return None

def main():
    db_path = "DB/metadata.db"
    
    if not Path(db_path).exists():
        print(f"Error: Database {db_path} not found")
        return
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("="*80)
    print("INTERACTIVE CV DATABASE SUMMARY (V2 Schema)")
    print("="*80)
    
    try:
        # Document counts by type
        print("\n📚 DOCUMENTS BY TYPE:")
        cursor.execute("SELECT COUNT(*) as count FROM chronicle_documents")
        chronicle_count = cursor.fetchone()['count']
        print(f"  - Chronicle: {chronicle_count} documents")
        
        cursor.execute("SELECT COUNT(*) as count FROM academic_documents")
        academic_count = cursor.fetchone()['count']
        print(f"  - Academic: {academic_count} documents")
        
        # Total unique entities
        print(f"\n🏷️  UNIQUE ENTITIES:")
        
        entity_tables = [
            ('topics', 'Topics'),
            ('people', 'People'),
            ('projects', 'Projects'),
            ('institutions', 'Institutions'),
            ('methods', 'Methods'),
            ('applications', 'Applications')
        ]
        
        for table, label in entity_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"  - {label}: {count}")
            except sqlite3.OperationalError:
                pass  # Table doesn't exist
        
        # Academic papers with details
        print("\n🎓 ACADEMIC PAPERS:")
        cursor.execute("""
            SELECT title, date, domain, document_type
            FROM academic_documents 
            ORDER BY date DESC, title
        """)
        for i, row in enumerate(cursor.fetchall(), 1):
            domain = f" [{row['domain']}]" if row['domain'] else ""
            doc_type = f" ({row['document_type']})" if row['document_type'] else ""
            print(f"  {i}. {row['title']}{domain}{doc_type}")
        
        # Top research topics using relationships table
        print("\n🔬 TOP RESEARCH TOPICS:")
        cursor.execute("""
            SELECT t.name, t.category, COUNT(DISTINCT r.source_id) as doc_count
            FROM topics t
            JOIN relationships r ON r.target_type = 'topic' AND r.target_id = t.id
            WHERE r.source_type = 'document'
            GROUP BY t.id
            ORDER BY doc_count DESC
            LIMIT 15
        """)
        for row in cursor.fetchall():
            category = f" ({row['category']})" if row['category'] else ""
            print(f"  - {row['name']}{category}: {row['doc_count']} documents")
        
        # Projects with status
        print("\n💼 PROJECTS:")
        cursor.execute("""
            SELECT p.name, p.status, p.project_type, 
                   COUNT(DISTINCT r.source_id) as mentions
            FROM projects p
            LEFT JOIN relationships r ON r.target_type = 'project' AND r.target_id = p.id
            WHERE r.source_type = 'document' OR r.source_id IS NULL
            GROUP BY p.id
            ORDER BY mentions DESC
        """)
        for row in cursor.fetchall():
            status = f" [{row['status']}]" if row['status'] else ""
            ptype = f" ({row['project_type']})" if row['project_type'] else ""
            print(f"  - {row['name']}{status}{ptype}: {row['mentions']} mentions")
        
        # Recent chronicle activity
        print("\n📅 RECENT CHRONICLE ACTIVITY:")
        cursor.execute("""
            SELECT date, title, note_type
            FROM chronicle_documents 
            ORDER BY date DESC
            LIMIT 10
        """)
        for row in cursor.fetchall():
            note_type = f" ({row['note_type']})" if row['note_type'] else ""
            print(f"  - {row['date']}: {row['title']}{note_type}")
        
        # People and their affiliations
        print("\n👥 PEOPLE & COLLABORATORS:")
        cursor.execute("""
            SELECT p.name, p.affiliation, p.role,
                   COUNT(DISTINCT r.source_id) as mentions
            FROM people p
            LEFT JOIN relationships r ON r.target_type = 'person' AND r.target_id = p.id
            WHERE r.source_type = 'document' OR r.source_id IS NULL
            GROUP BY p.id
            ORDER BY mentions DESC
            LIMIT 10
        """)
        for row in cursor.fetchall():
            affiliation = f" @ {row['affiliation']}" if row['affiliation'] else ""
            role = f" ({row['role']})" if row['role'] else ""
            print(f"  - {row['name']}{role}{affiliation}: {row['mentions']} mentions")
        
        # Institutions
        print("\n🏛️  INSTITUTIONS:")
        cursor.execute("""
            SELECT i.name, i.type, i.location,
                   COUNT(DISTINCT r.source_id) as doc_count
            FROM institutions i
            LEFT JOIN relationships r ON r.target_type = 'institution' AND r.target_id = i.id
            WHERE r.source_type = 'document' OR r.source_id IS NULL
            GROUP BY i.id
            ORDER BY doc_count DESC
        """)
        for row in cursor.fetchall():
            itype = f" ({row['type']})" if row['type'] else ""
            location = f" - {row['location']}" if row['location'] else ""
            print(f"  - {row['name']}{itype}{location}: {row['doc_count']} documents")
        
        # Methods and algorithms
        print("\n⚙️  METHODS & ALGORITHMS:")
        cursor.execute("""
            SELECT m.name, m.category, 
                   COUNT(DISTINCT r.source_id) as usage_count
            FROM methods m
            LEFT JOIN relationships r ON r.target_type = 'method' AND r.target_id = m.id
            WHERE r.source_type = 'document' OR r.source_id IS NULL
            GROUP BY m.id
            ORDER BY usage_count DESC
            LIMIT 10
        """)
        for row in cursor.fetchall():
            category = f" ({row['category']})" if row['category'] else ""
            print(f"  - {row['name']}{category}: {row['usage_count']} documents")
        
        # Cross-domain connections
        print("\n🔗 CROSS-DOMAIN CONNECTIONS:")
        
        # Topics in both academic and chronicle
        cursor.execute("""
            WITH academic_topics AS (
                SELECT DISTINCT t.id, t.name
                FROM topics t
                JOIN relationships r ON r.target_type = 'topic' AND r.target_id = t.id
                WHERE r.source_type = 'document' 
                  AND r.source_id LIKE 'academic_%'
            ),
            chronicle_topics AS (
                SELECT DISTINCT t.id, t.name
                FROM topics t
                JOIN relationships r ON r.target_type = 'topic' AND r.target_id = t.id
                WHERE r.source_type = 'document' 
                  AND r.source_id LIKE 'chronicle_%'
            )
            SELECT at.name
            FROM academic_topics at
            INNER JOIN chronicle_topics ct ON at.id = ct.id
            LIMIT 10
        """)
        shared_topics = cursor.fetchall()
        if shared_topics:
            print("  Topics in both academic papers and chronicle notes:")
            for row in shared_topics:
                print(f"    - {row['name']}")
        
        # Relationship statistics
        print("\n📊 RELATIONSHIP STATISTICS:")
        cursor.execute("""
            SELECT relationship_type, COUNT(*) as count
            FROM relationships
            GROUP BY relationship_type
            ORDER BY count DESC
        """)
        for row in cursor.fetchall():
            print(f"  - {row['relationship_type']}: {row['count']} connections")
        
        # Graph table status
        print("\n🔍 GRAPH TABLE STATUS:")
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('graph_nodes', 'graph_edges')
        """)
        graph_tables = [row['name'] for row in cursor.fetchall()]
        
        if 'graph_nodes' in graph_tables:
            cursor.execute("SELECT COUNT(*) FROM graph_nodes")
            node_count = cursor.fetchone()[0]
            print(f"  - Graph nodes: {node_count}")
            
            # Top nodes by PageRank
            cursor.execute("""
                SELECT node_id, label, entity_type, pagerank_score
                FROM graph_nodes
                WHERE pagerank_score IS NOT NULL
                ORDER BY pagerank_score DESC
                LIMIT 5
            """)
            top_nodes = cursor.fetchall()
            if top_nodes:
                print("  - Top nodes by PageRank:")
                for row in top_nodes:
                    print(f"    • {row['label']} ({row['entity_type']}): {row['pagerank_score']:.4f}")
        
        if 'graph_edges' in graph_tables:
            cursor.execute("SELECT COUNT(*) FROM graph_edges")
            edge_count = cursor.fetchone()[0]
            print(f"  - Graph edges: {edge_count}")
        
        # Embeddings status
        print("\n🧠 EMBEDDINGS STATUS:")
        for table in ['embeddings', 'embeddings_v2']:
            try:
                cursor.execute(f"""
                    SELECT entity_type, COUNT(*) as count
                    FROM {table}
                    GROUP BY entity_type
                """)
                embeddings = cursor.fetchall()
                if embeddings:
                    print(f"  From {table}:")
                    for row in embeddings:
                        print(f"    - {row['entity_type']}: {row['count']} embeddings")
                break
            except sqlite3.OperationalError:
                continue
        
    except Exception as e:
        print(f"\nError querying database: {e}")
    
    finally:
        conn.close()
    
    print("\n" + "="*80)
    print("✅ V2 Database ready for enhanced RAG queries!")
    print("="*80)


if __name__ == "__main__":
    main()