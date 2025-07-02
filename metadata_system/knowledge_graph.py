#!/usr/bin/env python3
"""
Configurable knowledge graph extractor.
Extract entities and relationships based on a flexible schema definition.
"""

import sqlite3
import json
import networkx as nx
from typing import Dict, List, Tuple, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Default schema that matches the current database structure
DEFAULT_SCHEMA = {
    'entities': {
        'chronicle_document': {
            'table': 'chronicle_documents',
            'id_column': 'id',
            'id_prefix': 'doc_',
            'label_column': 'title',
            'attributes': {
                'title': 'title',
                'date': 'date'
            }
        },
        'academic_document': {
            'table': 'academic_documents',
            'id_column': 'id',
            'id_prefix': 'doc_',
            'label_column': 'title',
            'attributes': {
                'title': 'title',
                'date': 'date'
            }
        },
        'topic': {
            'table': 'topics',
            'id_column': 'id',
            'id_prefix': 'topic_',
            'label_column': 'name',
            'attributes': {
                'name': 'name'
            }
        },
        'person': {
            'table': 'people',
            'id_column': 'id',
            'id_prefix': 'person_',
            'label_column': 'name',
            'attributes': {
                'name': 'name'
            }
        },
        'project': {
            'table': 'projects',
            'id_column': 'id',
            'id_prefix': 'project_',
            'label_column': 'name',
            'attributes': {
                'name': 'name'
            }
        },
        'institution': {
            'table': 'institutions',
            'id_column': 'id',
            'id_prefix': 'institution_',
            'label_column': 'name',
            'attributes': {
                'name': 'name',
                'description': 'description'
            },
            'optional': True  # Table might not exist
        },
        'semantic_concept': {
            'table': 'semantic_concepts',
            'id_column': 'concept_id',
            'id_prefix': 'concept_',
            'label_column': 'name',
            'attributes': {
                'name': 'name',
                'concept_type': 'concept_type',
                'description': 'description'
            },
            'filters': {
                'concept_type': {'not': 'institution'}  # Exclude institutions
            },
            'optional': True
        }
    },
    'relationships': {
        'has_topic': {
            'table': 'document_topics',
            'source': {'column': 'document_id', 'entity': ['chronicle_document', 'academic_document']},
            'target': {'column': 'topic_id', 'entity': 'topic'}
        },
        'mentions_person': {
            'table': 'document_people',
            'source': {'column': 'document_id', 'entity': ['chronicle_document', 'academic_document']},
            'target': {'column': 'person_id', 'entity': 'person'}
        },
        'relates_to_project': {
            'table': 'document_projects',
            'source': {'column': 'document_id', 'entity': ['chronicle_document', 'academic_document']},
            'target': {'column': 'project_id', 'entity': 'project'}
        },
        'affiliated_with': {
            'table': 'document_institutions',
            'source': {'column': 'document_id', 'entity': ['chronicle_document', 'academic_document']},
            'target': {'column': 'institution_id', 'entity': 'institution'},
            'optional': True
        },
        'semantic': {
            'table': 'semantic_relationships',
            'source': {'column': 'source_id', 'entity_column': 'source_type'},
            'target': {'column': 'target_id', 'entity_column': 'target_type'},
            'relationship_column': 'relationship_type',
            'attributes': ['description'],
            'optional': True,
            'custom_handler': True  # Needs special handling for dynamic entity types
        }
    }
}


