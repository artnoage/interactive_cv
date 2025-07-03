#!/usr/bin/env python3
"""
Knowledge graph system for v2 database schema.
Uses the unified relationships table and pre-computed graph tables for performance.
"""

import sqlite3
import json
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Set
from abc import ABC, abstractmethod
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Core Knowledge Graph Class (Same as before, database-agnostic)
# ============================================================================

class KnowledgeGraph:
    """A database-agnostic knowledge graph builder."""
    
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_node(self, node_id: str, node_type: str, label: str, **attributes):
        """Add a node to the graph."""
        self.graph.add_node(
            node_id,
            type=node_type,
            label=label,
            **attributes
        )
        
    def add_edge(self, source_id: str, target_id: str, relationship: str, **attributes):
        """Add an edge between two nodes."""
        if self.graph.has_node(source_id) and self.graph.has_node(target_id):
            self.graph.add_edge(
                source_id,
                target_id,
                relationship=relationship,
                **attributes
            )
        else:
            logger.warning(f"Cannot add edge: missing node(s) - {source_id} or {target_id}")
            
    def add_nodes_batch(self, nodes: List[Dict[str, Any]]):
        """Add multiple nodes at once."""
        for node in nodes:
            node_id = node.pop('id')
            node_type = node.pop('type')
            label = node.pop('label')
            self.add_node(node_id, node_type, label, **node)
            
    def add_edges_batch(self, edges: List[Dict[str, Any]]):
        """Add multiple edges at once."""
        for edge in edges:
            source = edge.pop('source')
            target = edge.pop('target')
            relationship = edge.pop('relationship')
            self.add_edge(source, target, relationship, **edge)
            
    def get_graph(self) -> nx.Graph:
        """Get the NetworkX graph object."""
        return self.graph
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        
        stats = {
            'total_nodes': num_nodes,
            'total_edges': num_edges,
            'node_types': {},
            'relationship_types': {},
            'average_degree': (2 * num_edges / num_nodes) if num_nodes > 0 else 0,
            'connected_components': nx.number_connected_components(self.graph)
        }
        
        # Count nodes by type
        for _, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'unknown')
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            
        # Count edges by relationship type
        for _, _, data in self.graph.edges(data=True):
            rel_type = data.get('relationship', 'unknown')
            stats['relationship_types'][rel_type] = stats['relationship_types'].get(rel_type, 0) + 1
            
        # Add PageRank if available
        if num_nodes > 0:
            try:
                pagerank = nx.pagerank(self.graph, alpha=0.85)
                top_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
                stats['top_nodes_by_pagerank'] = [
                    {
                        'id': node_id,
                        'label': self.graph.nodes[node_id].get('label', node_id),
                        'type': self.graph.nodes[node_id].get('type', 'unknown'),
                        'score': score
                    }
                    for node_id, score in top_nodes
                ]
            except:
                pass
                
        return stats
        
    def export_as_json(self, output_path: str):
        """Export graph as JSON in node-link format."""
        data = nx.node_link_data(self.graph, edges="links")
        
        # Add metadata
        data['metadata'] = {
            'version': '2.0',
            'statistics': self.get_statistics()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Graph exported to {output_path}")
        return data


# ============================================================================
# V2 SQL Data Provider
# ============================================================================

class V2SQLProvider:
    """
    SQL provider for the v2 database schema.
    Uses unified relationships table and pre-computed graph tables if available.
    """
    
    def __init__(self, db_path: str, use_precomputed: bool = True):
        self.db_path = db_path
        self.use_precomputed = use_precomputed
        
    def _table_exists(self, conn, table_name: str) -> bool:
        """Check if a table exists in the database."""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    
    def _format_node_id(self, entity_type: str, entity_id: str) -> str:
        """Format node ID consistently."""
        if entity_type == 'document':
            # Document IDs already include type prefix
            return f"doc_{entity_id}"
        else:
            return f"{entity_type}_{entity_id}"
    
    def get_nodes(self) -> List[Dict[str, Any]]:
        """Extract all nodes from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # Check if pre-computed graph_nodes table exists
            if self.use_precomputed and self._table_exists(conn, 'graph_nodes'):
                logger.info("Using pre-computed graph_nodes table")
                return self._get_precomputed_nodes(conn)
            else:
                logger.info("Extracting nodes from entity tables")
                return self._extract_nodes_from_entities(conn)
        finally:
            conn.close()
    
    def _get_precomputed_nodes(self, conn) -> List[Dict[str, Any]]:
        """Get nodes from pre-computed graph_nodes table."""
        nodes = []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT node_id, entity_type, label, attributes, 
                   pagerank_score, degree, community_id
            FROM graph_nodes
            ORDER BY pagerank_score DESC
        """)
        
        for row in cursor.fetchall():
            node = {
                'id': row['node_id'],
                'type': row['entity_type'],
                'label': row['label'],
                'pagerank': row['pagerank_score'],
                'degree': row['degree'],
                'community': row['community_id']
            }
            
            # Add attributes if present
            if row['attributes']:
                try:
                    attrs = json.loads(row['attributes'])
                    node.update(attrs)
                except:
                    pass
                    
            nodes.append(node)
            
        return nodes
    
    def _extract_nodes_from_entities(self, conn) -> List[Dict[str, Any]]:
        """Extract nodes from entity tables."""
        nodes = []
        cursor = conn.cursor()
        
        # Entity table configurations
        entity_configs = [
            # Documents - use unified view
            {
                'query': """
                    SELECT unified_id, doc_type, title, date, file_path 
                    FROM documents
                """,
                'type': 'document',
                'id_field': 'unified_id',
                'label_field': 'title',
                'extra_fields': ['date', 'file_path', 'doc_type']
            },
            # Topics
            {
                'query': "SELECT id, name, category, description FROM topics",
                'type': 'topic',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['category', 'description']
            },
            # People
            {
                'query': "SELECT id, name, affiliation, role, expertise FROM people",
                'type': 'person',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['affiliation', 'role', 'expertise']
            },
            # Projects
            {
                'query': "SELECT id, name, description, status, project_type FROM projects",
                'type': 'project',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['description', 'status', 'project_type']
            },
            # Institutions
            {
                'query': "SELECT id, name, type, location, description FROM institutions",
                'type': 'institution',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['type', 'location', 'description']
            },
            # Methods
            {
                'query': "SELECT id, name, category, description FROM methods",
                'type': 'method',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['category', 'description']
            },
            # Applications
            {
                'query': "SELECT id, name, domain, description, impact_level FROM applications",
                'type': 'application',
                'id_field': 'id',
                'label_field': 'name',
                'extra_fields': ['domain', 'description', 'impact_level']
            }
        ]
        
        for config in entity_configs:
            try:
                cursor.execute(config['query'])
                
                for row in cursor.fetchall():
                    # Format node ID
                    if config['type'] == 'document':
                        node_id = f"doc_{row[config['id_field']]}"
                    else:
                        node_id = f"{config['type']}_{row[config['id_field']]}"
                    
                    node = {
                        'id': node_id,
                        'type': config['type'],
                        'label': row[config['label_field']] or f"{config['type']} {row[config['id_field']]}"
                    }
                    
                    # Add extra fields
                    for field in config['extra_fields']:
                        if field in row.keys() and row[field] is not None:
                            node[field] = row[field]
                    
                    nodes.append(node)
                    
            except sqlite3.OperationalError as e:
                logger.warning(f"Could not query {config['type']}: {e}")
                
        return nodes
    
    def get_edges(self) -> List[Dict[str, Any]]:
        """Extract all edges from the database."""
        conn = sqlite3.connect(self.db_path)
        
        try:
            # Check if pre-computed graph_edges table exists
            if self.use_precomputed and self._table_exists(conn, 'graph_edges'):
                logger.info("Using pre-computed graph_edges table")
                return self._get_precomputed_edges(conn)
            else:
                logger.info("Extracting edges from relationships table")
                return self._extract_edges_from_relationships(conn)
        finally:
            conn.close()
    
    def _get_precomputed_edges(self, conn) -> List[Dict[str, Any]]:
        """Get edges from pre-computed graph_edges table."""
        edges = []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT source_node_id, target_node_id, relationship_type, 
                   weight, attributes
            FROM graph_edges
        """)
        
        for row in cursor.fetchall():
            edge = {
                'source': row['source_node_id'],
                'target': row['target_node_id'],
                'relationship': row['relationship_type'],
                'weight': row['weight']
            }
            
            # Add attributes if present
            if row['attributes']:
                try:
                    attrs = json.loads(row['attributes'])
                    edge.update(attrs)
                except:
                    pass
                    
            edges.append(edge)
            
        return edges
    
    def _extract_edges_from_relationships(self, conn) -> List[Dict[str, Any]]:
        """Extract edges from unified relationships table."""
        edges = []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT source_type, source_id, target_type, target_id, 
                   relationship_type, confidence, context, metadata
            FROM relationships
        """)
        
        for row in cursor.fetchall():
            # Format node IDs
            source_id = self._format_node_id(row['source_type'], row['source_id'])
            target_id = self._format_node_id(row['target_type'], row['target_id'])
            
            edge = {
                'source': source_id,
                'target': target_id,
                'relationship': row['relationship_type']
            }
            
            # Add optional fields
            if row['confidence'] and row['confidence'] != 1.0:
                edge['confidence'] = row['confidence']
                
            if row['context']:
                edge['context'] = row['context']
                
            if row['metadata']:
                try:
                    metadata = json.loads(row['metadata'])
                    edge['metadata'] = metadata
                except:
                    pass
                    
            edges.append(edge)
            
        return edges


