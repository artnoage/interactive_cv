#!/usr/bin/env python3
"""
Blueprint-driven knowledge graph builder
Uses visualization blueprints to determine node types, colors, and relationships
"""

import sqlite3
import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Add blueprints to path (robust path resolution)
blueprint_core_path = Path(__file__).parent.parent / "blueprints" / "core"
if str(blueprint_core_path) not in sys.path:
    sys.path.insert(0, str(blueprint_core_path))

try:
    from blueprint_loader import get_blueprint_loader, load_visualization_config # type: ignore
except ImportError as e:
    print(f"Error importing blueprint_loader: {e}")
    print(f"Blueprint path: {blueprint_core_path}")
    raise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphBuilder:
    """Build knowledge graph using blueprint-driven visualization rules"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.blueprint_loader = get_blueprint_loader()
        self.viz_config = load_visualization_config()
        
    def _get_node_type_from_entity(self, entity_type: str, category: Optional[str], 
                                  document_type: Optional[str] = None) -> str:
        """Determine visualization node type based on entity type and category"""
        
        # Handle document types
        if entity_type == 'document':
            if document_type:
                doc_mapping = self.viz_config.node_type_mappings.get('document', {})
                return doc_mapping.get(document_type, entity_type)
            return entity_type
        
        # Handle entities with categories
        type_mappings = self.viz_config.node_type_mappings.get(entity_type, {})
        
        if category and category in type_mappings:
            return type_mappings[category]
        
        # Check for default mapping
        if 'default' in type_mappings:
            return type_mappings['default']
        
        # Fall back to entity type
        return entity_type
    
    def _get_node_attributes(self, node_type: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get node visual attributes based on blueprint configuration"""
        
        attributes = {
            'color': self.viz_config.colors.get(node_type, self.viz_config.colors.get('default', '#888888')),
            'size': self.viz_config.sizes.get(node_type, self.viz_config.sizes.get('default', 10))
        }
        
        # Add additional attributes from entity data
        for key in ['description', 'category', 'domain', 'role', 'affiliation', 'date']:
            if key in entity_data and entity_data[key]:
                attributes[key] = entity_data[key]
        
        return attributes
    
    def _get_edge_attributes(self, relationship_type: str) -> Dict[str, Any]:
        """Get edge visual attributes based on blueprint configuration"""
        
        edge_style = self.viz_config.edge_styles.get(
            relationship_type, 
            self.viz_config.edge_styles.get('default', {})
        )
        
        return {
            'color': edge_style.get('color', '#999999'),
            'width': edge_style.get('width', 1),
            'style': edge_style.get('style', 'solid')
        }
    
    def build_graph(self) -> Dict[str, Any]:
        """Build knowledge graph from database using blueprint visualization rules"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        nodes = []
        links = []
        
        try:
            cursor = conn.cursor()
            
            # Build nodes from documents
            logger.info("Building document nodes...")
            
            # Academic documents
            cursor.execute("""
                SELECT id, title, date, domain, document_type
                FROM academic_documents
            """)
            
            for row in cursor.fetchall():
                node_id = f"academic_{row['id']}"
                node_type = self._get_node_type_from_entity('document', None, 'academic_document')
                
                entity_data = {
                    'title': row['title'],
                    'date': row['date'],
                    'domain': row['domain'],
                    'document_type': row['document_type']
                }
                
                attributes = self._get_node_attributes(node_type, entity_data)
                
                nodes.append({
                    'id': node_id,
                    'type': node_type,
                    'label': row['title'][:80] + '...' if len(row['title']) > 80 else row['title'],
                    **attributes
                })
            
            # Chronicle documents
            cursor.execute("""
                SELECT id, title, date, note_type
                FROM chronicle_documents
            """)
            
            for row in cursor.fetchall():
                node_id = f"chronicle_{row['id']}"
                node_type = self._get_node_type_from_entity('document', None, 'chronicle_document')
                
                entity_data = {
                    'title': row['title'],
                    'date': row['date'],
                    'note_type': row['note_type']
                }
                
                attributes = self._get_node_attributes(node_type, entity_data)
                
                nodes.append({
                    'id': node_id,
                    'type': node_type,
                    'label': row['title'],
                    **attributes
                })
            
            # Build nodes from entities
            logger.info("Building entity nodes...")
            
            entity_tables = [
                ('topics', 'topic', ['name', 'category', 'description']),
                ('people', 'person', ['name', 'role', 'affiliation']),
                ('projects', 'project', ['name', 'description']),
                ('institutions', 'institution', ['name', 'type', 'location']),
                ('methods', 'method', ['name', 'category', 'description']),
                ('applications', 'application', ['name', 'domain', 'description'])
            ]
            
            for table, entity_type, fields in entity_tables:
                cursor.execute(f"SELECT {', '.join(fields)}, id FROM {table}")
                
                for row in cursor.fetchall():
                    node_id = f"{entity_type}_{row['id']}"
                    
                    # Determine visualization node type using blueprint
                    category = row['category'] if 'category' in row.keys() else (row['type'] if 'type' in row.keys() else None)
                    node_type = self._get_node_type_from_entity(entity_type, category)
                    
                    # Prepare entity data
                    entity_data = {field: row[field] for field in fields if field in row.keys() and row[field]}
                    
                    # Get visual attributes from blueprint
                    attributes = self._get_node_attributes(node_type, entity_data)
                    
                    nodes.append({
                        'id': node_id,
                        'type': node_type,
                        'label': row['name'],
                        'original_category': category,
                        **attributes
                    })
            
            # Build edges from relationships
            logger.info("Building relationship edges...")
            
            cursor.execute("""
                SELECT source_type, source_id, target_type, target_id, 
                       relationship_type, confidence, metadata
                FROM relationships
            """)
            
            for row in cursor.fetchall():
                # Fix document ID mapping - remove duplicate prefixes
                if row['source_type'] == 'document':
                    source_id = row['source_id']  # Use academic_1, chronicle_2 directly
                else:
                    source_id = f"{row['source_type']}_{row['source_id']}"
                    
                if row['target_type'] == 'document':
                    target_id = row['target_id']  # Use academic_1, chronicle_2 directly
                else:
                    target_id = f"{row['target_type']}_{row['target_id']}"
                
                # Get edge attributes from blueprint
                edge_attrs = self._get_edge_attributes(row['relationship_type'])
                
                link = {
                    'source': source_id,
                    'target': target_id,
                    'type': row['relationship_type'],
                    'confidence': row['confidence'] or 1.0,
                    **edge_attrs
                }
                
                # Add metadata if available
                if row['metadata']:
                    try:
                        metadata = json.loads(row['metadata'])
                        link['metadata'] = metadata
                    except:
                        pass
                
                links.append(link)
            
        finally:
            conn.close()
        
        # Calculate statistics
        type_counts = {}
        for node in nodes:
            node_type = node['type']
            type_counts[node_type] = type_counts.get(node_type, 0) + 1
        
        relationship_counts = {}
        for link in links:
            rel_type = link['type']
            relationship_counts[rel_type] = relationship_counts.get(rel_type, 0) + 1
        
        logger.info(f"Built graph with {len(nodes)} nodes and {len(links)} edges")
        logger.info("Node type distribution:")
        for node_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {node_type}: {count}")
        
        # Create graph data structure
        graph_data = {
            'nodes': nodes,
            'links': links,
            'metadata': {
                'version': 'blueprint-v1.0',
                'total_nodes': len(nodes),
                'total_edges': len(links),
                'node_types': type_counts,
                'relationship_types': relationship_counts,
                'legend': self.viz_config.legend,
                'node_groups': self.viz_config.node_groups
            }
        }
        
        return graph_data
    
    def export_graph(self, output_path: str) -> Dict[str, Any]:
        """Build and export knowledge graph to JSON file"""
        
        logger.info(f"Building blueprint-driven knowledge graph from {self.db_path}")
        graph_data = self.build_graph()
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        logger.info(f"Graph saved to {output_path}")
        
        return graph_data


def main():
    """Main function to build blueprint-driven knowledge graph"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build blueprint-driven knowledge graph')
    parser.add_argument('db_path', help='Path to SQLite database')
    parser.add_argument('--output', default='KG/knowledge_graph.json',
                       help='Output JSON file path')
    parser.add_argument('--validate-blueprints', action='store_true',
                       help='Validate blueprint configurations')
    
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
            print("All blueprints are valid!")
    
    # Build graph
    builder = GraphBuilder(args.db_path)
    graph_data = builder.export_graph(args.output)
    
    # Print statistics
    print(f"\nBlueprint-Driven Knowledge Graph Generated!")
    print(f"Total nodes: {graph_data['metadata']['total_nodes']}")
    print(f"Total edges: {graph_data['metadata']['total_edges']}")
    
    print(f"\nRich node types (from blueprints):")
    for node_type, count in sorted(graph_data['metadata']['node_types'].items(), 
                                  key=lambda x: x[1], reverse=True):
        print(f"  {node_type}: {count}")
    
    print(f"\nTop relationship types:")
    rel_types = sorted(graph_data['metadata']['relationship_types'].items(), 
                      key=lambda x: x[1], reverse=True)[:10]
    for rel_type, count in rel_types:
        print(f"  {rel_type}: {count}")
    
    print(f"\nVisualization features:")
    print(f"  - Colors: {len(load_visualization_config().colors)} node types")
    print(f"  - Edge styles: {len(load_visualization_config().edge_styles)} relationship types")
    print(f"  - Node groups: {len(load_visualization_config().node_groups)} layout groups")
    
    return 0


if __name__ == "__main__":
    exit(main())