class KnowledgeGraphExtractor:
    """Extract knowledge graph based on configurable schema."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db", schema: Dict = None):
        self.db_path = db_path
        self.schema = schema or DEFAULT_SCHEMA
        self.graph = nx.Graph()
        
    def extract_graph(self) -> nx.Graph:
        """Extract full knowledge graph based on schema."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # Extract all entity types
            for entity_type, config in self.schema['entities'].items():
                self._add_entities(conn, entity_type, config)
            
            # Extract all relationships
            for rel_type, config in self.schema['relationships'].items():
                if config.get('custom_handler'):
                    self._add_semantic_relationships(conn, rel_type, config)
                else:
                    self._add_relationships(conn, rel_type, config)
            
            logger.info(f"Graph extracted: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
            
        finally:
            conn.close()
            
        return self.graph
    
    def _table_exists(self, conn, table_name: str) -> bool:
        """Check if a table exists in the database."""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    
    def _add_entities(self, conn, entity_type: str, config: Dict):
        """Add entities of a specific type based on configuration."""
        table = config['table']
        
        # Check if table exists (for optional tables)
        if config.get('optional', False) and not self._table_exists(conn, table):
            logger.debug(f"Skipping optional table: {table}")
            return
        
        cursor = conn.cursor()
        
        # Build query
        columns = [config['id_column']]
        if 'label_column' in config:
            columns.append(config['label_column'])
        
        # Add attribute columns
        for attr_name, col_name in config.get('attributes', {}).items():
            if col_name not in columns:
                columns.append(col_name)
        
        query = f"SELECT {', '.join(columns)} FROM {table}"
        
        # Add filters if specified
        if 'filters' in config:
            where_clauses = []
            for col, filter_config in config['filters'].items():
                if 'not' in filter_config:
                    where_clauses.append(f"{col} != '{filter_config['not']}'")
                elif 'equals' in filter_config:
                    where_clauses.append(f"{col} = '{filter_config['equals']}'")
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
        
        cursor.execute(query)
        
        # Add nodes
        for row in cursor.fetchall():
            node_id = f"{config['id_prefix']}{row[config['id_column']]}"
            
            # Build node attributes
            node_attrs = {
                'type': entity_type
            }
            
            # Add label
            if 'label_column' in config:
                node_attrs['label'] = row[config['label_column']]
            
            # Add other attributes
            for attr_name, col_name in config.get('attributes', {}).items():
                value = row[col_name]
                if value is not None:
                    node_attrs[attr_name] = value
            
            self.graph.add_node(node_id, **node_attrs)
        
        logger.debug(f"Added {cursor.rowcount} {entity_type} entities")
    
    def _add_relationships(self, conn, rel_type: str, config: Dict):
        """Add relationships based on configuration."""
        table = config['table']
        
        # Check if table exists (for optional relationships)
        if config.get('optional', False) and not self._table_exists(conn, table):
            logger.debug(f"Skipping optional relationship table: {table}")
            return
        
        cursor = conn.cursor()
        
        # Build query
        columns = [
            config['source']['column'],
            config['target']['column']
        ]
        
        # Add attribute columns if specified
        for attr in config.get('attributes', []):
            columns.append(attr)
        
        query = f"SELECT {', '.join(columns)} FROM {table}"
        cursor.execute(query)
        
        # Add edges
        # Handle multiple entity types for source/target
        source_entities = config['source']['entity']
        if not isinstance(source_entities, list):
            source_entities = [source_entities]
        target_entities = config['target']['entity']
        if not isinstance(target_entities, list):
            target_entities = [target_entities]
        
        for row in cursor.fetchall():
            source_id_raw = row[config['source']['column']]
            target_id_raw = row[config['target']['column']]
            
            # Try to find the source node with any of the possible entity types
            source_node = None
            for entity_type in source_entities:
                if entity_type in self.schema['entities']:
                    entity_config = self.schema['entities'][entity_type]
                    potential_id = f"{entity_config['id_prefix']}{source_id_raw}"
                    if self.graph.has_node(potential_id):
                        source_node = potential_id
                        break
            
            # Try to find the target node with any of the possible entity types
            target_node = None
            for entity_type in target_entities:
                if entity_type in self.schema['entities']:
                    entity_config = self.schema['entities'][entity_type]
                    potential_id = f"{entity_config['id_prefix']}{target_id_raw}"
                    if self.graph.has_node(potential_id):
                        target_node = potential_id
                        break
            
            # Only add edge if both nodes exist
            if source_node and target_node:
                edge_attrs = {'relationship': rel_type}
                
                # Add additional attributes
                for attr in config.get('attributes', []):
                    if row[attr] is not None:
                        edge_attrs[attr] = row[attr]
                
                self.graph.add_edge(source_node, target_node, **edge_attrs)
    
    def _add_semantic_relationships(self, conn, rel_type: str, config: Dict):
        """Handle semantic relationships with dynamic entity types."""
        table = config['table']
        
        if not self._table_exists(conn, table):
            logger.debug(f"Skipping semantic relationships table: {table}")
            return
        
        cursor = conn.cursor()
        
        # Query semantic relationships
        cursor.execute(f"""
            SELECT source_type, source_id, target_type, target_id, 
                   relationship_type, description 
            FROM {table}
        """)
        
        for row in cursor.fetchall():
            source_type, source_id, target_type, target_id, rel_name, desc = row
            
            # Map entity types to node IDs
            source_node = self._get_node_id_for_semantic(conn, source_type, source_id)
            target_node = self._get_node_id_for_semantic(conn, target_type, target_id)
            
            # Add edge if both nodes exist
            if source_node and target_node and self.graph.has_node(source_node) and self.graph.has_node(target_node):
                self.graph.add_edge(
                    source_node, 
                    target_node,
                    relationship=rel_name,
                    semantic=True,
                    description=desc or ''
                )
    
    def _get_node_id_for_semantic(self, conn, entity_type: str, entity_id: str) -> Optional[str]:
        """Get the graph node ID for a semantic relationship entity."""
        if entity_type == 'document':
            return f"doc_{entity_id}"
        elif entity_type == 'topic':
            # Find topic ID by name
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM topics WHERE LOWER(name) = LOWER(?)", (entity_id,))
            row = cursor.fetchone()
            return f"topic_{row[0]}" if row else f"concept_{entity_id}"
        elif entity_type == 'concept':
            return f"concept_{entity_id}"
        else:
            return None
    
    def export_as_json(self, output_path: str = "metadata_system/knowledge_graph.json"):
        """Export graph as JSON in node-link format."""
        data = nx.node_link_data(self.graph)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Graph exported to {output_path}")
        return data
    
    def get_statistics(self) -> Dict:
        """Get graph statistics."""
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        
        stats = {
            'total_nodes': num_nodes,
            'total_edges': num_edges,
            'node_types': {},
            'average_degree': (2 * num_edges / num_nodes) if num_nodes > 0 else 0,
            'connected_components': nx.number_connected_components(self.graph)
        }
        
        # Count nodes by type
        for _, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'unknown')
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            
        return stats


if __name__ == "__main__":
    # Extract knowledge graph using default schema
    extractor = KnowledgeGraphExtractor()
    graph = extractor.extract_graph()
    
    # Get statistics
    stats = extractor.get_statistics()
    print("\nKnowledge Graph Statistics:")
    print(f"  Total nodes: {stats['total_nodes']}")
    print(f"  Total edges: {stats['total_edges']}")
    print(f"  Average connections per node: {stats['average_degree']:.2f}")
    print(f"  Connected components: {stats['connected_components']}")
    print("\nNodes by type:")
    for node_type, count in sorted(stats['node_types'].items()):
        print(f"  {node_type}: {count}")
    
    # Export as JSON
    extractor.export_as_json()
    
    print("\nGraph data exported to: metadata_system/knowledge_graph.json")