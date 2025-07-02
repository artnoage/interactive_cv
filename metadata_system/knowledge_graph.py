#!/usr/bin/env python3
"""
Extract and visualize knowledge graph from the metadata database.
Creates network graphs showing relationships between documents, topics, people, and projects.
"""

import sqlite3
import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeGraphExtractor:
    """Extract knowledge graph from metadata database."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db"):
        self.db_path = db_path
        self.graph = nx.Graph()
        
    def extract_graph(self) -> nx.Graph:
        """Extract full knowledge graph from database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # Add document nodes
            self._add_documents(conn)
            
            # Add topic nodes and edges
            self._add_topics(conn)
            
            # Add people nodes and edges
            self._add_people(conn)
            
            # Add project nodes and edges
            self._add_projects(conn)
            
            # Add semantic concepts and relationships (if they exist)
            self._add_semantic_relationships(conn)
            
            logger.info(f"Graph extracted: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
            
        finally:
            conn.close()
            
        return self.graph
    
    def _add_documents(self, conn):
        """Add document nodes to the graph."""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, doc_type, date 
            FROM documents
        """)
        
        for row in cursor.fetchall():
            self.graph.add_node(
                f"doc_{row['id']}", 
                label=row['title'],
                type='document',
                doc_type=row['doc_type'],
                date=row['date']
            )
    
    def _add_topics(self, conn):
        """Add topic nodes and document-topic edges."""
        cursor = conn.cursor()
        
        # Add topic nodes
        cursor.execute("SELECT id, name FROM topics")
        for row in cursor.fetchall():
            self.graph.add_node(
                f"topic_{row['id']}", 
                label=row['name'],
                type='topic'
            )
        
        # Add document-topic edges
        cursor.execute("""
            SELECT dt.document_id, dt.topic_id, d.title, t.name
            FROM document_topics dt
            JOIN documents d ON dt.document_id = d.id
            JOIN topics t ON dt.topic_id = t.id
        """)
        
        for row in cursor.fetchall():
            self.graph.add_edge(
                f"doc_{row['document_id']}", 
                f"topic_{row['topic_id']}",
                relationship='has_topic'
            )
    
    def _add_people(self, conn):
        """Add people nodes and document-people edges."""
        cursor = conn.cursor()
        
        # Add people nodes
        cursor.execute("SELECT id, name FROM people")
        for row in cursor.fetchall():
            self.graph.add_node(
                f"person_{row['id']}", 
                label=row['name'],
                type='person'
            )
        
        # Add document-people edges
        cursor.execute("""
            SELECT dp.document_id, dp.person_id
            FROM document_people dp
        """)
        
        for row in cursor.fetchall():
            self.graph.add_edge(
                f"doc_{row['document_id']}", 
                f"person_{row['person_id']}",
                relationship='mentions_person'
            )
    
    def _add_projects(self, conn):
        """Add project nodes and document-project edges."""
        cursor = conn.cursor()
        
        # Add project nodes
        cursor.execute("SELECT id, name FROM projects")
        for row in cursor.fetchall():
            self.graph.add_node(
                f"project_{row['id']}", 
                label=row['name'],
                type='project'
            )
        
        # Add document-project edges
        cursor.execute("""
            SELECT dp.document_id, dp.project_id
            FROM document_projects dp
        """)
        
        for row in cursor.fetchall():
            self.graph.add_edge(
                f"doc_{row['document_id']}", 
                f"project_{row['project_id']}",
                relationship='relates_to_project'
            )
    
    def _add_semantic_relationships(self, conn):
        """Add semantic concepts and relationships if they exist."""
        cursor = conn.cursor()
        
        # Check if semantic tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='semantic_concepts'
        """)
        if not cursor.fetchone():
            return  # Tables don't exist yet
        
        # Add semantic concept nodes
        cursor.execute("SELECT concept_id, concept_type, name, description FROM semantic_concepts")
        for row in cursor.fetchall():
            self.graph.add_node(
                f"concept_{row[0]}", 
                label=row[2],  # name
                type='semantic_concept',
                concept_type=row[1],
                description=row[3]
            )
        
        # Add semantic relationships
        cursor.execute("""
            SELECT source_type, source_id, target_type, target_id, 
                   relationship_type, description 
            FROM semantic_relationships
        """)
        
        for row in cursor.fetchall():
            source_type, source_id, target_type, target_id, rel_type, desc = row
            
            # Create node IDs based on type
            if source_type == 'document':
                source_node = f"doc_{source_id}"
            elif source_type == 'topic':
                # Find topic ID by name
                cursor.execute("SELECT id FROM topics WHERE LOWER(name) = LOWER(?)", (source_id,))
                topic_row = cursor.fetchone()
                source_node = f"topic_{topic_row[0]}" if topic_row else f"concept_{source_id}"
            else:
                source_node = f"concept_{source_id}"
            
            if target_type == 'document':
                target_node = f"doc_{target_id}"
            elif target_type == 'topic':
                # Find topic ID by name
                cursor.execute("SELECT id FROM topics WHERE LOWER(name) = LOWER(?)", (target_id,))
                topic_row = cursor.fetchone()
                target_node = f"topic_{topic_row[0]}" if topic_row else f"concept_{target_id}"
            else:
                target_node = f"concept_{target_id}"
            
            # Add edge if both nodes exist
            if self.graph.has_node(source_node) and self.graph.has_node(target_node):
                self.graph.add_edge(
                    source_node, 
                    target_node,
                    relationship=rel_type,
                    semantic=True,
                    description=desc
                )
    
    def export_for_web(self, output_path: str = "metadata_system/knowledge_graph.json"):
        """Export graph in format suitable for web visualization (D3.js/vis.js)."""
        # Convert to node-link format for D3.js
        data = nx.node_link_data(self.graph)
        
        # Enhance node data for visualization
        for node in data['nodes']:
            node['group'] = node.get('type', 'unknown')
            node['title'] = node.get('label', node['id'])
            
        # Enhance edge data
        for link in data['links']:
            link['value'] = 1  # Weight for visualization
            
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Graph exported to {output_path}")
        return data
    
    def visualize_matplotlib(self, figsize=(20, 20)):
        """Create a basic visualization using matplotlib."""
        plt.figure(figsize=figsize)
        
        # Create layout
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Separate nodes by type
        node_colors = {
            'document': '#ff9999',
            'topic': '#66b3ff', 
            'person': '#99ff99',
            'project': '#ffcc99'
        }
        
        # Draw nodes by type
        for node_type, color in node_colors.items():
            nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == node_type]
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=nodes,
                node_color=color,
                node_size=500,
                label=node_type.capitalize()
            )
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3)
        
        # Draw labels for smaller graphs
        if self.graph.number_of_nodes() < 50:
            labels = nx.get_node_attributes(self.graph, 'label')
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
        
        plt.title("Interactive CV Knowledge Graph")
        plt.legend()
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('metadata_system/knowledge_graph.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_statistics(self) -> Dict:
        """Get graph statistics."""
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        
        # Calculate average degree
        if num_nodes > 0:
            degree_dict = dict(self.graph.degree())
            avg_degree = sum(degree_dict.values()) / num_nodes
        else:
            avg_degree = 0
            
        stats = {
            'total_nodes': num_nodes,
            'total_edges': num_edges,
            'node_types': {},
            'average_degree': avg_degree,
            'connected_components': nx.number_connected_components(self.graph)
        }
        
        # Count nodes by type
        for _, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'unknown')
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            
        return stats


