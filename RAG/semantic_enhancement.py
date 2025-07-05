#!/usr/bin/env python3
"""
Semantic Enhancement Engine
Provides hybrid semantic search capabilities for blueprint-generated tools.

This module implements intelligent query enhancement using embeddings while
maintaining the blueprint-driven architecture. It enables semantic intelligence
to improve search precision without hardcoding domain knowledge.
"""

import sqlite3
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
import logging
from dataclasses import dataclass

from RAG.semantic_search import (
    semantic_search_chunks, 
    find_similar_entities,
    generate_embedding,
    cosine_similarity
)

logger = logging.getLogger(__name__)


@dataclass 
class SemanticResult:
    """Result from semantic search with score and metadata."""
    content: Dict[str, Any]
    similarity: float
    source: str  # 'semantic' or 'sql'
    entity_type: Optional[str] = None


@dataclass
class EnhancedQuery:
    """Query enhanced with semantic expansion terms."""
    original_query: str
    expanded_terms: List[str]
    enhanced_query: str
    expansion_confidence: float


class SemanticEnhancementEngine:
    """
    Provides semantic intelligence for blueprint-generated tools.
    
    This engine enhances SQL-based tools with semantic search capabilities,
    query expansion, and intelligent result merging while maintaining
    full compatibility with the blueprint-driven architecture.
    """
    
    def __init__(self, db_path: str, semantic_config: Dict[str, Any]):
        """Initialize with database and semantic configuration."""
        self.db_path = db_path
        self.config = semantic_config
        self.semantic_enabled = semantic_config.get('semantic_config', {}).get('query_enhancement', {}).get('enabled', True)
        
        # Cache for embeddings and expansions
        self._embedding_cache: Dict[str, np.ndarray] = {}
        self._expansion_cache: Dict[str, List[str]] = {}
        
        logger.info(f"Semantic enhancement engine initialized (enabled: {self.semantic_enabled})")
    
    def enhance_search_function(self, original_function: Callable, tool_name: str) -> Callable:
        """
        Enhance a blueprint-generated search function with semantic capabilities.
        
        Args:
            original_function: The original SQL-based search function
            tool_name: Name of the tool for configuration lookup
            
        Returns:
            Enhanced function that combines SQL and semantic search
        """
        # Get enhancement configuration for this tool
        tool_config = self.config.get('tool_enhancements', {}).get(tool_name, {})
        
        if not tool_config.get('semantic_enabled', False) or not self.semantic_enabled:
            # Return original function if semantic enhancement disabled
            return original_function
        
        enhancement_type = tool_config.get('enhancement_type', 'query_expansion')
        
        if enhancement_type == 'hybrid_search':
            return self._create_hybrid_search_function(original_function, tool_config)
        elif enhancement_type == 'query_expansion':
            return self._create_query_expansion_function(original_function, tool_config)
        else:
            return original_function
    
    def _create_hybrid_search_function(self, original_function: Callable, tool_config: Dict[str, Any]) -> Callable:
        """Create hybrid search function that combines SQL and semantic results."""
        
        def hybrid_search(*args, **kwargs) -> List[Dict[str, Any]]:
            """Enhanced search function with hybrid SQL + semantic capabilities."""
            
            # Extract query parameter
            query = self._extract_query_param(args, kwargs)
            if not query:
                return original_function(*args, **kwargs)
            
            limit = kwargs.get('limit', 10)
            semantic_weight = tool_config.get('semantic_weight', 0.6)
            sql_weight = tool_config.get('sql_weight', 0.4)
            
            # Run both searches in parallel
            sql_results = []
            semantic_results = []
            
            try:
                # Get SQL results
                sql_results = original_function(*args, **kwargs)
                sql_results = [SemanticResult(content=r, similarity=1.0, source='sql') 
                              for r in sql_results]
                
                # Get semantic results
                semantic_results = self._get_semantic_results(query, tool_config, limit)
                
            except Exception as e:
                logger.warning(f"Error in hybrid search: {e}")
                # Fallback to SQL only
                return [r.content for r in sql_results] if sql_results else original_function(*args, **kwargs)
            
            # Merge and rank results
            merged_results = self._merge_results(sql_results, semantic_results, 
                                                sql_weight, semantic_weight, limit)
            
            return [r.content for r in merged_results]
        
        return hybrid_search
    
    def _create_query_expansion_function(self, original_function: Callable, tool_config: Dict[str, Any]) -> Callable:
        """Create query expansion function that enhances search terms."""
        
        def expanded_search(*args, **kwargs) -> List[Dict[str, Any]]:
            """Enhanced search function with semantic query expansion."""
            
            # Extract and expand query
            query = self._extract_query_param(args, kwargs)
            if not query:
                return original_function(*args, **kwargs)
            
            try:
                enhanced_query = self._expand_query(query, tool_config)
                
                # Update kwargs with enhanced query
                if 'query' in kwargs:
                    kwargs['query'] = enhanced_query.enhanced_query
                elif len(args) > 0:
                    # Assume first arg is query
                    args = (enhanced_query.enhanced_query,) + args[1:]
                
                logger.debug(f"Expanded query: '{query}' → '{enhanced_query.enhanced_query}'")
                
            except Exception as e:
                logger.warning(f"Query expansion failed: {e}")
                # Continue with original query
            
            return original_function(*args, **kwargs)
        
        return expanded_search
    
    def _extract_query_param(self, args: tuple, kwargs: dict) -> Optional[str]:
        """Extract query parameter from function arguments."""
        if 'query' in kwargs:
            return kwargs['query']
        elif len(args) > 0 and isinstance(args[0], str):
            return args[0]
        return None
    
    def _expand_query(self, query: str, tool_config: Dict[str, Any]) -> EnhancedQuery:
        """Expand query using semantic similarity."""
        
        # Check cache first
        if query in self._expansion_cache:
            cached_terms = self._expansion_cache[query]
            enhanced_query = f"{query} {' '.join(cached_terms)}"
            return EnhancedQuery(query, cached_terms, enhanced_query, 0.8)
        
        expansion_source = tool_config.get('expansion_source', 'topics')
        max_expansions = tool_config.get('max_expansions', 3)
        
        try:
            # Find semantically similar entities for expansion
            similar_entities = find_similar_entities(
                self.db_path, query, 
                entity_type=expansion_source,
                limit=max_expansions * 2,  # Get more to filter
                similarity_threshold=0.6
            )
            
            # Extract expansion terms
            expansion_terms = []
            for entity in similar_entities[:max_expansions]:
                if entity.get('name') and entity['name'].lower() != query.lower():
                    expansion_terms.append(entity['name'])
            
            # Cache the expansion
            self._expansion_cache[query] = expansion_terms
            
            # Build enhanced query
            enhanced_query = f"{query} {' '.join(expansion_terms)}" if expansion_terms else query
            confidence = np.mean([e.get('similarity', 0) for e in similar_entities]) if similar_entities else 0.0
            
            return EnhancedQuery(query, expansion_terms, enhanced_query, confidence)
            
        except Exception as e:
            logger.warning(f"Query expansion failed for '{query}': {e}")
            return EnhancedQuery(query, [], query, 0.0)
    
    def _get_semantic_results(self, query: str, tool_config: Dict[str, Any], limit: int) -> List[SemanticResult]:
        """Get semantic search results."""
        semantic_results = []
        
        try:
            # Search document chunks semantically
            chunk_results = semantic_search_chunks(
                self.db_path, query, 
                limit=limit,
                similarity_threshold=0.5
            )
            
            for chunk in chunk_results:
                semantic_results.append(SemanticResult(
                    content={
                        'id': chunk.get('chunk_id'),
                        'title': chunk.get('document_title', 'Unknown'),
                        'content': chunk.get('content', '')[:1000],  # Truncate for consistency
                        'date': chunk.get('document_date'),
                        'document_type': chunk.get('document_type'),
                        'document_id': chunk.get('document_id')
                    },
                    similarity=chunk.get('similarity', 0.0),
                    source='semantic',
                    entity_type='document_chunk'
                ))
            
            # Also search entities semantically
            entity_results = find_similar_entities(
                self.db_path, query,
                limit=limit//2,
                similarity_threshold=0.6
            )
            
            for entity in entity_results:
                semantic_results.append(SemanticResult(
                    content=entity,
                    similarity=entity.get('similarity', 0.0),
                    source='semantic',
                    entity_type=entity.get('entity_type')
                ))
                
        except Exception as e:
            logger.warning(f"Semantic search failed: {e}")
        
        return semantic_results
    
    def _merge_results(self, sql_results: List[SemanticResult], semantic_results: List[SemanticResult],
                      sql_weight: float, semantic_weight: float, limit: int) -> List[SemanticResult]:
        """Merge and rank SQL and semantic results."""
        
        # Apply weights to scores
        for result in sql_results:
            result.similarity *= sql_weight
        
        for result in semantic_results:
            result.similarity *= semantic_weight
        
        # Combine and deduplicate
        all_results = sql_results + semantic_results
        
        # Simple deduplication by title/name
        seen_titles = set()
        deduplicated = []
        
        for result in all_results:
            content = result.content
            identifier = content.get('title') or content.get('name') or str(content.get('id', ''))
            
            if identifier and identifier not in seen_titles:
                seen_titles.add(identifier)
                deduplicated.append(result)
        
        # Sort by similarity and limit
        deduplicated.sort(key=lambda x: x.similarity, reverse=True)
        return deduplicated[:limit]
    
    def create_semantic_tools(self) -> Dict[str, Callable]:
        """Create dedicated semantic search tools from configuration."""
        tools = {}
        
        semantic_tools_config = self.config.get('semantic_tools', {})
        
        for tool_name, tool_spec in semantic_tools_config.items():
            if tool_name == 'semantic_search_chunks':
                tools[tool_name] = self._create_semantic_chunks_tool(tool_spec)
            elif tool_name == 'find_similar_entities':
                tools[tool_name] = self._create_similar_entities_tool(tool_spec)
            elif tool_name == 'hybrid_search_documents':
                tools[tool_name] = self._create_hybrid_documents_tool(tool_spec)
            elif tool_name == 'semantic_concept_explorer':
                tools[tool_name] = self._create_concept_explorer_tool(tool_spec)
        
        return tools
    
    def _create_semantic_chunks_tool(self, tool_spec: Dict[str, Any]) -> Callable:
        """Create semantic chunk search tool."""
        
        def semantic_chunks_search(query: str, limit: int = 10, doc_type: Optional[str] = None, 
                                 similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
            """Perform semantic search across document chunks using embeddings."""
            try:
                return semantic_search_chunks(
                    self.db_path, query, limit=limit, 
                    doc_type=doc_type, similarity_threshold=similarity_threshold
                )
            except Exception as e:
                logger.error(f"Semantic chunks search failed: {e}")
                return []
        
        return semantic_chunks_search
    
    def _create_similar_entities_tool(self, tool_spec: Dict[str, Any]) -> Callable:
        """Create similar entities search tool."""
        
        def similar_entities_search(query: str, entity_type: Optional[str] = None, 
                                  limit: int = 15, similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
            """Find entities semantically similar to query using embeddings."""
            try:
                return find_similar_entities(
                    self.db_path, query, entity_type=entity_type,
                    limit=limit, similarity_threshold=similarity_threshold
                )
            except Exception as e:
                logger.error(f"Similar entities search failed: {e}")
                return []
        
        return similar_entities_search
    
    def _create_hybrid_documents_tool(self, tool_spec: Dict[str, Any]) -> Callable:
        """Create hybrid document search tool."""
        
        def hybrid_documents_search(query: str, semantic_weight: float = 0.6, 
                                  limit: int = 10) -> List[Dict[str, Any]]:
            """Search documents using both keyword and semantic matching."""
            
            # This would combine SQL document search with semantic search
            # For now, delegate to semantic search
            try:
                return semantic_search_chunks(
                    self.db_path, query, limit=limit, similarity_threshold=0.4
                )
            except Exception as e:
                logger.error(f"Hybrid documents search failed: {e}")
                return []
        
        return hybrid_documents_search
    
    def _create_concept_explorer_tool(self, tool_spec: Dict[str, Any]) -> Callable:
        """Create concept exploration tool."""
        
        def concept_explorer(concept: str, depth: int = 2, 
                           include_types: Optional[List[str]] = None) -> Dict[str, Any]:
            """Explore concepts using semantic similarity across all entity types."""
            
            results = {
                'concept': concept,
                'related_topics': [],
                'related_documents': [],
                'related_people': [],
                'exploration_depth': depth
            }
            
            try:
                include_types = include_types or ['topic', 'person', 'method']
                
                for entity_type in include_types:
                    similar = find_similar_entities(
                        self.db_path, concept, entity_type=entity_type,
                        limit=5, similarity_threshold=0.6
                    )
                    results[f'related_{entity_type}s'] = similar
                
                # Also find related document chunks
                chunks = semantic_search_chunks(
                    self.db_path, concept, limit=5, similarity_threshold=0.6
                )
                results['related_documents'] = chunks
                
            except Exception as e:
                logger.error(f"Concept exploration failed: {e}")
            
            return results
        
        return concept_explorer
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get statistics about semantic enhancement usage."""
        return {
            'enabled': self.semantic_enabled,
            'embedding_cache_size': len(self._embedding_cache),
            'expansion_cache_size': len(self._expansion_cache),
            'config_tools': len(self.config.get('tool_enhancements', {})),
            'semantic_tools': len(self.config.get('semantic_tools', {}))
        }


def main():
    """Test the semantic enhancement engine."""
    try:
        # Mock semantic config for testing
        semantic_config = {
            'semantic_config': {
                'query_enhancement': {'enabled': True}
            },
            'tool_enhancements': {
                'search_topics': {
                    'semantic_enabled': True,
                    'enhancement_type': 'query_expansion',
                    'expansion_source': 'topics',
                    'max_expansions': 3
                }
            },
            'semantic_tools': {
                'semantic_search_chunks': {},
                'find_similar_entities': {}
            }
        }
        
        engine = SemanticEnhancementEngine("DB/metadata.db", semantic_config)
        
        print("=== Semantic Enhancement Engine Test ===")
        print(f"Status: {engine.get_enhancement_stats()}")
        
        # Test semantic tools creation
        semantic_tools = engine.create_semantic_tools()
        print(f"Created {len(semantic_tools)} semantic tools")
        
        # Test query expansion
        if 'semantic_search_chunks' in semantic_tools:
            results = semantic_tools['semantic_search_chunks']('optimal transport', limit=3)
            print(f"Semantic chunks search: {len(results)} results")
        
        print("✅ Semantic enhancement engine working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()