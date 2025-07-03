#!/usr/bin/env python3
"""
Populate the graph_nodes and graph_edges tables from existing data
"""

import sqlite3
from typing import Dict, Set, Tuple
import json


def populate_graph_tables(db_path: str = "DB/metadata.db"):
    """Populate graph tables from existing entities and relationships"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Clear existing graph data
        cursor.execute("DELETE FROM graph_edges")
        cursor.execute("DELETE FROM graph_nodes")
        
        print("Building graph nodes...")
        
        # Create nodes for all documents
        cursor.execute("""
            INSERT INTO graph_nodes (node_id, node_type, node_label, attributes)
            SELECT 
                'academic_' || id,
                'academic_document',
                title,
                json_object('date', date, 'domain', domain)
            FROM academic_documents
        """)
        
        cursor.execute("""
            INSERT INTO graph_nodes (node_id, node_type, node_label, attributes)
            SELECT 
                'chronicle_' || id,
                'chronicle_document',
                title,
                json_object('date', date, 'note_type', note_type)
            FROM chronicle_documents
        """)
        
        # Create nodes for all entities
        entity_tables = [
            ('topics', 'topic', 'category'),
            ('people', 'person', 'role'),
            ('projects', 'project', 'description'),
            ('institutions', 'institution', 'type'),
            ('methods', 'method', 'category'),
            ('applications', 'application', 'domain')
        ]
        
        for table, node_type, attr_field in entity_tables:
            cursor.execute(f"""
                INSERT INTO graph_nodes (node_id, node_type, node_label, attributes)
                SELECT 
                    '{node_type}_' || id,
                    '{node_type}',
                    name,
                    CASE 
                        WHEN {attr_field} IS NOT NULL 
                        THEN json_object('description', {attr_field})
                        ELSE '{{}}'
                    END
                FROM {table}
            """)
        
        print("Building graph edges...")
        
        # Create edges from relationships
        cursor.execute("""
            INSERT INTO graph_edges (source_node_id, target_node_id, edge_type, weight, attributes)
            SELECT 
                source_type || '_' || source_id,
                target_type || '_' || target_id,
                relationship_type,
                confidence,
                COALESCE(metadata, '{}')
            FROM relationships
            WHERE (source_type || '_' || source_id) IN (SELECT node_id FROM graph_nodes)
            AND (target_type || '_' || target_id) IN (SELECT node_id FROM graph_nodes)
        """)
        
        # Add topic-to-topic relationships based on co-occurrence
        cursor.execute("""
            INSERT OR IGNORE INTO graph_edges (source_node_id, target_node_id, edge_type, weight)
            SELECT DISTINCT
                'topic_' || r1.target_id,
                'topic_' || r2.target_id,
                'related_to',
                COUNT(*) * 0.1  -- Weight based on co-occurrence frequency
            FROM relationships r1
            JOIN relationships r2 ON r1.source_id = r2.source_id 
                AND r1.source_type = r2.source_type
                AND r1.target_id < r2.target_id  -- Avoid duplicates
            WHERE r1.target_type = 'topic' AND r2.target_type = 'topic'
                AND r1.source_type = 'document'
            GROUP BY r1.target_id, r2.target_id
            HAVING COUNT(*) > 1  -- Only if co-occur more than once
        """)
        
        # Add person-to-person collaboration edges
        cursor.execute("""
            INSERT OR IGNORE INTO graph_edges (source_node_id, target_node_id, edge_type, weight)
            SELECT DISTINCT
                'person_' || r1.target_id,
                'person_' || r2.target_id,
                'collaborates_with',
                COUNT(*) * 0.2
            FROM relationships r1
            JOIN relationships r2 ON r1.source_id = r2.source_id 
                AND r1.source_type = r2.source_type
                AND r1.target_id < r2.target_id
            WHERE r1.target_type = 'person' AND r2.target_type = 'person'
                AND r1.source_type = 'document'
            GROUP BY r1.target_id, r2.target_id
        """)
        
        conn.commit()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM graph_nodes")
        node_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM graph_edges")
        edge_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT node_type, COUNT(*) FROM graph_nodes GROUP BY node_type")
        node_types = cursor.fetchall()
        
        cursor.execute("SELECT edge_type, COUNT(*) FROM graph_edges GROUP BY edge_type")
        edge_types = cursor.fetchall()
        
        print(f"\n✓ Created {node_count} nodes and {edge_count} edges")
        
        print("\nNode distribution:")
        for node_type, count in node_types:
            print(f"  {node_type}: {count}")
        
        print("\nEdge distribution:")
        for edge_type, count in edge_types:
            print(f"  {edge_type}: {count}")
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "DB/metadata.db"
    populate_graph_tables(db_path)