def create_web_visualization_html(graph_data: dict, output_path: str = "metadata_system/knowledge_graph.html"):
    """Create an HTML file with vis.js visualization."""
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Interactive CV Knowledge Graph</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        #mynetwork {{
            width: 100%%;
            height: 800px;
            border: 1px solid lightgray;
        }}
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .legend {{
            margin: 20px 0;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <h1>Interactive CV Knowledge Graph</h1>
    <div class="legend">
        <div class="legend-item">
            <span class="legend-color" style="background-color: #ff9999;"></span>Documents
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background-color: #66b3ff;"></span>Topics
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background-color: #99ff99;"></span>People
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background-color: #ffcc99;"></span>Projects
        </div>
    </div>
    <div id="mynetwork"></div>

    <script type="text/javascript">
        // Parse graph data
        var graphData = {graph_data};
        
        // Transform nodes
        var nodes = graphData.nodes.map(function(node) {{
            var color = '#cccccc';
            if (node.group === 'document') color = '#ff9999';
            else if (node.group === 'topic') color = '#66b3ff';
            else if (node.group === 'person') color = '#99ff99';
            else if (node.group === 'project') color = '#ffcc99';
            
            return {{
                id: node.id,
                label: node.title || node.id,
                color: color,
                title: node.title + ' (' + node.group + ')'
            }};
        }});
        
        // Transform edges
        var edges = graphData.links.map(function(link) {{
            return {{
                from: link.source,
                to: link.target
            }};
        }});
        
        // Create network
        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(edges)
        }};
        var options = {{
            physics: {{
                stabilization: false,
                barnesHut: {{
                    springLength: 200
                }}
            }},
            nodes: {{
                shape: 'dot',
                size: 16,
                font: {{
                    size: 12
                }}
            }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>
"""
    
    # Use format instead of % to avoid issues
    html_content = html_template.format(graph_data=json.dumps(graph_data))
    
    with open(output_path, 'w') as f:
        f.write(html_content)
        
    logger.info(f"Web visualization saved to {output_path}")


if __name__ == "__main__":
    # Extract knowledge graph
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
    for node_type, count in stats['node_types'].items():
        print(f"  {node_type}: {count}")
    
    # Export for web
    graph_data = extractor.export_for_web()
    
    # Create web visualization (commented out since using Gemini visualization)
    # create_web_visualization_html(graph_data)
    
    print("\nFiles created:")
    print("  - metadata_system/knowledge_graph.json (graph data)")
    # print("  - metadata_system/knowledge_graph.html (interactive visualization)")
    
    # Optional: Create matplotlib visualization for smaller graphs
    if stats['total_nodes'] < 100:
        print("\nCreating matplotlib visualization...")
        extractor.visualize_matplotlib()
        print("  - metadata_system/knowledge_graph.png (static image)")
    else:
        print("\nGraph too large for matplotlib visualization. Use the HTML file instead.")