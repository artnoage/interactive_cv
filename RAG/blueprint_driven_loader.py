#!/usr/bin/env python3
"""
Blueprint-Driven Tool Loader
Parses YAML blueprints and provides unified API for tool generation.

This module implements the vision of configuration-driven tool generation,
where sophisticated domain-aware tools are automatically created from 
declarative YAML specifications rather than manual coding.
"""

import yaml
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DatabaseColumn:
    """Represents a database column with its properties."""
    name: str
    type: str
    primary_key: bool = False
    auto_increment: bool = False
    unique: bool = False
    not_null: bool = False
    default: Optional[str] = None
    description: Optional[str] = None


@dataclass
class DatabaseTable:
    """Represents a database table with its columns and constraints."""
    name: str
    description: str
    columns: Dict[str, DatabaseColumn]
    constraints: Dict[str, Any]
    indexes: List[str]


@dataclass
class EntityMapping:
    """Represents how extracted metadata maps to database entities."""
    target_table: str
    entity_type: str
    relationship_type: str
    category_field: Optional[str] = None
    category_override: Optional[str] = None
    category_handling: Optional[str] = None
    description_field: Optional[str] = None
    role_override: Optional[str] = None
    domain_field: Optional[str] = None


@dataclass
class VisualizationConfig:
    """Represents visualization configuration for node types."""
    colors: Dict[str, str]
    sizes: Dict[str, int]
    node_groups: Dict[str, Dict[str, Any]]
    edge_styles: Dict[str, Dict[str, Any]]
    node_type_mappings: Dict[str, Dict[str, str]]