# ============================================================================
# Main Functions
# ============================================================================

def build_knowledge_graph(db_path: str, use_precomputed: bool = True) -> KnowledgeGraph:
    """Build a knowledge graph from the v2 database schema."""
    
    # Create graph and provider
    graph = KnowledgeGraph()
    provider = V2SQLProvider(db_path, use_precomputed)
    
    # Extract and add nodes
    logger.info("Extracting nodes...")
    nodes = provider.get_nodes()
    graph.add_nodes_batch(nodes)
    logger.info(f"Added {len(nodes)} nodes")
    
    # Extract and add edges  
    logger.info("Extracting edges...")
    edges = provider.get_edges()
    graph.add_edges_batch(edges)
    logger.info(f"Added {len(edges)} edges")
    
    return graph


def update_graph_tables(db_path: str):
    """Update the pre-computed graph tables from current data."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        logger.info("Building knowledge graph...")
        graph = build_knowledge_graph(db_path, use_precomputed=False)
        nx_graph = graph.get_graph()
        
        # Calculate PageRank
        logger.info("Calculating PageRank...")
        pagerank = nx.pagerank(nx_graph, alpha=0.85)
        
        # Calculate betweenness centrality for smaller graphs
        betweenness = {}
        if nx_graph.number_of_nodes() < 1000:
            logger.info("Calculating betweenness centrality...")
            betweenness = nx.betweenness_centrality(nx_graph)
        
        # Clear existing graph tables
        cursor.execute("DELETE FROM graph_nodes")
        cursor.execute("DELETE FROM graph_edges")
        
        # Insert nodes
        logger.info("Updating graph_nodes table...")
        for node_id, data in nx_graph.nodes(data=True):
            # Calculate degree
            degree = nx_graph.degree(node_id)
            
            # Prepare attributes
            attrs = {k: v for k, v in data.items() 
                    if k not in ['type', 'label']}
            
            cursor.execute("""
                INSERT INTO graph_nodes 
                (node_id, entity_type, entity_id, label, attributes, 
                 degree, pagerank_score, betweenness_centrality)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                node_id,
                data.get('type', 'unknown'),
                node_id.split('_', 1)[1] if '_' in node_id else node_id,
                data.get('label', node_id),
                json.dumps(attrs) if attrs else None,
                degree,
                pagerank.get(node_id, 0),
                betweenness.get(node_id, 0)
            ))
        
        # Insert edges
        logger.info("Updating graph_edges table...")
        edge_id = 1
        for source, target, data in nx_graph.edges(data=True):
            attrs = {k: v for k, v in data.items() 
                    if k != 'relationship'}
            
            cursor.execute("""
                INSERT INTO graph_edges 
                (edge_id, source_node_id, target_node_id, 
                 relationship_type, weight, attributes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                edge_id,
                source,
                target,
                data.get('relationship', 'unknown'),
                data.get('weight', 1.0),
                json.dumps(attrs) if attrs else None
            ))
            edge_id += 1
        
        conn.commit()
        logger.info("Graph tables updated successfully")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Error updating graph tables: {e}")
        raise
    finally:
        conn.close()


def main():
    """Main function for testing."""
    import sys
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "metadata.db"
    
    if not Path(db_path).exists():
        print(f"Error: Database {db_path} not found")
        return
    
    # Build knowledge graph
    graph = build_knowledge_graph(db_path)
    
    # Print statistics
    stats = graph.get_statistics()
    print("\nKnowledge Graph Statistics:")
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Total edges: {stats['total_edges']}")
    print(f"Average degree: {stats['average_degree']:.2f}")
    print(f"Connected components: {stats['connected_components']}")
    
    print("\nNode types:")
    for node_type, count in stats['node_types'].items():
        print(f"  {node_type}: {count}")
    
    print("\nRelationship types:")
    for rel_type, count in stats['relationship_types'].items():
        print(f"  {rel_type}: {count}")
    
    if 'top_nodes_by_pagerank' in stats:
        print("\nTop nodes by PageRank:")
        for node in stats['top_nodes_by_pagerank']:
            print(f"  {node['label']} ({node['type']}): {node['score']:.4f}")
    
    # Export to JSON
    output_path = "KG/knowledge_graph.json"
    graph.export_as_json(output_path)
    print(f"\nGraph exported to {output_path}")
    
    # Update graph tables if requested
    if len(sys.argv) > 2 and sys.argv[2] == '--update-tables':
        print("\nUpdating graph tables...")
        update_graph_tables(db_path)


if __name__ == "__main__":
    main()