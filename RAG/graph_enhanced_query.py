#!/usr/bin/env python3
"""
Graph-enhanced query system that combines SQL queries with graph traversal
for more intelligent agent responses in the Interactive CV RAG system.

This module provides intelligent query enhancement by leveraging the knowledge graph
to find semantic connections, track research evolution, and discover relationships
between entities that aren't immediately obvious from simple database queries.
"""

import sqlite3
import json
import networkx as nx
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphEnhancedQuery:
    """
    Combines database queries with knowledge graph traversal for intelligent RAG.
    
    This class provides sophisticated query enhancement capabilities by combining
    traditional SQL database queries with graph-based analysis to discover hidden
    relationships and provide richer context for agent responses.
    """
    
    def __init__(self, db_path: str = "DB/metadata.db", 
                 graph_path: str = "KG/knowledge_graph.json"):
        """
        Initialize the graph-enhanced query system.
        
        Args:
            db_path: Path to the SQLite database
            graph_path: Path to the knowledge graph JSON file
        """
        self.db_path = db_path
        self.graph_path = graph_path
        self.graph = None
        self._load_graph()
        
    def _load_graph(self) -> None:
        """Load knowledge graph from JSON with proper error handling."""
        try:
            # Try the provided path first
            if Path(self.graph_path).exists():
                with open(self.graph_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.graph = nx.node_link_graph(data)
                logger.info(f"Loaded knowledge graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
                return
            
            # Try the pruned graph in web_ui folder
            pruned_path = "web_ui/knowledge_graph.json"
            if Path(pruned_path).exists():
                with open(pruned_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.graph = nx.node_link_graph(data)
                logger.info(f"Loaded pruned knowledge graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
                return
                
            # If neither exists, create empty graph
            logger.warning(f"Knowledge graph file not found at {self.graph_path} or {pruned_path}. Creating empty graph.")
            self.graph = nx.Graph()
            
        except Exception as e:
            logger.error(f"Error loading knowledge graph: {e}")
            self.graph = nx.Graph()
    
    def _get_db_connection(self) -> sqlite3.Connection:
        """Get database connection with proper error handling."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def is_graph_available(self) -> bool:
        """Check if the knowledge graph is available and non-empty."""
        return self.graph is not None and self.graph.number_of_nodes() > 0
    
    def find_related_topics(self, topic: str, max_distance: int = 2) -> List[Dict[str, Any]]:
        """
        Find topics related to a given topic through graph traversal.
        
        Args:
            topic: Topic name to search for
            max_distance: Maximum graph distance to search
            
        Returns:
            List of related topics with distance and connection strength
        """
        if not self.is_graph_available():
            logger.warning("Knowledge graph not available for topic search")
            return []
            
        try:
            # Find topic nodes with flexible matching
            topic_lower = topic.lower()
            topic_nodes = []
            
            for node, data in self.graph.nodes(data=True):
                if data.get('type') in ['topic', 'math_foundation', 'research_area', 'research_insight']:
                    label = data.get('label', '').lower()
                    if topic_lower in label or any(word in label for word in topic_lower.split()):
                        topic_nodes.append(node)
            
            if not topic_nodes:
                logger.info(f"No topic nodes found for '{topic}'")
                return []
            
            related = []
            seen_topics = set()
            
            for node in topic_nodes:
                try:
                    # Get neighbors within max_distance
                    distances = nx.single_source_shortest_path_length(self.graph, node, max_distance)
                    
                    for neighbor, distance in distances.items():
                        if neighbor == node or neighbor in seen_topics:
                            continue
                            
                        data = self.graph.nodes[neighbor]
                        node_type = data.get('type', '')
                        
                        # Include various types of related nodes
                        if node_type in ['topic', 'math_foundation', 'research_area', 'research_insight']:
                            label = data.get('label', '')
                            if label and label not in [d['topic'] for d in related]:
                                related.append({
                                    'topic': label,
                                    'type': node_type,
                                    'distance': distance,
                                    'connection_strength': 1.0 / max(distance, 0.1),
                                    'category': data.get('category', 'unknown')
                                })
                                seen_topics.add(neighbor)
                                
                except nx.NetworkXError as e:
                    logger.warning(f"Graph traversal error for node {node}: {e}")
                    continue
            
            # Sort by connection strength (closer topics first)
            return sorted(related, key=lambda x: x['connection_strength'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error finding related topics for '{topic}': {e}")
            return []
    
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
            
            # Check incoming edges too (only for directed graphs)
            if isinstance(self.graph, nx.DiGraph):
                for predecessor in self.graph.predecessors(node):
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
        """
        Track how research on a topic evolved over time using database queries.
        
        Args:
            topic: Topic to track evolution for
            
        Returns:
            List of documents mentioning the topic, ordered by date
        """
        try:
            conn = self._get_db_connection()
            
            # First try with the relationships table approach using UNION for split tables
            query = """
                SELECT DISTINCT 
                    'academic_' || ad.id as doc_id, ad.title, ad.date, 'academic' as document_type, ad.content,
                    t.name as topic_name, t.category
                FROM academic_documents ad
                JOIN relationships r ON ('academic_' || ad.id) = r.source_id OR ('academic_' || ad.id) = r.target_id
                JOIN topics t ON (r.source_id = t.id OR r.target_id = t.id)
                WHERE t.name LIKE ? AND ad.title IS NOT NULL
                
                UNION ALL
                
                SELECT DISTINCT 
                    'chronicle_' || cd.id as doc_id, cd.title, cd.date, 'chronicle' as document_type, cd.content,
                    t.name as topic_name, t.category
                FROM chronicle_documents cd
                JOIN relationships r ON ('chronicle_' || cd.id) = r.source_id OR ('chronicle_' || cd.id) = r.target_id
                JOIN topics t ON (r.source_id = t.id OR r.target_id = t.id)
                WHERE t.name LIKE ? AND cd.title IS NOT NULL
                
                ORDER BY date
            """
            
            results = conn.execute(query, (f'%{topic}%', f'%{topic}%')).fetchall()
            
            # If no results, try a broader search across both tables
            if not results:
                query = """
                    SELECT 'academic_' || id as doc_id, title, date, 'academic' as document_type, content
                    FROM academic_documents
                    WHERE content LIKE ? AND title IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 'chronicle_' || id as doc_id, title, date, 'chronicle' as document_type, content
                    FROM chronicle_documents
                    WHERE content LIKE ? AND title IS NOT NULL
                    
                    ORDER BY date
                """
                results = conn.execute(query, (f'%{topic}%', f'%{topic}%')).fetchall()
            
            evolution = []
            for row in results:
                # Handle the row structure - access by column name using row factory
                try:
                    doc_id = row['doc_id'] if 'doc_id' in row.keys() else row[0]
                    title = row['title'] if 'title' in row.keys() else row[1]
                    date = row['date'] if 'date' in row.keys() else row[2]
                    doc_type = row['document_type'] if 'document_type' in row.keys() else row[3]
                    content = (row['content'] if 'content' in row.keys() else row[4]) or ''
                except (IndexError, KeyError) as e:
                    # Fallback to index access
                    doc_id = row[0]
                    title = row[1] 
                    date = row[2]
                    doc_type = row[3]
                    content = row[4] if len(row) > 4 else ''
                
                # Extract relevant excerpt from content
                topic_pos = content.lower().find(topic.lower())
                excerpt = ''
                if topic_pos >= 0:
                    start = max(0, topic_pos - 100)
                    end = min(len(content), topic_pos + 200)
                    excerpt = content[start:end]
                
                evolution.append({
                    'date': date,
                    'title': title,
                    'type': doc_type,
                    'excerpt': excerpt,
                    'topic_mentioned': topic,
                    'document_id': doc_id
                })
            
            conn.close()
            return evolution
            
        except Exception as e:
            logger.error(f"Error finding research evolution for '{topic}': {e}")
            return []
    
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


def create_agent_context(query: str, db_path: str = "DB/metadata.db", 
                        graph_path: str = "KG/knowledge_graph.json") -> Dict[str, Any]:
    """
    Create enriched context for agent queries using graph + database analysis.
    
    This function analyzes the user's query and provides intelligent context by
    leveraging both the knowledge graph and database to find relevant connections,
    research evolution, and collaboration patterns.
    
    Args:
        query: The user's query to analyze
        db_path: Path to the SQLite database
        graph_path: Path to the knowledge graph JSON
        
    Returns:
        Dictionary with enriched context for the agent
    """
    try:
        enhancer = GraphEnhancedQuery(db_path, graph_path)
        
        context = {
            'query': query,
            'graph_available': enhancer.is_graph_available(),
            'graph_insights': {},
            'related_topics': [],
            'research_evolution': [],
            'collaboration_info': {},
            'semantic_connections': {},
            'key_entities': [],
            'suggested_expansions': []
        }
        
        query_lower = query.lower()
        logger.info(f"Creating agent context for query: '{query}'")
        
        # Extract key terms from query (simple tokenization)
        key_terms = [term.strip() for term in query_lower.split() 
                    if len(term.strip()) > 3 and term.strip() not in 
                    ['what', 'when', 'where', 'how', 'who', 'why', 'the', 'and', 'or', 'but']]
        
        # Find related topics for key terms
        for term in key_terms:
            related = enhancer.find_related_topics(term, max_distance=2)
            if related:
                context['related_topics'].extend(related[:3])  # Top 3 per term
        
        # Check for temporal/evolution queries
        if any(word in query_lower for word in ['evolution', 'over time', 'progress', 'development', 'history']):
            for term in key_terms:
                evolution = enhancer.find_research_evolution(term)
                if evolution:
                    context['research_evolution'].extend(evolution[:5])  # Top 5 per term
        
        # Check for relationship queries
        if any(word in query_lower for word in ['related', 'connected', 'similar', 'connection']):
            for term in key_terms:
                related = enhancer.find_related_topics(term, max_distance=3)
                context['related_topics'].extend(related[:5])
        
        # Check for project queries
        if 'project' in query_lower:
            if enhancer.is_graph_available():
                for node, data in enhancer.graph.nodes(data=True):
                    if (data.get('type') == 'project' and 
                        any(term in data.get('label', '').lower() for term in key_terms)):
                        connections = enhancer.find_project_connections(data['label'])
                        if connections:
                            context['graph_insights'][data['label']] = connections
        
        # Check for collaboration queries
        if any(word in query_lower for word in ['collaborat', 'people', 'who', 'author', 'coauthor']):
            context['collaboration_info'] = enhancer.find_collaboration_patterns()
        
        # Add key entities if graph is available
        if enhancer.is_graph_available():
            try:
                important_nodes = enhancer.get_node_importance()
                context['key_entities'] = important_nodes[:10]  # Top 10 most important
            except Exception as e:
                logger.warning(f"Could not calculate node importance: {e}")
        
        # Remove duplicates from related topics
        seen_topics = set()
        unique_topics = []
        for topic in context['related_topics']:
            topic_key = topic['topic'].lower()
            if topic_key not in seen_topics:
                unique_topics.append(topic)
                seen_topics.add(topic_key)
        context['related_topics'] = unique_topics[:10]  # Limit to top 10
        
        # Generate query expansion suggestions
        context['suggested_expansions'] = _generate_query_expansions(query, context)
        
        logger.info(f"Generated context with {len(context['related_topics'])} related topics, "
                   f"{len(context['research_evolution'])} evolution items")
        
        return context
        
    except Exception as e:
        logger.error(f"Error creating agent context: {e}")
        return {
            'query': query,
            'error': str(e),
            'graph_available': False,
            'related_topics': [],
            'research_evolution': [],
            'collaboration_info': {},
            'semantic_connections': {},
            'key_entities': [],
            'suggested_expansions': []
        }


def _generate_query_expansions(query: str, context: Dict[str, Any]) -> List[str]:
    """Generate suggested query expansions based on context."""
    expansions = []
    
    # Add related topic suggestions
    if context['related_topics']:
        top_topics = [t['topic'] for t in context['related_topics'][:3]]
        expansions.extend([
            f"How does {query.lower()} relate to {topic}?" for topic in top_topics
        ])
    
    # Add temporal suggestions if evolution data exists
    if context['research_evolution']:
        expansions.append(f"How has {query.lower()} evolved over time?")
    
    # Add collaboration suggestions
    if context['collaboration_info']:
        expansions.append(f"Who has worked on {query.lower()}?")
    
    return expansions[:5]  # Limit to 5 suggestions


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