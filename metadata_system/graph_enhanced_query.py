#!/usr/bin/env python3
"""
Graph-enhanced query system that combines SQL queries with graph traversal
for more intelligent agent responses.
"""

import sqlite3
import json
import networkx as nx
from typing import List, Dict, Any, Tuple
import numpy as np
from pathlib import Path


class GraphEnhancedQuery:
    """Combines database queries with knowledge graph traversal."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db", 
                 graph_path: str = "metadata_system/knowledge_graph.json"):
        self.db_path = db_path
        self.graph = self._load_graph(graph_path)
        
    def _load_graph(self, graph_path: str) -> nx.Graph:
        """Load knowledge graph from JSON."""
        with open(graph_path, 'r') as f:
            data = json.load(f)
        return nx.node_link_graph(data, edges="links")
    
    def find_related_topics(self, topic: str, max_distance: int = 2) -> List[Dict[str, Any]]:
        """Find topics related to a given topic through the graph."""
        # Find the topic node
        topic_nodes = [n for n, d in self.graph.nodes(data=True) 
                      if d.get('type') == 'topic' and topic.lower() in d.get('label', '').lower()]
        
        if not topic_nodes:
            return []
        
        related = []
        for node in topic_nodes:
            # Get neighbors within max_distance
            for neighbor in nx.single_source_shortest_path_length(self.graph, node, max_distance).keys():
                data = self.graph.nodes[neighbor]
                if data.get('type') == 'topic' and neighbor != node:
                    distance = nx.shortest_path_length(self.graph, node, neighbor)
                    related.append({
                        'topic': data['label'],
                        'distance': distance,
                        'connection_strength': 1.0 / distance
                    })
        
        # Sort by distance
        return sorted(related, key=lambda x: x['distance'])
    
    def find_semantic_connections(self, node_label: str, node_type: str = 'topic') -> List[Dict[str, Any]]:
        """Find semantic relationships for a given node using the enriched graph."""
        # Find nodes matching the label
        matching_nodes = [n for n, d in self.graph.nodes(data=True) 
                         if d.get('type') == node_type and node_label.lower() in d.get('label', '').lower()]
        
        if not matching_nodes:
            # Try semantic concepts
            matching_nodes = [n for n, d in self.graph.nodes(data=True) 
                             if d.get('type') == 'semantic_concept' and node_label.lower() in d.get('label', '').lower()]
        
        connections = []
        for node in matching_nodes:
            # Check all edges for semantic relationships
            for neighbor in self.graph.neighbors(node):
                edge_data = self.graph.get_edge_data(node, neighbor)
                if edge_data and edge_data.get('semantic'):
                    neighbor_data = self.graph.nodes[neighbor]
                    connections.append({
                        'target': neighbor_data.get('label', neighbor),
                        'target_type': neighbor_data.get('type'),
                        'relationship': edge_data.get('relationship'),
                        'description': edge_data.get('description', ''),
                        'direction': 'from'
                    })
            
            # Check incoming edges too
            for predecessor in self.graph.predecessors(node) if self.graph.is_directed() else []:
                edge_data = self.graph.get_edge_data(predecessor, node)
                if edge_data and edge_data.get('semantic'):
                    pred_data = self.graph.nodes[predecessor]
                    connections.append({
                        'target': pred_data.get('label', predecessor),
                        'target_type': pred_data.get('type'),
                        'relationship': edge_data.get('relationship'),
                        'description': edge_data.get('description', ''),
                        'direction': 'to'
                    })
        
        return connections
    
    def find_project_connections(self, project_name: str) -> Dict[str, List[str]]:
        """Find all connections for a given project."""
        # Find project node
        project_nodes = [n for n, d in self.graph.nodes(data=True) 
                        if d.get('type') == 'project' and project_name.lower() in d.get('label', '').lower()]
        
        if not project_nodes:
            return {}
        
        connections = {
            'topics': [],
            'people': [],
            'documents': [],
            'related_projects': []
        }
        
        for node in project_nodes:
            # Get all neighbors
            for neighbor in self.graph.neighbors(node):
                data = self.graph.nodes[neighbor]
                node_type = data.get('type')
                label = data.get('label', data.get('title', ''))
                
                if node_type == 'topic':
                    connections['topics'].append(label)
                elif node_type == 'person':
                    connections['people'].append(label)
                elif node_type == 'document':
                    connections['documents'].append(label)
                elif node_type == 'project' and neighbor != node:
                    connections['related_projects'].append(label)
        
        # Remove duplicates
        for key in connections:
            connections[key] = list(set(connections[key]))
        
        return connections
    
    def find_research_evolution(self, topic: str) -> List[Dict[str, Any]]:
        """Track how research on a topic evolved over time."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find documents mentioning this topic
        cursor.execute("""
            SELECT d.id, d.title, d.date, d.doc_type, d.metadata
            FROM documents d
            JOIN document_topics dt ON d.id = dt.document_id
            JOIN topics t ON dt.topic_id = t.id
            WHERE t.name LIKE ?
            ORDER BY d.date
        """, (f'%{topic}%',))
        
        evolution = []
        for row in cursor.fetchall():
            metadata = json.loads(row[4]) if row[4] else {}
            evolution.append({
                'date': row[2],
                'title': row[1],
                'type': row[3],
                'context': metadata.get('day_summary', metadata.get('core_contributions', ''))
            })
        
        conn.close()
        return evolution
    
    def find_collaboration_patterns(self) -> Dict[str, Any]:
        """Analyze collaboration patterns from the graph."""
        people_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'person']
        
        patterns = {}
        for person in people_nodes:
            person_data = self.graph.nodes[person]
            person_name = person_data['label']
            
            # Find all documents this person is connected to
            docs = []
            topics = set()
            projects = set()
            
            for neighbor in self.graph.neighbors(person):
                neighbor_data = self.graph.nodes[neighbor]
                if neighbor_data.get('type') == 'document':
                    docs.append(neighbor_data['label'])
                    
                    # Find topics and projects of these documents
                    for doc_neighbor in self.graph.neighbors(neighbor):
                        doc_neighbor_data = self.graph.nodes[doc_neighbor]
                        if doc_neighbor_data.get('type') == 'topic':
                            topics.add(doc_neighbor_data['label'])
                        elif doc_neighbor_data.get('type') == 'project':
                            projects.add(doc_neighbor_data['label'])
            
            patterns[person_name] = {
                'documents': len(docs),
                'topics': list(topics),
                'projects': list(projects)
            }
        
        return patterns
    
    def get_node_importance(self) -> List[Tuple[str, str, float]]:
        """Calculate importance of nodes using PageRank."""
        pagerank = nx.pagerank(self.graph)
        
        # Sort by PageRank score
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for node_id, score in sorted_nodes[:20]:  # Top 20
            node_data = self.graph.nodes[node_id]
            results.append((
                node_data.get('label', node_id),
                node_data.get('type', 'unknown'),
                score
            ))
        
        return results
    
    def suggest_connections(self, doc_title: str) -> Dict[str, List[str]]:
        """Suggest potential connections for a document."""
        # Find document node
        doc_nodes = [n for n, d in self.graph.nodes(data=True) 
                    if d.get('type') == 'document' and doc_title.lower() in d.get('title', '').lower()]
        
        if not doc_nodes:
            return {}
        
        suggestions = {
            'similar_documents': [],
            'recommended_topics': [],
            'potential_collaborators': []
        }
        
        for node in doc_nodes:
            # Get current connections
            current_neighbors = set(self.graph.neighbors(node))
            current_topics = {n for n in current_neighbors 
                            if self.graph.nodes[n].get('type') == 'topic'}
            
            # Find documents with similar topics
            for topic in current_topics:
                for doc_neighbor in self.graph.neighbors(topic):
                    if (self.graph.nodes[doc_neighbor].get('type') == 'document' 
                        and doc_neighbor != node):
                        suggestions['similar_documents'].append(
                            self.graph.nodes[doc_neighbor]['title']
                        )
            
            # Recommend topics from similar documents
            for similar_doc in set([n for n, d in self.graph.nodes(data=True) 
                                   if d.get('type') == 'document' and n != node]):
                # Calculate Jaccard similarity
                similar_neighbors = set(self.graph.neighbors(similar_doc))
                similarity = len(current_neighbors & similar_neighbors) / len(current_neighbors | similar_neighbors) if len(current_neighbors | similar_neighbors) > 0 else 0
                
                if similarity > 0.3:  # Threshold
                    for neighbor in similar_neighbors:
                        if (self.graph.nodes[neighbor].get('type') == 'topic' 
                            and neighbor not in current_topics):
                            suggestions['recommended_topics'].append(
                                self.graph.nodes[neighbor]['label']
                            )
        
        # Remove duplicates
        for key in suggestions:
            suggestions[key] = list(set(suggestions[key]))[:5]  # Top 5
        
        return suggestions