class BlueprintLoader:
    """
    Loads and parses all YAML blueprints to provide unified API for tool generation.
    
    This class implements the core vision: read declarative specifications and
    provide programmatic access to database schema, entity mappings, and
    visualization configurations.
    """
    
    def __init__(self, blueprints_dir: str = "blueprints"):
        """Initialize loader with blueprints directory."""
        self.blueprints_dir = Path(blueprints_dir)
        self.database_schema: Dict[str, DatabaseTable] = {}
        self.entity_mappings: Dict[str, Dict[str, EntityMapping]] = {}
        self.visualization_config: Optional[VisualizationConfig] = None
        self.extraction_schemas: Dict[str, Dict[str, Any]] = {}
        self.tool_guidance: Optional[Dict[str, Any]] = None
        
        self._load_all_blueprints()
    
    def _load_all_blueprints(self):
        """Load all blueprint files and parse them."""
        logger.info(f"Loading blueprints from {self.blueprints_dir}")
        
        # Load core database schema
        self._load_database_schema()
        
        # Load visualization config
        self._load_visualization_config()
        
        # Load tool guidance config
        self._load_tool_guidance()
        
        # Load domain-specific mappings
        self._load_domain_mappings()
        
        logger.info(f"Loaded {len(self.database_schema)} tables, "
                   f"{sum(len(m) for m in self.entity_mappings.values())} entity mappings")
    
    def _load_database_schema(self):
        """Load database schema from core/database_schema.yaml."""
        schema_file = self.blueprints_dir / "core" / "database_schema.yaml"
        
        if not schema_file.exists():
            raise FileNotFoundError(f"Database schema not found: {schema_file}")
        
        with open(schema_file, 'r') as f:
            schema_data = yaml.safe_load(f)
        
        # Parse all table categories
        all_tables = {}
        for category in ['document_tables', 'entity_tables', 'processing_tables', 
                        'vector_tables', 'metadata_tables']:
            if category in schema_data:
                all_tables.update(schema_data[category])
        
        # Add relationship table
        if 'relationship_table' in schema_data:
            all_tables.update(schema_data['relationship_table'])
        
        # Parse tables
        for table_name, table_spec in all_tables.items():
            columns = {}
            constraints = {}
            
            # Parse columns
            for col_name, col_spec in table_spec.get('columns', {}).items():
                columns[col_name] = DatabaseColumn(
                    name=col_name,
                    type=col_spec.get('type', 'TEXT'),
                    primary_key=col_spec.get('primary_key', False),
                    auto_increment=col_spec.get('auto_increment', False),
                    unique=col_spec.get('unique', False),
                    not_null=col_spec.get('not_null', False),
                    default=col_spec.get('default'),
                    description=col_spec.get('description')
                )
            
            # Parse constraints
            constraints = table_spec.get('constraints', {})
            
            self.database_schema[table_name] = DatabaseTable(
                name=table_name,
                description=table_spec.get('description', ''),
                columns=columns,
                constraints=constraints,
                indexes=[]  # TODO: Parse indexes from schema
            )
    
    def _load_visualization_config(self):
        """Load visualization configuration from core/visualization.yaml."""
        viz_file = self.blueprints_dir / "core" / "visualization.yaml"
        
        if not viz_file.exists():
            logger.warning(f"Visualization config not found: {viz_file}")
            return
        
        with open(viz_file, 'r') as f:
            viz_data = yaml.safe_load(f)
        
        self.visualization_config = VisualizationConfig(
            colors=viz_data.get('colors', {}),
            sizes=viz_data.get('sizes', {}),
            node_groups=viz_data.get('node_groups', {}),
            edge_styles=viz_data.get('edge_styles', {}),
            node_type_mappings=viz_data.get('node_type_mappings', {})
        )
    
    def _load_tool_guidance(self):
        """Load tool guidance configuration from core/tool_guidance.yaml."""
        guidance_file = self.blueprints_dir / "core" / "tool_guidance.yaml"
        
        if not guidance_file.exists():
            logger.warning(f"Tool guidance config not found: {guidance_file}")
            self.tool_guidance = {}
            return
        
        with open(guidance_file, 'r') as f:
            self.tool_guidance = yaml.safe_load(f)
        
        logger.info("Loaded tool guidance configuration")
    
    def _load_domain_mappings(self):
        """Load domain-specific entity mappings."""
        for domain_dir in self.blueprints_dir.iterdir():
            if domain_dir.is_dir() and domain_dir.name != 'core':
                domain_name = domain_dir.name
                self.entity_mappings[domain_name] = {}
                
                # Load database mapping
                mapping_file = domain_dir / "database_mapping.yaml"
                if mapping_file.exists():
                    self._load_domain_mapping(domain_name, mapping_file)
                
                # Load extraction schema
                extraction_file = domain_dir / "extraction_schema.yaml"
                if extraction_file.exists():
                    self._load_extraction_schema(domain_name, extraction_file)
    
    def _load_domain_mapping(self, domain: str, mapping_file: Path):
        """Load entity mappings for a specific domain."""
        with open(mapping_file, 'r') as f:
            mapping_data = yaml.safe_load(f)
        
        entity_mappings = mapping_data.get('entity_mappings', {})
        
        for entity_name, entity_spec in entity_mappings.items():
            self.entity_mappings[domain][entity_name] = EntityMapping(
                target_table=entity_spec.get('target_table'),
                entity_type=entity_spec.get('entity_type'),
                relationship_type=entity_spec.get('relationship_type'),
                category_field=entity_spec.get('category_field'),
                category_override=entity_spec.get('category_override'),
                category_handling=entity_spec.get('category_handling'),
                description_field=entity_spec.get('description_field'),
                role_override=entity_spec.get('role_override'),
                domain_field=entity_spec.get('domain_field')
            )
    
    def _load_extraction_schema(self, domain: str, extraction_file: Path):
        """Load extraction schema for a specific domain."""
        with open(extraction_file, 'r') as f:
            extraction_data = yaml.safe_load(f)
        
        self.extraction_schemas[domain] = extraction_data
    
    # ========== Public API Methods ==========
    
    def get_table_schema(self, table_name: str) -> Optional[DatabaseTable]:
        """Get schema for a specific table."""
        return self.database_schema.get(table_name)
    
    def get_all_tables(self) -> Dict[str, DatabaseTable]:
        """Get all table schemas."""
        return self.database_schema.copy()
    
    def get_entity_mappings(self, domain: str) -> Dict[str, EntityMapping]:
        """Get entity mappings for a domain."""
        return self.entity_mappings.get(domain, {})
    
    def get_all_entity_mappings(self) -> Dict[str, Dict[str, EntityMapping]]:
        """Get all entity mappings for all domains."""
        return self.entity_mappings.copy()
    
    def get_visualization_config(self) -> Optional[VisualizationConfig]:
        """Get visualization configuration."""
        return self.visualization_config
    
    def get_extraction_schema(self, domain: str) -> Dict[str, Any]:
        """Get extraction schema for a domain."""
        return self.extraction_schemas.get(domain, {})
    
    def get_tool_guidance(self) -> Dict[str, Any]:
        """Get tool guidance configuration."""
        return self.tool_guidance or {}
    
    def get_entity_tables(self) -> List[str]:
        """Get list of all entity table names."""
        entity_tables = []
        for table_name, table in self.database_schema.items():
            # Entity tables are those that store extractable entities
            if table_name in ['topics', 'people', 'methods', 'institutions', 
                             'applications', 'projects']:
                entity_tables.append(table_name)
        return entity_tables
    
    def get_document_tables(self) -> List[str]:
        """Get list of document table names."""
        return [name for name in self.database_schema.keys() 
                if 'document' in name and name != 'document_chunks']
    
    def get_relationship_types(self, domain: str = None) -> List[str]:
        """Get all relationship types, optionally filtered by domain."""
        rel_types = set()
        
        if domain:
            mappings = self.entity_mappings.get(domain, {})
            for mapping in mappings.values():
                rel_types.add(mapping.relationship_type)
        else:
            for domain_mappings in self.entity_mappings.values():
                for mapping in domain_mappings.values():
                    rel_types.add(mapping.relationship_type)
        
        return sorted(list(rel_types))
    
    def get_entity_categories(self, entity_type: str) -> List[str]:
        """Get all possible categories for an entity type."""
        categories = set()
        
        # From visualization mappings
        if self.visualization_config:
            type_mappings = self.visualization_config.node_type_mappings.get(entity_type, {})
            categories.update(type_mappings.keys())
        
        # From entity mappings
        for domain_mappings in self.entity_mappings.values():
            for mapping in domain_mappings.values():
                if mapping.entity_type == entity_type:
                    if mapping.category_override:
                        categories.add(mapping.category_override)
        
        return sorted(list(categories))
    
    def generate_sql_schema(self) -> str:
        """Generate SQL CREATE statements from blueprint schema."""
        sql_statements = []
        
        for table_name, table in self.database_schema.items():
            # CREATE TABLE statement
            columns = []
            constraints = []
            
            for col_name, col in table.columns.items():
                col_def = f"{col_name} {col.type}"
                
                if col.primary_key:
                    col_def += " PRIMARY KEY"
                if col.auto_increment:
                    col_def += " AUTOINCREMENT"
                if col.unique:
                    col_def += " UNIQUE"
                if col.not_null:
                    col_def += " NOT NULL"
                if col.default:
                    col_def += f" DEFAULT {col.default}"
                
                columns.append(col_def)
            
            # Add table constraints
            for constraint in table.constraints.values():
                if constraint.get('type') == 'UNIQUE':
                    cols = ', '.join(constraint.get('columns', []))
                    constraints.append(f"UNIQUE({cols})")
            
            all_definitions = columns + constraints
            create_stmt = f"CREATE TABLE {table_name} (\n    " + ",\n    ".join(all_definitions) + "\n);"
            sql_statements.append(create_stmt)
        
        return "\n\n".join(sql_statements)
    
    def validate_database_schema(self, db_path: str) -> Dict[str, Any]:
        """Validate actual database against blueprint schema."""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        validation_results = {
            'missing_tables': [],
            'extra_tables': [],
            'schema_mismatches': [],
            'valid': True
        }
        
        # Get actual tables
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        actual_tables = {row[0] for row in cursor}
        
        # Get expected tables
        expected_tables = set(self.database_schema.keys())
        
        # Find missing and extra tables
        validation_results['missing_tables'] = list(expected_tables - actual_tables)
        validation_results['extra_tables'] = list(actual_tables - expected_tables)
        
        # Check schema for existing tables
        for table_name in expected_tables & actual_tables:
            expected_table = self.database_schema[table_name]
            
            # Get actual columns
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            actual_columns = {row[1]: row[2] for row in cursor}  # name: type
            
            if expected_table and expected_table.columns:
                expected_columns = {col.name: col.type for col in expected_table.columns.values()}
            else:
                expected_columns = {}
            
            if actual_columns != expected_columns:
                validation_results['schema_mismatches'].append({
                    'table': table_name,
                    'expected': expected_columns,
                    'actual': actual_columns
                })
        
        validation_results['valid'] = (
            not validation_results['missing_tables'] and
            not validation_results['schema_mismatches']
        )
        
        conn.close()
        return validation_results


