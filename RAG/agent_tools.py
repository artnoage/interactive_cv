#!/usr/bin/env python3
"""
Consolidated tools for the Interactive CV agent.
These tools provide all the functionality needed to answer questions about the CV content.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from RAG import semantic_search
from RAG.graph_enhanced_query import GraphEnhancedQuery


class InteractiveCVTools:
    """Complete toolset for the Interactive CV agent."""
    
    def __init__(self, db_path: str = "DB/metadata.db", graph_path: str = "KG/knowledge_graph.json"):
        self.db_path = db_path
        self.graph_path = graph_path
        self._graph_enhancer = None
        
    def _get_connection(self):
        """Get a new database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @property
    def graph_enhancer(self):
        """Lazy load graph enhancer."""
        if self._graph_enhancer is None:
            try:
                self._graph_enhancer = GraphEnhancedQuery(self.db_path, self.graph_path)
            except:
                pass
        return self._graph_enhancer
    
    # ========== Paper Search Tools ==========
    
    def search_academic_papers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for academic papers by keywords in title or content.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of papers with title, date, and content preview
        """
        conn = self._get_connection()
        results = []
        
        try:
            sql_query = """
            SELECT id, title, date, domain, 
                   SUBSTR(content, 1, 1500) as content_preview
            FROM academic_documents
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY 
                CASE WHEN title LIKE ? THEN 0 ELSE 1 END,
                date DESC
            LIMIT ?
            """
            
            search_pattern = f"%{query}%"
            cursor = conn.execute(sql_query, (search_pattern, search_pattern, search_pattern, limit))
            
            for row in cursor:
                results.append({
                    "id": row["id"],
                    "doc_id": f"academic_{row['id']}",
                    "title": row["title"],
                    "date": row["date"],
                    "domain": row["domain"],
                    "content_preview": row["content_preview"]
                })
                
        finally:
            conn.close()
            
        return results
    
    def get_paper_content(self, paper_title: str, max_length: int = None) -> Dict[str, Any]:
        """
        Get full or partial content of a specific paper.
        
        Args:
            paper_title: Title or partial title of the paper
            max_length: Maximum content length to return
            
        Returns:
            Paper details with content
        """
        conn = self._get_connection()
        result = None
        
        try:
            query = """
            SELECT id, title, date, domain, content
            FROM academic_documents
            WHERE title LIKE ?
            LIMIT 1
            """
            
            cursor = conn.execute(query, (f"%{paper_title}%",))
            row = cursor.fetchone()
            
            if row:
                content = row["content"]
                if max_length and content and len(content) > max_length:
                    content = content[:max_length] + "..."
                    
                result = {
                    "id": row["id"],
                    "doc_id": f"academic_{row['id']}",
                    "title": row["title"],
                    "date": row["date"],
                    "domain": row["domain"],
                    "content": content
                }
                
        finally:
            conn.close()
            
        return result
    
    def get_paper_authors(self, paper_title: str) -> List[Dict[str, Any]]:
        """
        Get authors of a specific paper.
        
        Args:
            paper_title: Title or partial title of the paper
            
        Returns:
            List of authors with their affiliations
        """
        conn = self._get_connection()
        results = []
        
        try:
            # First find the paper
            paper_query = "SELECT id FROM academic_documents WHERE title LIKE ?"
            cursor = conn.execute(paper_query, (f"%{paper_title}%",))
            paper = cursor.fetchone()
            
            if paper:
                doc_id = f"academic_{paper['id']}"
                
                # Get authors
                author_query = """
                SELECT DISTINCT p.name, p.role, p.affiliation
                FROM people p
                JOIN relationships r ON p.id = r.target_id
                WHERE r.source_id = ? 
                AND r.source_type = 'document'
                AND r.target_type = 'person'
                AND r.relationship_type = 'authored_by'
                ORDER BY p.name
                """
                
                cursor = conn.execute(author_query, (doc_id,))
                
                for row in cursor:
                    results.append({
                        "name": row["name"],
                        "role": row["role"] or "author",
                        "affiliation": row["affiliation"] or "Not specified"
                    })
                    
        finally:
            conn.close()
            
        return results
    
    # ========== Chronicle/Notes Search Tools ==========
    
    def search_chronicle_notes(self, query: str, date_range: Tuple[str, str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search personal/chronicle notes.
        
        Args:
            query: Search query
            date_range: Optional tuple of (start_date, end_date) in YYYY-MM-DD format
            limit: Maximum number of results
            
        Returns:
            List of matching chronicle entries
        """
        conn = self._get_connection()
        results = []
        
        try:
            sql_query = """
            SELECT id, title, date, note_type, content
            FROM chronicle_documents
            WHERE (title LIKE ? OR content LIKE ?)
            """
            
            params = [f"%{query}%", f"%{query}%"]
            
            if date_range:
                sql_query += " AND date BETWEEN ? AND ?"
                params.extend(date_range)
                
            sql_query += " ORDER BY date DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(sql_query, params)
            
            for row in cursor:
                # Extract context around query
                content = row["content"]
                context = content[:1500]  # Default to first 1500 chars
                
                if query.lower() in content.lower():
                    idx = content.lower().find(query.lower())
                    start = max(0, idx - 500)
                    end = min(len(content), idx + 1000)
                    context = "..." + content[start:end] + "..."
                
                results.append({
                    "id": row["id"],
                    "doc_id": f"chronicle_{row['id']}",
                    "title": row["title"],
                    "date": row["date"],
                    "note_type": row["note_type"],
                    "context": context
                })
                
        finally:
            conn.close()
            
        return results
    
    # ========== Topic/Entity Search Tools ==========
    
    def find_research_topics(self, query: str, category: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Find research topics and concepts.
        
        Args:
            query: Search query
            category: Optional category filter (e.g., 'math_foundation', 'innovation')
            limit: Maximum number of results
            
        Returns:
            List of topics with their categories and descriptions
        """
        conn = self._get_connection()
        results = []
        
        try:
            sql_query = """
            SELECT t.id, t.name, t.category, t.description,
                   COUNT(DISTINCT r.source_id) as mention_count
            FROM topics t
            LEFT JOIN relationships r ON t.id = r.target_id AND r.target_type = 'topic'
            WHERE (t.name LIKE ? OR t.description LIKE ?)
            """
            
            params = [f"%{query}%", f"%{query}%"]
            
            if category:
                sql_query += " AND t.category = ?"
                params.append(category)
                
            sql_query += " GROUP BY t.id ORDER BY mention_count DESC, t.name LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(sql_query, params)
            
            for row in cursor:
                results.append({
                    "id": row["id"],
                    "name": row["name"],
                    "category": row["category"],
                    "description": row["description"],
                    "mention_count": row["mention_count"]
                })
                
        finally:
            conn.close()
            
        return results
    
    def find_methods(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Find methods and algorithms.
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of methods with descriptions
        """
        conn = self._get_connection()
        results = []
        
        try:
            sql_query = """
            SELECT m.id, m.name, m.category, m.description
            FROM methods m
            WHERE (m.name LIKE ? OR m.description LIKE ?)
            """
            
            params = [f"%{query}%", f"%{query}%"]
            
            if category:
                sql_query += " AND m.category = ?"
                params.append(category)
                
            sql_query += " ORDER BY m.name"
            
            cursor = conn.execute(sql_query, params)
            
            for row in cursor:
                results.append({
                    "id": row["id"],
                    "name": row["name"],
                    "category": row["category"],
                    "description": row["description"]
                })
                
        finally:
            conn.close()
            
        return results
    
    # ========== Evolution & Connection Tools ==========
    
    def get_research_evolution(self, topic: str) -> List[Dict[str, Any]]:
        """
        Track how a research topic evolved over time.
        
        Args:
            topic: Research topic to track
            
        Returns:
            List of papers/notes mentioning the topic in chronological order
        """
        conn = self._get_connection()
        results = []
        
        try:
            # Find topic IDs
            topic_query = """
            SELECT id FROM topics 
            WHERE name LIKE ? OR description LIKE ?
            """
            cursor = conn.execute(topic_query, (f"%{topic}%", f"%{topic}%"))
            topic_ids = [row["id"] for row in cursor]
            
            if topic_ids:
                # Find documents discussing these topics
                placeholders = ",".join("?" * len(topic_ids))
                doc_query = f"""
                SELECT DISTINCT 
                    CASE 
                        WHEN r.source_type = 'document' AND r.source_id LIKE 'academic_%' THEN 'academic'
                        WHEN r.source_type = 'document' AND r.source_id LIKE 'chronicle_%' THEN 'chronicle'
                    END as doc_type,
                    CAST(SUBSTR(r.source_id, INSTR(r.source_id, '_') + 1) AS INTEGER) as doc_id,
                    a.title as academic_title, a.date as academic_date,
                    c.title as chronicle_title, c.date as chronicle_date
                FROM relationships r
                LEFT JOIN academic_documents a ON r.source_id = 'academic_' || a.id
                LEFT JOIN chronicle_documents c ON r.source_id = 'chronicle_' || c.id
                WHERE r.target_id IN ({placeholders})
                AND r.target_type = 'topic'
                ORDER BY COALESCE(a.date, c.date)
                """
                
                cursor = conn.execute(doc_query, topic_ids)
                
                for row in cursor:
                    if row["doc_type"] == "academic":
                        results.append({
                            "type": "academic",
                            "title": row["academic_title"],
                            "date": row["academic_date"],
                            "doc_id": f"academic_{row['doc_id']}"
                        })
                    elif row["doc_type"] == "chronicle":
                        results.append({
                            "type": "chronicle",
                            "title": row["chronicle_title"],
                            "date": row["chronicle_date"],
                            "doc_id": f"chronicle_{row['doc_id']}"
                        })
                        
        finally:
            conn.close()
            
        return results
    
    def find_project_connections(self, project_name: str) -> Dict[str, Any]:
        """
        Find all connections related to a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Dictionary with people, topics, methods, and papers connected to the project
        """
        conn = self._get_connection()
        connections = {
            "project_info": None,
            "people": [],
            "topics": [],
            "methods": [],
            "papers": [],
            "notes": []
        }
        
        try:
            # Find project
            proj_query = "SELECT * FROM projects WHERE name LIKE ?"
            cursor = conn.execute(proj_query, (f"%{project_name}%",))
            project = cursor.fetchone()
            
            if project:
                connections["project_info"] = {
                    "name": project["name"],
                    "description": project["description"],
                    "start_date": project["start_date"],
                    "end_date": project["end_date"],
                    "status": project["status"]
                }
                
                # Find all relationships where project is involved
                rel_query = """
                SELECT r.*, 
                       t.name as topic_name, t.category as topic_cat,
                       p.name as person_name, p.affiliation,
                       m.name as method_name, m.category as method_cat
                FROM relationships r
                LEFT JOIN topics t ON r.target_type = 'topic' AND r.target_id = t.id
                LEFT JOIN people p ON r.target_type = 'person' AND r.target_id = p.id
                LEFT JOIN methods m ON r.target_type = 'method' AND r.target_id = m.id
                WHERE (r.source_id = ? AND r.source_type = 'project')
                   OR (r.target_id = ? AND r.target_type = 'project')
                """
                
                cursor = conn.execute(rel_query, (project["id"], project["id"]))
                
                for row in cursor:
                    if row["target_type"] == "topic" and row["topic_name"]:
                        connections["topics"].append({
                            "name": row["topic_name"],
                            "category": row["topic_cat"]
                        })
                    elif row["target_type"] == "person" and row["person_name"]:
                        connections["people"].append({
                            "name": row["person_name"],
                            "affiliation": row["affiliation"]
                        })
                    elif row["target_type"] == "method" and row["method_name"]:
                        connections["methods"].append({
                            "name": row["method_name"],
                            "category": row["method_cat"]
                        })
                        
        finally:
            conn.close()
            
        return connections
    
    def get_collaborations(self, person_name: str = None) -> List[Dict[str, Any]]:
        """
        Find collaboration patterns.
        
        Args:
            person_name: Optional person to focus on
            
        Returns:
            List of collaborations with co-authors and papers
        """
        conn = self._get_connection()
        results = []
        
        try:
            if person_name:
                # Find specific person's collaborations
                query = """
                SELECT DISTINCT p2.name as collaborator, COUNT(DISTINCT r1.source_id) as paper_count
                FROM people p1
                JOIN relationships r1 ON p1.id = r1.target_id AND r1.target_type = 'person'
                JOIN relationships r2 ON r1.source_id = r2.source_id AND r2.target_type = 'person'
                JOIN people p2 ON r2.target_id = p2.id
                WHERE p1.name LIKE ? AND p2.name NOT LIKE ?
                AND r1.relationship_type = 'authored_by'
                AND r2.relationship_type = 'authored_by'
                GROUP BY p2.name
                ORDER BY paper_count DESC
                """
                
                pattern = f"%{person_name}%"
                cursor = conn.execute(query, (pattern, pattern))
                
                for row in cursor:
                    results.append({
                        "collaborator": row["collaborator"],
                        "paper_count": row["paper_count"]
                    })
            else:
                # Get all collaborations
                query = """
                SELECT p1.name as author1, p2.name as author2, COUNT(DISTINCT r1.source_id) as paper_count
                FROM relationships r1
                JOIN relationships r2 ON r1.source_id = r2.source_id
                JOIN people p1 ON r1.target_id = p1.id
                JOIN people p2 ON r2.target_id = p2.id
                WHERE r1.target_type = 'person' AND r2.target_type = 'person'
                AND r1.relationship_type = 'authored_by' AND r2.relationship_type = 'authored_by'
                AND p1.id < p2.id
                GROUP BY p1.id, p2.id
                HAVING paper_count > 1
                ORDER BY paper_count DESC
                LIMIT 20
                """
                
                cursor = conn.execute(query)
                
                for row in cursor:
                    results.append({
                        "author1": row["author1"],
                        "author2": row["author2"],
                        "paper_count": row["paper_count"]
                    })
                    
        finally:
            conn.close()
            
        return results
    
    # ========== Semantic Search Tools ==========
    
    def semantic_search_chunks(self, query: str, limit: int = 10, doc_type: str = None, 
                              similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Search document chunks using semantic similarity.
        
        Args:
            query: Search query
            limit: Maximum number of results
            doc_type: Filter by document type ('academic' or 'chronicle')
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of semantically similar chunks
        """
        try:
            return semantic_search.semantic_search_chunks(
                self.db_path, 
                query, 
                limit=limit,
                doc_type=doc_type,
                similarity_threshold=similarity_threshold
            )
        except Exception as e:
            print(f"Semantic search error: {e}")
            return []
    
    def find_similar_entities(self, query: str, entity_type: str = None, 
                            limit: int = 15, similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find entities similar to the query.
        
        Args:
            query: Search query
            entity_type: Filter by entity type
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of similar entities
        """
        try:
            return semantic_search.find_similar_entities(
                self.db_path,
                query,
                entity_type=entity_type,
                limit=limit,
                similarity_threshold=similarity_threshold
            )
        except Exception as e:
            print(f"Entity search error: {e}")
            return []
    
    # ========== Institution Tools ==========
    
    def get_all_institutions(self) -> List[Dict[str, Any]]:
        """
        Get all institutions in the database.
        
        Returns:
            List of institutions with their details
        """
        conn = self._get_connection()
        results = []
        
        try:
            query = """
            SELECT i.*, COUNT(DISTINCT r.source_id) as mention_count
            FROM institutions i
            LEFT JOIN relationships r ON i.id = r.target_id AND r.target_type = 'institution'
            GROUP BY i.id
            ORDER BY mention_count DESC, i.name
            """
            
            cursor = conn.execute(query)
            
            for row in cursor:
                results.append({
                    "id": row["id"],
                    "name": row["name"],
                    "type": row["type"],
                    "location": row["location"],
                    "mention_count": row["mention_count"]
                })
                
        finally:
            conn.close()
            
        return results
    
    def get_author_affiliations(self, author_name: str) -> List[Dict[str, Any]]:
        """
        Get all recorded affiliations for an author.
        
        Args:
            author_name: Name or partial name of the author
            
        Returns:
            List of author records with affiliations
        """
        conn = self._get_connection()
        results = []
        
        try:
            query = """
            SELECT DISTINCT name, role, affiliation
            FROM people
            WHERE name LIKE ?
            ORDER BY name
            """
            
            cursor = conn.execute(query, (f"%{author_name}%",))
            
            for row in cursor:
                if row["affiliation"]:
                    results.append({
                        "name": row["name"],
                        "role": row["role"],
                        "affiliation": row["affiliation"]
                    })
                    
        finally:
            conn.close()
            
        return results


# ========== Tool Wrappers for Agent Use ==========
# These match the expected interface for the interactive agent

def search_academic_papers(query: str) -> List[Dict[str, Any]]:
    """Search for academic papers by keyword."""
    tools = InteractiveCVTools()
    return tools.search_academic_papers(query)

def get_paper_content(paper_title: str) -> Dict[str, Any]:
    """Get content of a specific paper."""
    tools = InteractiveCVTools()
    return tools.get_paper_content(paper_title)

def search_chronicle_notes(query: str) -> List[Dict[str, Any]]:
    """Search personal/chronicle notes."""
    tools = InteractiveCVTools()
    return tools.search_chronicle_notes(query)

def find_research_topics(query: str) -> List[Dict[str, Any]]:
    """Find research topics and concepts."""
    tools = InteractiveCVTools()
    return tools.find_research_topics(query)

def get_research_evolution(topic: str) -> List[Dict[str, Any]]:
    """Track research evolution over time."""
    tools = InteractiveCVTools()
    return tools.get_research_evolution(topic)

def find_project_connections(project: str) -> Dict[str, Any]:
    """Find connections to a project."""
    tools = InteractiveCVTools()
    return tools.find_project_connections(project)

def semantic_search_chunks(query: str, limit: int = 10, doc_type: str = None, 
                          similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """Semantic search across document chunks."""
    tools = InteractiveCVTools()
    return tools.semantic_search_chunks(query, limit=limit, doc_type=doc_type, 
                                       similarity_threshold=similarity_threshold)

def get_collaborations(person: str = None) -> List[Dict[str, Any]]:
    """Find collaboration patterns."""
    tools = InteractiveCVTools()
    return tools.get_collaborations(person)


if __name__ == "__main__":
    # Quick test
    print("Testing agent tools...")
    results = search_academic_papers("UNOT")
    print(f"Found {len(results)} papers about UNOT")
    if results:
        print(f"First result: {results[0]['title']}")
        
        # Get authors
        tools = InteractiveCVTools()
        authors = tools.get_paper_authors(results[0]['title'])
        print(f"Authors: {', '.join([a['name'] for a in authors])}")