def create_agent_context(query: str, db_path: str = "metadata_system/metadata.db") -> Dict[str, Any]:
    """Create enriched context for agent queries using graph + database."""
    enhancer = GraphEnhancedQuery(db_path)
    
    context = {
        'query': query,
        'graph_insights': {},
        'relevant_documents': [],
        'topic_clusters': [],
        'collaboration_info': {},
        'semantic_connections': {}
    }
    
    # Extract potential topics from query
    query_lower = query.lower()
    
    # Check for relationship queries
    if any(word in query_lower for word in ['related', 'connected', 'similar']):
        # Extract topic and find relations
        for node, data in enhancer.graph.nodes(data=True):
            if data.get('type') == 'topic' and data['label'].lower() in query_lower:
                context['topic_clusters'] = enhancer.find_related_topics(data['label'])
                break
    
    # Check for project queries
    if 'project' in query_lower:
        for node, data in enhancer.graph.nodes(data=True):
            if data.get('type') == 'project' and data['label'].lower() in query_lower:
                context['graph_insights'] = enhancer.find_project_connections(data['label'])
                break
    
    # Check for collaboration queries
    if any(word in query_lower for word in ['collaborat', 'people', 'who']):
        context['collaboration_info'] = enhancer.find_collaboration_patterns()
    
    # Check for semantic relationship queries (foundational, contributes, etc.)
    if any(word in query_lower for word in ['foundation', 'contribut', 'connect', 'appli', 'theor']):
        # Look for key concepts mentioned in query
        for node, data in enhancer.graph.nodes(data=True):
            if data.get('label', '').lower() in query_lower:
                semantic_conns = enhancer.find_semantic_connections(data['label'], data.get('type', 'topic'))
                if semantic_conns:
                    context['semantic_connections'][data['label']] = semantic_conns
    
    # Add node importance for general context
    context['key_nodes'] = enhancer.get_node_importance()
    
    return context