def main():
    """Test the blueprint loader."""
    try:
        loader = BlueprintLoader()
        
        print("=== Blueprint Loader Test ===")
        print(f"Loaded {len(loader.get_all_tables())} tables")
        print(f"Loaded {len(loader.get_all_entity_mappings())} domain mappings")
        
        # Test table access
        print("\n=== Document Tables ===")
        for table_name in loader.get_document_tables():
            table = loader.get_table_schema(table_name)
            print(f"- {table_name}: {len(table.columns)} columns")
        
        # Test entity mappings
        print("\n=== Entity Mappings ===")
        for domain, mappings in loader.get_all_entity_mappings().items():
            print(f"- {domain}: {len(mappings)} mappings")
            for entity_name, mapping in list(mappings.items())[:3]:
                print(f"  - {entity_name} → {mapping.target_table} ({mapping.relationship_type})")
        
        # Test relationship types
        print("\n=== Relationship Types ===")
        rel_types = loader.get_relationship_types()
        print(f"Found {len(rel_types)} relationship types: {', '.join(rel_types[:5])}...")
        
        # Test categories
        print("\n=== Entity Categories ===")
        topic_categories = loader.get_entity_categories('topic')
        print(f"Topic categories: {', '.join(topic_categories[:5])}...")
        
        print("\n✅ Blueprint loader working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()