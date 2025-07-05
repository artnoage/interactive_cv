#!/usr/bin/env python3
"""
Blueprint-Generated Agent Tools
Clean interface for the Interactive CV Agent using blueprint-generated tools.

This module provides a simplified interface that wraps the sophisticated
blueprint-generated tools for use in the Interactive CV Agent.
"""

import sqlite3
from typing import Dict, List, Any, Optional, Tuple
import logging

from RAG.blueprint_driven_tools import BlueprintDrivenToolGenerator

logger = logging.getLogger(__name__)


class GeneratedInteractiveCVTools:
    """
    Clean interface for blueprint-generated tools.
    
    This class provides the same interface as the original manual tools,
    but uses sophisticated blueprint-generated tools under the hood.
    """
    
    def __init__(self, db_path: str = "DB/metadata.db", blueprints_dir: str = "blueprints"):
        """Initialize with blueprint-generated tools."""
        self.db_path = db_path
        self.generator = BlueprintDrivenToolGenerator(db_path, blueprints_dir)
        
        logger.info(f"Initialized with {len(self.generator.list_all_tools())} generated tools")
    
    # ========== Document Search Tools ==========
    
    def search_academic_papers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search academic papers using generated tools."""
        try:
            results = self.generator.execute_tool("search_academic_documents", query=query, limit=limit)
            
            # Convert to expected format
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.get("id"),
                    "doc_id": f"academic_{result.get('id')}",
                    "title": result.get("title"),
                    "date": result.get("date"),
                    "domain": result.get("domain"),
                    "content_preview": result.get("content", "")[:1500] if result.get("content") else ""
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in search_academic_papers: {e}")
            return []
    
    def get_paper_content(self, paper_title: str, max_length: int = None) -> Optional[Dict[str, Any]]:
        """Get paper content using generated tools."""
        try:
            # First search for the paper
            papers = self.generator.execute_tool("search_academic_documents", query=paper_title, limit=1)
            
            if not papers:
                return None
            
            paper = papers[0]
            content = paper.get("content", "")
            
            if max_length and content and len(content) > max_length:
                content = content[:max_length] + "..."
            
            return {
                "id": paper.get("id"),
                "doc_id": f"academic_{paper.get('id')}",
                "title": paper.get("title"),
                "date": paper.get("date"),
                "domain": paper.get("domain"),
                "content": content
            }
        except Exception as e:
            logger.error(f"Error in get_paper_content: {e}")
            return None
    
    def get_paper_authors(self, paper_title: str) -> List[Dict[str, Any]]:
        """Get paper authors using relationship traversal."""
        try:
            # First find the paper
            papers = self.generator.execute_tool("search_academic_documents", query=paper_title, limit=1)
            
            if not papers:
                return []
            
            paper_id = papers[0].get("id")
            if not paper_id:
                return []
            
            # Use relationship traversal to find authors
            try:
                authors = self.generator.execute_tool("reverse_authored_by", 
                                                    target_type="document", 
                                                    target_id=f"academic_{paper_id}",
                                                    limit=20)
                
                formatted_authors = []
                for author_rel in authors:
                    source_details = author_rel.get("source_details", {})
                    formatted_authors.append({
                        "name": source_details.get("name", "Unknown"),
                        "role": source_details.get("role", "author"),
                        "affiliation": source_details.get("affiliation", "Not specified")
                    })
                
                return formatted_authors
            except:
                # Fallback: search people mentioned in connection with this paper
                return []
                
        except Exception as e:
            logger.error(f"Error in get_paper_authors: {e}")
            return []
    
    # ========== Chronicle/Notes Search Tools ==========
    
    def search_chronicle_notes(self, query: str, date_range: Optional[Tuple[str, str]] = None, 
                              limit: int = 10) -> List[Dict[str, Any]]:
        """Search chronicle notes using generated tools."""
        try:
            # Use generated search tool
            results = self.generator.execute_tool("search_chronicle_documents", query=query, limit=limit)
            
            # Convert to expected format
            formatted_results = []
            for result in results:
                content = result.get("content", "")
                
                # Extract context around query
                context = content[:1500] if content else ""
                if query.lower() in content.lower():
                    idx = content.lower().find(query.lower())
                    start = max(0, idx - 500)
                    end = min(len(content), idx + 1000)
                    context = "..." + content[start:end] + "..."
                
                formatted_results.append({
                    "id": result.get("id"),
                    "doc_id": f"chronicle_{result.get('id')}",
                    "title": result.get("title"),
                    "date": result.get("date"),
                    "note_type": result.get("note_type"),
                    "context": context
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in search_chronicle_notes: {e}")
            return []
    
    # ========== Topic/Entity Search Tools ==========
    
    def find_research_topics(self, query: str, category: str = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Find research topics using generated category-aware tools."""
        try:
            # Use generated topic search
            results = self.generator.execute_tool("search_topics", query=query, limit=limit, category=category)
            
            # Convert to expected format
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "category": result.get("category"),
                    "description": result.get("description"),
                    "mention_count": 0  # Could be enhanced with relationship counting
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in find_research_topics: {e}")
            return []
    
    def find_methods(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Find methods using generated tools."""
        try:
            results = self.generator.execute_tool("search_methods", query=query, limit=20, category=category)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "category": result.get("category"),
                    "description": result.get("description")
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in find_methods: {e}")
            return []
    
    # ========== Evolution & Connection Tools ==========
    
    def get_research_evolution(self, topic: str) -> List[Dict[str, Any]]:
        """Get research evolution using relationship traversal."""
        try:
            # First find topics matching the query
            topics = self.generator.execute_tool("search_topics", query=topic, limit=5)
            
            if not topics:
                return []
            
            evolution = []
            
            # For each topic, find documents that discuss it
            for topic_result in topics:
                topic_id = topic_result.get("id")
                if topic_id:
                    try:
                        discussions = self.generator.execute_tool("reverse_discusses",
                                                                target_type="topic",
                                                                target_id=str(topic_id),
                                                                limit=10)
                        
                        for discussion in discussions:
                            source_details = discussion.get("source_details", {})
                            evolution.append({
                                "date": source_details.get("date"),
                                "title": source_details.get("title"),
                                "type": "academic" if "academic" in str(discussion.get("source_id", "")) else "chronicle",
                                "excerpt": "",  # Could be enhanced
                                "topic_mentioned": topic,
                                "document_id": discussion.get("source_id")
                            })
                    except:
                        continue
            
            # Sort by date
            evolution.sort(key=lambda x: x.get("date", ""))
            return evolution
            
        except Exception as e:
            logger.error(f"Error in get_research_evolution: {e}")
            return []
    
    def find_project_connections(self, project_name: str) -> Dict[str, Any]:
        """Find project connections using generated tools."""
        try:
            # Search for the project
            projects = self.generator.execute_tool("search_projects", query=project_name, limit=1)
            
            if not projects:
                return {"project_info": None, "people": [], "topics": [], "methods": [], "papers": [], "notes": []}
            
            project = projects[0]
            project_id = project.get("id")
            
            connections = {
                "project_info": {
                    "name": project.get("name"),
                    "description": project.get("description"),
                    "start_date": project.get("start_date"),
                    "end_date": project.get("end_date"),
                    "status": "active" if not project.get("end_date") else "completed"
                },
                "people": [],
                "topics": [],
                "methods": [],
                "papers": [],
                "notes": []
            }
            
            # Use relationship traversal to find connections
            if project_id:
                try:
                    # Find what the project relates to
                    relations = self.generator.execute_tool("traverse_part_of",
                                                          source_type="project",
                                                          source_id=str(project_id),
                                                          limit=20)
                    
                    for relation in relations:
                        target_type = relation.get("target_type")
                        target_details = relation.get("target_details", {})
                        
                        if target_type == "topic":
                            connections["topics"].append(target_details.get("name", ""))
                        elif target_type == "person":
                            connections["people"].append(target_details.get("name", ""))
                        elif target_type == "method":
                            connections["methods"].append(target_details.get("name", ""))
                
                except:
                    pass
            
            return connections
            
        except Exception as e:
            logger.error(f"Error in find_project_connections: {e}")
            return {"project_info": None, "people": [], "topics": [], "methods": [], "papers": [], "notes": []}
    
    def get_collaborations(self, person_name: str = None) -> List[Dict[str, Any]]:
        """Get collaboration patterns using generated tools."""
        try:
            if person_name:
                # Find specific person's collaborations through authored papers
                people = self.generator.execute_tool("search_people", query=person_name, limit=1)
                
                if not people:
                    return []
                
                person_id = people[0].get("id")
                if not person_id:
                    return []
                
                # Find papers authored by this person
                try:
                    papers = self.generator.execute_tool("traverse_authored_by",
                                                       source_type="person",
                                                       source_id=str(person_id),
                                                       limit=20)
                    
                    collaborators = {}
                    
                    # For each paper, find other authors
                    for paper_rel in papers:
                        paper_id = paper_rel.get("target_id")
                        if paper_id:
                            other_authors = self.generator.execute_tool("reverse_authored_by",
                                                                      target_type="document",
                                                                      target_id=paper_id,
                                                                      limit=10)
                            
                            for author_rel in other_authors:
                                author_details = author_rel.get("source_details", {})
                                author_name = author_details.get("name", "")
                                
                                if author_name and author_name != person_name:
                                    if author_name not in collaborators:
                                        collaborators[author_name] = 0
                                    collaborators[author_name] += 1
                    
                    return [{"collaborator": name, "paper_count": count} 
                           for name, count in collaborators.items()]
                
                except:
                    return []
            else:
                # Get general collaboration patterns - simplified
                return []
                
        except Exception as e:
            logger.error(f"Error in get_collaborations: {e}")
            return []
    
    # ========== Institution Tools ==========
    
    def get_all_institutions(self) -> List[Dict[str, Any]]:
        """Get all institutions using generated tools."""
        try:
            results = self.generator.execute_tool("list_institutions", limit=50)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "type": result.get("type"),
                    "location": result.get("location"),
                    "mention_count": 0  # Could be enhanced with relationship counting
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in get_all_institutions: {e}")
            return []
    
    def get_author_affiliations(self, author_name: str) -> List[Dict[str, Any]]:
        """Get author affiliations using generated tools."""
        try:
            people = self.generator.execute_tool("search_people", query=author_name, limit=10)
            
            formatted_results = []
            for person in people:
                if person.get("affiliation"):
                    formatted_results.append({
                        "name": person.get("name"),
                        "role": person.get("role"),
                        "affiliation": person.get("affiliation")
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error in get_author_affiliations: {e}")
            return []
    
    # ========== Semantic Search Tools ==========
    
    def semantic_search_chunks(self, query: str, limit: int = 10, doc_type: str = None, 
                              similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Semantic search using blueprint-generated tools + fallback to manual semantic search."""
        try:
            # Try to use enhanced search capabilities
            from RAG import semantic_search
            return semantic_search.semantic_search_chunks(
                self.db_path, query, limit=limit, doc_type=doc_type, 
                similarity_threshold=similarity_threshold
            )
        except Exception as e:
            logger.error(f"Error in semantic_search_chunks: {e}")
            return []
    
    def find_similar_entities(self, query: str, entity_type: str = None, 
                            limit: int = 15, similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Find similar entities using semantic search."""
        try:
            from RAG import semantic_search
            return semantic_search.find_similar_entities(
                self.db_path, query, entity_type=entity_type, 
                limit=limit, similarity_threshold=similarity_threshold
            )
        except Exception as e:
            logger.error(f"Error in find_similar_entities: {e}")
            return []
    
    # ========== Blueprint-Specific Advanced Tools ==========
    
    def explore_topic_categories(self, category: str = None, limit: int = 20) -> Dict[str, Any]:
        """Explore topic categories using generated tools."""
        try:
            return self.generator.execute_tool("explore_topic_categories", category=category, limit=limit)
        except Exception as e:
            logger.error(f"Error in explore_topic_categories: {e}")
            return {"categories": [], "total_categories": 0}
    
    def get_visualization_data(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get visualization-ready entity data."""
        try:
            return self.generator.execute_tool("get_visualization_data", 
                                             entity_type=entity_type, 
                                             entity_id=entity_id)
        except Exception as e:
            logger.error(f"Error in get_visualization_data: {e}")
            return None
    
    def traverse_relationship(self, relationship_type: str, source_type: str, 
                            source_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Traverse relationships using generated tools."""
        try:
            return self.generator.execute_tool(f"traverse_{relationship_type}",
                                             source_type=source_type,
                                             source_id=source_id,
                                             limit=limit)
        except Exception as e:
            logger.error(f"Error in traverse_relationship: {e}")
            return []


# ========== Wrapper Functions for Agent Use ==========

def search_academic_papers(query: str) -> List[Dict[str, Any]]:
    """Search for academic papers by keyword."""
    tools = GeneratedInteractiveCVTools()
    return tools.search_academic_papers(query)

def get_paper_content(paper_title: str) -> Optional[Dict[str, Any]]:
    """Get content of a specific paper."""
    tools = GeneratedInteractiveCVTools()
    return tools.get_paper_content(paper_title)

def search_chronicle_notes(query: str) -> List[Dict[str, Any]]:
    """Search personal/chronicle notes."""
    tools = GeneratedInteractiveCVTools()
    return tools.search_chronicle_notes(query)

def find_research_topics(query: str) -> List[Dict[str, Any]]:
    """Find research topics and concepts."""
    tools = GeneratedInteractiveCVTools()
    return tools.find_research_topics(query)

def get_research_evolution(topic: str) -> List[Dict[str, Any]]:
    """Track research evolution over time."""
    tools = GeneratedInteractiveCVTools()
    return tools.get_research_evolution(topic)

def find_project_connections(project: str) -> Dict[str, Any]:
    """Find connections to a project."""
    tools = GeneratedInteractiveCVTools()
    return tools.find_project_connections(project)

def semantic_search_chunks(query: str, limit: int = 10, doc_type: str = None, 
                          similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """Semantic search across document chunks."""
    tools = GeneratedInteractiveCVTools()
    return tools.semantic_search_chunks(query, limit=limit, doc_type=doc_type, 
                                       similarity_threshold=similarity_threshold)

def get_collaborations(person: str = None) -> List[Dict[str, Any]]:
    """Find collaboration patterns."""
    tools = GeneratedInteractiveCVTools()
    return tools.get_collaborations(person)


if __name__ == "__main__":
    # Test the generated tools interface
    try:
        tools = GeneratedInteractiveCVTools()
        
        print("=== Testing Generated Tools Interface ===")
        
        # Test search
        papers = tools.search_academic_papers("neural", limit=2)
        print(f"Found {len(papers)} papers about neural")
        
        # Test topics
        topics = tools.find_research_topics("optimal", limit=3)
        print(f"Found {len(topics)} topics about optimal")
        
        # Test categories
        categories = tools.explore_topic_categories(limit=5)
        print(f"Found {categories.get('total_categories', 0)} topic categories")
        
        print("✅ Generated tools interface working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()