if __name__ == "__main__":
    # Test the enhanced query system
    enhancer = GraphEnhancedQuery()
    
    print("=== Graph-Enhanced Query Examples ===\n")
    
    # Example 1: Find related topics
    print("1. Topics related to 'optimal transport':")
    related = enhancer.find_related_topics('optimal transport')
    for item in related[:5]:
        print(f"   - {item['topic']} (distance: {item['distance']})")
    
    # Example 2: Project connections
    print("\n2. Connections for 'Interactive CV' project:")
    connections = enhancer.find_project_connections('Interactive CV')
    for conn_type, items in connections.items():
        if items:
            print(f"   {conn_type}: {', '.join(items[:3])}")
    
    # Example 3: Research evolution
    print("\n3. Evolution of 'reinforcement learning' research:")
    evolution = enhancer.find_research_evolution('reinforcement learning')
    for item in evolution[:3]:
        print(f"   - {item['date']}: {item['title']}")
    
    # Example 4: Node importance
    print("\n4. Most important nodes in the knowledge graph:")
    important = enhancer.get_node_importance()
    for label, node_type, score in important[:5]:
        print(f"   - {label} ({node_type}): {score:.4f}")
    
    # Example 5: Semantic connections (if available)
    print("\n5. Semantic connections for 'Gradient Flows':")
    semantic = enhancer.find_semantic_connections('Gradient Flows')
    for conn in semantic[:3]:
        print(f"   - {conn['relationship']} → {conn['target']} ({conn['target_type']})")
        if conn['description']:
            print(f"     Description: {conn['description']}")
    
    # Example 6: Agent context
    print("\n6. Agent context for query: 'What projects are related to optimal transport?'")
    context = create_agent_context("What projects are related to optimal transport?")
    print(f"   Found {len(context['topic_clusters'])} related topics")
    print(f"   Key nodes: {[n[0] for n in context['key_nodes'][:3]]}")