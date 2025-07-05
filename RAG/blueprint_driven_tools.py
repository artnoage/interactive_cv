#!/usr/bin/env python3
"""
Blueprint-Driven Tool Generator
Automatically generates sophisticated, domain-aware tools from YAML blueprints.

This module implements the vision of AI-driven tool generation, where complex
database queries, entity searches, and relationship traversals are automatically
created from declarative specifications rather than manual coding.
"""

import sqlite3
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass
import logging

from RAG.blueprint_driven_loader import BlueprintLoader, EntityMapping, DatabaseTable

logger = logging.getLogger(__name__)


@dataclass
class GeneratedTool:
    """Represents a generated tool with its metadata."""
    name: str
    description: str
    function: Callable
    category: str
    parameters: Dict[str, Any]
    generated_from: str  # Which blueprint/specification generated this


class BlueprintDrivenToolGenerator:
    """
    Generates sophisticated tools automatically from blueprint specifications.
    
    This class embodies the vision of configuration-driven development:
    sophisticated domain-aware tools are generated automatically from
    declarative YAML specifications, eliminating manual coding and ensuring
    consistency with the data model.
    """
    
    def __init__(self, db_path: str = "DB/metadata.db", blueprints_dir: str = "blueprints"):
        """Initialize tool generator with database and blueprints."""
        self.db_path = db_path
        self.loader = BlueprintLoader(blueprints_dir)
        self.generated_tools: Dict[str, GeneratedTool] = {}
        
        # Generate all tools from blueprints
        self._generate_all_tools()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _generate_all_tools(self):
        """Generate all tools from blueprint specifications."""
        logger.info("Generating tools from blueprints...")
        
        # Generate schema-driven query tools
        self._generate_schema_driven_tools()
        
        # Generate entity-aware search tools
        self._generate_entity_search_tools()
        
        # Generate relationship traversal tools
        self._generate_relationship_tools()
        
        # Generate category-aware tools
        self._generate_category_tools()
        
        # Generate visualization-ready tools
        self._generate_visualization_tools()
        
        logger.info(f"Generated {len(self.generated_tools)} tools from blueprints")
    
    def _generate_schema_driven_tools(self):
        """Generate basic CRUD tools for each table from schema."""
        for table_name, table_schema in self.loader.get_all_tables().items():
            # Skip processing tables
            if table_name in ['document_chunks', 'chunk_entities', 'embeddings', 
                             'graph_nodes', 'graph_edges', 'extraction_log']:
                continue
            
            # Generate search tool for this table
            search_tool = self._create_table_search_tool(table_name, table_schema)
            self.generated_tools[f"search_{table_name}"] = search_tool
            
            # Generate get-by-id tool for this table  
            get_tool = self._create_table_get_tool(table_name, table_schema)
            self.generated_tools[f"get_{table_name}_by_id"] = get_tool
            
            # Generate list tool for this table
            list_tool = self._create_table_list_tool(table_name, table_schema)
            self.generated_tools[f"list_{table_name}"] = list_tool
    
    def _create_table_search_tool(self, table_name: str, table_schema: DatabaseTable) -> GeneratedTool:
        """Create a search tool for a specific table."""
        
        def search_function(query: str, limit: int = 10, **filters) -> List[Dict[str, Any]]:
            """Search function generated from table schema."""
            conn = self._get_connection()
            results = []
            
            try:
                # Build dynamic search query based on table columns
                searchable_columns = []
                for col_name, col in table_schema.columns.items():
                    if col.type == 'TEXT' and col_name not in ['id', 'created_at', 'modified_at']:
                        searchable_columns.append(col_name)
                
                if not searchable_columns:
                    return []
                
                # Build WHERE clause for text search
                search_conditions = []
                params = []
                
                for col in searchable_columns:
                    search_conditions.append(f"{col} LIKE ?")
                    params.append(f"%{query}%")
                
                # Add filter conditions
                filter_conditions = []
                for filter_name, filter_value in filters.items():
                    if filter_name in table_schema.columns:
                        filter_conditions.append(f"{filter_name} = ?")
                        params.append(filter_value)
                
                # Combine conditions
                where_clause = " OR ".join(search_conditions)
                if filter_conditions:
                    where_clause = f"({where_clause}) AND {' AND '.join(filter_conditions)}"
                
                sql_query = f"""
                    SELECT * FROM {table_name}
                    WHERE {where_clause}
                    ORDER BY 
                        CASE WHEN name LIKE ? THEN 0 ELSE 1 END,
                        id
                    LIMIT ?
                """
                
                # Add name priority parameter if name column exists
                if 'name' in table_schema.columns:
                    params.append(f"%{query}%")
                else:
                    # Remove the ORDER BY name clause
                    sql_query = f"""
                        SELECT * FROM {table_name}
                        WHERE {where_clause}
                        ORDER BY id
                        LIMIT ?
                    """
                
                params.append(limit)
                
                cursor = conn.execute(sql_query, params)
                for row in cursor:
                    results.append(dict(row))
                
            finally:
                conn.close()
            
            return results
        
        return GeneratedTool(
            name=f"search_{table_name}",
            description=f"Search {table_schema.description or table_name} by text query with optional filters",
            function=search_function,
            category="schema_driven_search",
            parameters={
                "query": {"type": "str", "description": "Search query"},
                "limit": {"type": "int", "default": 10, "description": "Maximum results"},
                "filters": {"type": "dict", "description": "Column filters"}
            },
            generated_from=f"database_schema.yaml:{table_name}"
        )
    
    def _create_table_get_tool(self, table_name: str, table_schema: DatabaseTable) -> GeneratedTool:
        """Create a get-by-id tool for a specific table."""
        
        def get_function(entity_id: int) -> Optional[Dict[str, Any]]:
            """Get entity by ID function generated from table schema."""
            conn = self._get_connection()
            
            try:
                cursor = conn.execute(f"SELECT * FROM {table_name} WHERE id = ?", (entity_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
            finally:
                conn.close()
        
        return GeneratedTool(
            name=f"get_{table_name}_by_id",
            description=f"Get {table_schema.description or table_name} by ID",
            function=get_function,
            category="schema_driven_get",
            parameters={
                "entity_id": {"type": "int", "description": "Entity ID"}
            },
            generated_from=f"database_schema.yaml:{table_name}"
        )
    
    def _create_table_list_tool(self, table_name: str, table_schema: DatabaseTable) -> GeneratedTool:
        """Create a list tool for a specific table."""
        
        def list_function(limit: int = 50, offset: int = 0, **filters) -> List[Dict[str, Any]]:
            """List entities function generated from table schema."""
            conn = self._get_connection()
            results = []
            
            try:
                # Build filter conditions
                filter_conditions = []
                params = []
                
                for filter_name, filter_value in filters.items():
                    if filter_name in table_schema.columns:
                        filter_conditions.append(f"{filter_name} = ?")
                        params.append(filter_value)
                
                where_clause = ""
                if filter_conditions:
                    where_clause = f"WHERE {' AND '.join(filter_conditions)}"
                
                sql_query = f"""
                    SELECT * FROM {table_name}
                    {where_clause}
                    ORDER BY id
                    LIMIT ? OFFSET ?
                """
                
                params.extend([limit, offset])
                
                cursor = conn.execute(sql_query, params)
                for row in cursor:
                    results.append(dict(row))
                
            finally:
                conn.close()
            
            return results
        
        return GeneratedTool(
            name=f"list_{table_name}",
            description=f"List {table_schema.description or table_name} with pagination and filters",
            function=list_function,
            category="schema_driven_list",
            parameters={
                "limit": {"type": "int", "default": 50, "description": "Maximum results"},
                "offset": {"type": "int", "default": 0, "description": "Offset for pagination"},
                "filters": {"type": "dict", "description": "Column filters"}
            },
            generated_from=f"database_schema.yaml:{table_name}"
        )
    
    def _generate_entity_search_tools(self):
        """Generate entity-aware search tools based on entity mappings."""
        for domain, mappings in self.loader.get_all_entity_mappings().items():
            # Group mappings by target table
            table_mappings = {}
            for entity_name, mapping in mappings.items():
                if mapping.target_table not in table_mappings:
                    table_mappings[mapping.target_table] = []
                table_mappings[mapping.target_table].append((entity_name, mapping))
            
            # Generate search tools for each table in this domain
            for table_name, entity_mappings in table_mappings.items():
                search_tool = self._create_entity_aware_search_tool(domain, table_name, entity_mappings)
                self.generated_tools[f"search_{domain}_{table_name}"] = search_tool
    
    def _create_entity_aware_search_tool(self, domain: str, table_name: str, 
                                        entity_mappings: List[Tuple[str, EntityMapping]]) -> GeneratedTool:
        """Create entity-aware search tool."""
        
        def search_function(query: str, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
            """Entity-aware search with category filtering."""
            conn = self._get_connection()
            results = []
            
            try:
                # Build category-aware query
                base_query = f"SELECT * FROM {table_name}"
                conditions = []
                params = []
                
                # Text search conditions
                text_columns = ['name', 'description', 'title']
                text_conditions = []
                for col in text_columns:
                    # Check if column exists in table
                    table_schema = self.loader.get_table_schema(table_name)
                    if table_schema and col in table_schema.columns:
                        text_conditions.append(f"{col} LIKE ?")
                        params.append(f"%{query}%")
                
                if text_conditions:
                    conditions.append(f"({' OR '.join(text_conditions)})")
                
                # Category filtering
                if category:
                    conditions.append("category = ?")
                    params.append(category)
                
                if conditions:
                    base_query += f" WHERE {' AND '.join(conditions)}"
                
                base_query += " ORDER BY id LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(base_query, params)
                for row in cursor:
                    result = dict(row)
                    # Add domain context
                    result['domain'] = domain
                    result['entity_mappings'] = [em[0] for em in entity_mappings]
                    results.append(result)
                
            finally:
                conn.close()
            
            return results
        
        mapping_names = [em[0] for em in entity_mappings]
        
        return GeneratedTool(
            name=f"search_{domain}_{table_name}",
            description=f"Search {table_name} entities from {domain} domain with category awareness",
            function=search_function,
            category="entity_aware_search",
            parameters={
                "query": {"type": "str", "description": "Search query"},
                "category": {"type": "str", "optional": True, "description": "Entity category filter"},
                "limit": {"type": "int", "default": 10, "description": "Maximum results"}
            },
            generated_from=f"{domain}/database_mapping.yaml:{','.join(mapping_names)}"
        )
    
    def _generate_relationship_tools(self):
        """Generate relationship traversal tools."""
        # Get all relationship types from mappings
        relationship_types = set()
        for domain, mappings in self.loader.get_all_entity_mappings().items():
            for mapping in mappings.values():
                relationship_types.add(mapping.relationship_type)
        
        # Generate traversal tools for each relationship type
        for rel_type in relationship_types:
            traversal_tool = self._create_relationship_traversal_tool(rel_type)
            self.generated_tools[f"traverse_{rel_type}"] = traversal_tool
            
            reverse_tool = self._create_reverse_relationship_tool(rel_type)
            self.generated_tools[f"reverse_{rel_type}"] = reverse_tool
    
    def _create_relationship_traversal_tool(self, relationship_type: str) -> GeneratedTool:
        """Create relationship traversal tool."""
        
        def traverse_function(source_type: str, source_id: str, limit: int = 20) -> List[Dict[str, Any]]:
            """Traverse relationships from source entity."""
            conn = self._get_connection()
            results = []
            
            try:
                # Find all targets connected by this relationship type
                query = """
                    SELECT r.target_type, r.target_id, r.confidence, r.metadata
                    FROM relationships r
                    WHERE r.source_type = ? AND r.source_id = ? 
                    AND r.relationship_type = ?
                    ORDER BY r.confidence DESC
                    LIMIT ?
                """
                
                cursor = conn.execute(query, (source_type, source_id, relationship_type, limit))
                
                for row in cursor:
                    target_type = row['target_type']
                    target_id = row['target_id']
                    
                    # Get target entity details
                    target_details = self._get_entity_details(conn, target_type, target_id)
                    
                    if target_details:
                        result = {
                            'relationship_type': relationship_type,
                            'target_type': target_type,
                            'target_id': target_id,
                            'confidence': row['confidence'],
                            'metadata': row['metadata'],
                            'target_details': target_details
                        }
                        results.append(result)
                
            finally:
                conn.close()
            
            return results
        
        return GeneratedTool(
            name=f"traverse_{relationship_type}",
            description=f"Traverse {relationship_type} relationships from source entities",
            function=traverse_function,
            category="relationship_traversal",
            parameters={
                "source_type": {"type": "str", "description": "Source entity type"},
                "source_id": {"type": "str", "description": "Source entity ID"},
                "limit": {"type": "int", "default": 20, "description": "Maximum results"}
            },
            generated_from=f"entity_mappings:relationship_type={relationship_type}"
        )
    
    def _create_reverse_relationship_tool(self, relationship_type: str) -> GeneratedTool:
        """Create reverse relationship traversal tool."""
        
        def reverse_traverse_function(target_type: str, target_id: str, limit: int = 20) -> List[Dict[str, Any]]:
            """Traverse relationships to target entity (reverse direction)."""
            conn = self._get_connection()
            results = []
            
            try:
                query = """
                    SELECT r.source_type, r.source_id, r.confidence, r.metadata
                    FROM relationships r
                    WHERE r.target_type = ? AND r.target_id = ? 
                    AND r.relationship_type = ?
                    ORDER BY r.confidence DESC
                    LIMIT ?
                """
                
                cursor = conn.execute(query, (target_type, target_id, relationship_type, limit))
                
                for row in cursor:
                    source_type = row['source_type']
                    source_id = row['source_id']
                    
                    # Get source entity details
                    source_details = self._get_entity_details(conn, source_type, source_id)
                    
                    if source_details:
                        result = {
                            'relationship_type': relationship_type,
                            'source_type': source_type,
                            'source_id': source_id,
                            'confidence': row['confidence'],
                            'metadata': row['metadata'],
                            'source_details': source_details
                        }
                        results.append(result)
                
            finally:
                conn.close()
            
            return results
        
        return GeneratedTool(
            name=f"reverse_{relationship_type}",
            description=f"Find entities that have {relationship_type} relationship with target",
            function=reverse_traverse_function,
            category="reverse_relationship_traversal",
            parameters={
                "target_type": {"type": "str", "description": "Target entity type"},
                "target_id": {"type": "str", "description": "Target entity ID"},
                "limit": {"type": "int", "default": 20, "description": "Maximum results"}
            },
            generated_from=f"entity_mappings:relationship_type={relationship_type}"
        )
    
    def _generate_category_tools(self):
        """Generate category-aware tools from visualization config."""
        if not self.loader.visualization_config:
            return
        
        # Generate tools for each entity type that has categories
        for entity_type, type_mappings in self.loader.visualization_config.node_type_mappings.items():
            if entity_type == 'topic':  # Topics have the most categories
                category_tool = self._create_category_exploration_tool(entity_type, type_mappings)
                self.generated_tools[f"explore_{entity_type}_categories"] = category_tool
    
    def _create_category_exploration_tool(self, entity_type: str, type_mappings: Dict[str, str]) -> GeneratedTool:
        """Create category exploration tool."""
        
        def explore_function(category: str = None, limit: int = 20) -> Dict[str, Any]:
            """Explore entities by category with visualization data."""
            conn = self._get_connection()
            
            try:
                if category:
                    # Get entities of specific category
                    query = """
                        SELECT * FROM topics 
                        WHERE category = ?
                        ORDER BY id
                        LIMIT ?
                    """
                    cursor = conn.execute(query, (category, limit))
                    entities = [dict(row) for row in cursor]
                    
                    # Add visualization data
                    viz_config = self.loader.visualization_config
                    viz_type = type_mappings.get(category, 'general_topic')
                    
                    for entity in entities:
                        entity['visualization'] = {
                            'type': viz_type,
                            'color': viz_config.colors.get(viz_type, '#888888'),
                            'size': viz_config.sizes.get(viz_type, 10)
                        }
                    
                    return {
                        'category': category,
                        'visualization_type': viz_type,
                        'entities': entities,
                        'count': len(entities)
                    }
                else:
                    # Get category distribution
                    query = """
                        SELECT category, COUNT(*) as count
                        FROM topics
                        GROUP BY category
                        ORDER BY count DESC
                    """
                    cursor = conn.execute(query)
                    
                    categories = []
                    for row in cursor:
                        cat = row['category']
                        viz_type = type_mappings.get(cat, 'general_topic')
                        categories.append({
                            'category': cat,
                            'count': row['count'],
                            'visualization_type': viz_type,
                            'color': self.loader.visualization_config.colors.get(viz_type, '#888888')
                        })
                    
                    return {
                        'categories': categories,
                        'total_categories': len(categories)
                    }
                
            finally:
                conn.close()
        
        return GeneratedTool(
            name=f"explore_{entity_type}_categories",
            description=f"Explore {entity_type} entities by category with visualization data",
            function=explore_function,
            category="category_exploration",
            parameters={
                "category": {"type": "str", "optional": True, "description": "Specific category to explore"},
                "limit": {"type": "int", "default": 20, "description": "Maximum results per category"}
            },
            generated_from="core/visualization.yaml:node_type_mappings"
        )
    
    def _generate_visualization_tools(self):
        """Generate visualization-ready tools."""
        if not self.loader.visualization_config:
            return
        
        # Generate tool for getting visualization-ready data
        viz_tool = self._create_visualization_data_tool()
        self.generated_tools["get_visualization_data"] = viz_tool
    
    def _create_visualization_data_tool(self) -> GeneratedTool:
        """Create tool for getting visualization-ready entity data."""
        
        def get_viz_data_function(entity_type: str, entity_id: str) -> Dict[str, Any]:
            """Get entity with complete visualization configuration."""
            conn = self._get_connection()
            
            try:
                # Get entity details
                entity_details = self._get_entity_details(conn, entity_type, entity_id)
                if not entity_details:
                    return None
                
                # Get visualization configuration
                viz_config = self.loader.visualization_config
                
                # Determine visualization type
                if entity_type == 'topic':
                    category = entity_details.get('category', 'default')
                    viz_type = viz_config.node_type_mappings.get('topic', {}).get(category, 'general_topic')
                else:
                    viz_type = viz_config.node_type_mappings.get(entity_type, entity_type)
                
                return {
                    'entity': entity_details,
                    'visualization': {
                        'type': viz_type,
                        'color': viz_config.colors.get(viz_type, '#888888'),
                        'size': viz_config.sizes.get(viz_type, 10),
                        'group': self._get_node_group(viz_type)
                    }
                }
                
            finally:
                conn.close()
        
        return GeneratedTool(
            name="get_visualization_data",
            description="Get entity with complete visualization configuration",
            function=get_viz_data_function,
            category="visualization",
            parameters={
                "entity_type": {"type": "str", "description": "Entity type"},
                "entity_id": {"type": "str", "description": "Entity ID"}
            },
            generated_from="core/visualization.yaml:complete_config"
        )
    
    def _get_entity_details(self, conn: sqlite3.Connection, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity details based on type (helper method)."""
        # Handle entity_id format
        if '_' in entity_id:
            numeric_id = entity_id.split('_')[-1]
        else:
            numeric_id = entity_id
        
        # Map entity types to tables
        type_to_table = {
            'topic': 'topics',
            'person': 'people',
            'method': 'methods',
            'institution': 'institutions',
            'application': 'applications',
            'project': 'projects',
            'document': 'academic_documents'  # Default to academic
        }
        
        table_name = type_to_table.get(entity_type)
        if not table_name:
            return None
        
        try:
            cursor = conn.execute(f"SELECT * FROM {table_name} WHERE id = ?", (numeric_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except:
            return None
    
    def _get_node_group(self, viz_type: str) -> str:
        """Get node group for visualization layout."""
        if not self.loader.visualization_config:
            return "default"
        
        for group_name, group_config in self.loader.visualization_config.node_groups.items():
            if viz_type in group_config.get('types', []):
                return group_name
        
        return "default"
    
    # ========== Public API Methods ==========
    
    def get_tool(self, tool_name: str) -> Optional[GeneratedTool]:
        """Get a generated tool by name."""
        return self.generated_tools.get(tool_name)
    
    def get_tools_by_category(self, category: str) -> List[GeneratedTool]:
        """Get all tools in a specific category."""
        return [tool for tool in self.generated_tools.values() if tool.category == category]
    
    def list_all_tools(self) -> Dict[str, GeneratedTool]:
        """Get all generated tools."""
        return self.generated_tools.copy()
    
    def get_tool_function(self, tool_name: str) -> Optional[Callable]:
        """Get the function for a specific tool."""
        tool = self.get_tool(tool_name)
        return tool.function if tool else None
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool with given parameters."""
        tool_func = self.get_tool_function(tool_name)
        if not tool_func:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        return tool_func(**kwargs)


def main():
    """Test the blueprint-driven tool generator."""
    try:
        generator = BlueprintDrivenToolGenerator()
        
        print("=== Blueprint-Driven Tool Generator Test ===")
        print(f"Generated {len(generator.list_all_tools())} tools")
        
        # Test by category
        categories = {}
        for tool in generator.list_all_tools().values():
            if tool.category not in categories:
                categories[tool.category] = []
            categories[tool.category].append(tool.name)
        
        print(f"\n=== Tools by Category ===")
        for category, tool_names in categories.items():
            print(f"- {category}: {len(tool_names)} tools")
            for tool_name in tool_names[:3]:  # Show first 3
                print(f"  - {tool_name}")
        
        # Test executing a generated tool
        print(f"\n=== Testing Generated Tools ===")
        
        # Test search tool
        search_results = generator.execute_tool("search_topics", query="neural", limit=3)
        print(f"Search topics for 'neural': {len(search_results)} results")
        for result in search_results[:2]:
            print(f"  - {result.get('name', 'N/A')}")
        
        # Test relationship traversal
        try:
            rel_results = generator.execute_tool("traverse_discusses", 
                                               source_type="document", 
                                               source_id="academic_1", 
                                               limit=3)
            print(f"Traverse 'discusses' relationships: {len(rel_results)} results")
        except Exception as e:
            print(f"Relationship traversal test: {e}")
        
        # Test category exploration
        try:
            cat_results = generator.execute_tool("explore_topic_categories", limit=5)
            print(f"Topic categories: {cat_results.get('total_categories', 0)} categories")
        except Exception as e:
            print(f"Category exploration test: {e}")
        
        print("\n✅ Blueprint-driven tool generator working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()