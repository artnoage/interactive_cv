#!/usr/bin/env python3
"""
Blueprint loader system for reading and parsing YAML configuration files
Provides a unified interface for accessing all blueprint configurations
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ExtractionField:
    """Represents a field definition from extraction schema"""
    name: str
    field_type: str
    description: str
    required: bool = False
    default: Any = None
    enum: Optional[List[str]] = None
    schema: Optional[Dict[str, Any]] = None


@dataclass
class EntityMapping:
    """Represents how a metadata field maps to database entities"""
    metadata_field: str
    target_table: str
    entity_type: str
    relationship_type: str
    category_handling: Optional[str] = None
    category_override: Optional[str] = None
    category_field: Optional[str] = None
    description_field: Optional[str] = None
    domain_field: Optional[str] = None
    role_override: Optional[str] = None
    confidence: float = 1.0


@dataclass
class VisualizationConfig:
    """Represents visualization configuration for knowledge graph"""
    node_type_mappings: Dict[str, Dict[str, str]]
    colors: Dict[str, str]
    sizes: Dict[str, int]
    edge_styles: Dict[str, Dict[str, Any]]
    node_groups: Dict[str, Dict[str, Any]]
    legend: Dict[str, Any]


class BlueprintLoader:
    """Loads and parses blueprint configurations from YAML files"""
    
    def __init__(self, blueprints_dir: Union[str, Path] = "blueprints"):
        # Resolve blueprints_dir relative to the project root
        if isinstance(blueprints_dir, str) and blueprints_dir == "blueprints":
            # Find project root by looking for blueprint directory
            current = Path(__file__).parent
            while current != current.parent:
                if (current / "blueprints").exists():
                    self.blueprints_dir = current / "blueprints"
                    break
                current = current.parent
            else:
                # Fallback: assume we're in blueprints/core/
                self.blueprints_dir = Path(__file__).parent.parent
        else:
            self.blueprints_dir = Path(blueprints_dir)
        self._cache = {}
        
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML file with caching"""
        cache_key = str(file_path)
        
        if cache_key not in self._cache:
            try:
                with open(file_path, 'r') as f:
                    self._cache[cache_key] = yaml.safe_load(f)
                logger.debug(f"Loaded blueprint: {file_path}")
            except FileNotFoundError:
                logger.error(f"Blueprint file not found: {file_path}")
                raise
            except yaml.YAMLError as e:
                logger.error(f"Error parsing YAML file {file_path}: {e}")
                raise
                
        return self._cache[cache_key]
    
    def get_extraction_schema(self, document_type: str) -> Dict[str, List[ExtractionField]]:
        """Get extraction schema for a document type (academic, personal)"""
        schema_path = self.blueprints_dir / document_type / "extraction_schema.yaml"
        config = self._load_yaml(schema_path)
        
        schema = {}
        
        # Process all field sections
        field_sections = [
            'core_fields', 'reconnaissance_fields', 'technical_fields',
            'analysis_fields', 'evaluation_fields', 'synthesis_fields',
            'context_fields', 'entity_fields', 'activity_fields',
            'challenge_fields', 'metrics_fields', 'additional_fields',
            'extraction_metadata'
        ]
        
        for section in field_sections:
            if section in config:
                schema[section] = []
                for field_name, field_config in config[section].items():
                    field = ExtractionField(
                        name=field_name,
                        field_type=field_config.get('type', 'string'),
                        description=field_config.get('description', ''),
                        required=field_config.get('required', False),
                        default=field_config.get('default'),
                        enum=field_config.get('enum'),
                        schema=field_config.get('schema')
                    )
                    schema[section].append(field)
        
        return schema
    
    def get_database_mapping(self, document_type: str) -> Dict[str, EntityMapping]:
        """Get database mapping configuration for a document type"""
        mapping_path = self.blueprints_dir / document_type / "database_mapping.yaml"
        config = self._load_yaml(mapping_path)
        
        mappings = {}
        entity_mappings = config.get('entity_mappings', {})
        
        for field_name, mapping_config in entity_mappings.items():
            mapping = EntityMapping(
                metadata_field=field_name,
                target_table=mapping_config.get('target_table'),
                entity_type=mapping_config.get('entity_type'),
                relationship_type=mapping_config.get('relationship_type'),
                category_handling=mapping_config.get('category_handling'),
                category_override=mapping_config.get('category_override'),
                category_field=mapping_config.get('category_field'),
                description_field=mapping_config.get('description_field'),
                domain_field=mapping_config.get('domain_field'),
                role_override=mapping_config.get('role_override'),
                confidence=mapping_config.get('confidence', 1.0)
            )
            mappings[field_name] = mapping
            
        return mappings
    
    def get_document_mapping(self, document_type: str) -> Dict[str, Any]:
        """Get document table mapping for a document type"""
        mapping_path = self.blueprints_dir / document_type / "database_mapping.yaml"
        config = self._load_yaml(mapping_path)
        return config.get('document_mapping', {})
    
    def get_visualization_config(self) -> VisualizationConfig:
        """Get visualization configuration"""
        viz_path = self.blueprints_dir / "core" / "visualization.yaml"
        config = self._load_yaml(viz_path)
        
        return VisualizationConfig(
            node_type_mappings=config.get('node_type_mappings', {}),
            colors=config.get('colors', {}),
            sizes=config.get('sizes', {}),
            edge_styles=config.get('edge_styles', {}),
            node_groups=config.get('node_groups', {}),
            legend=config.get('legend', {})
        )
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Get core database schema configuration"""
        schema_path = self.blueprints_dir / "core" / "database_schema.yaml"
        return self._load_yaml(schema_path)
    
    def get_special_handling(self, document_type: str) -> Dict[str, Any]:
        """Get special handling rules for a document type"""
        mapping_path = self.blueprints_dir / document_type / "database_mapping.yaml"
        config = self._load_yaml(mapping_path)
        return config.get('special_handling', {})
    
    def get_relationship_confidence(self, document_type: str) -> Dict[str, float]:
        """Get relationship confidence scores for a document type"""
        mapping_path = self.blueprints_dir / document_type / "database_mapping.yaml"
        config = self._load_yaml(mapping_path)
        return config.get('relationship_confidence', {})
    
    def list_document_types(self) -> List[str]:
        """List available document types based on blueprint directories"""
        document_types = []
        for item in self.blueprints_dir.iterdir():
            if item.is_dir() and item.name != 'core':
                # Check if it has required blueprint files
                extraction_schema = item / "extraction_schema.yaml"
                database_mapping = item / "database_mapping.yaml"
                if extraction_schema.exists() and database_mapping.exists():
                    document_types.append(item.name)
        return document_types
    
    def validate_blueprints(self) -> Dict[str, List[str]]:
        """Validate all blueprint configurations and return any errors"""
        errors = {}
        
        # Check core blueprints
        core_dir = self.blueprints_dir / "core"
        if not core_dir.exists():
            errors['core'] = ["Core blueprints directory missing"]
        else:
            required_core = ["database_schema.yaml", "visualization.yaml"]
            for required_file in required_core:
                if not (core_dir / required_file).exists():
                    if 'core' not in errors:
                        errors['core'] = []
                    errors['core'].append(f"Missing {required_file}")
        
        # Check document type blueprints
        for doc_type in self.list_document_types():
            doc_errors = []
            
            try:
                # Try to load extraction schema
                self.get_extraction_schema(doc_type)
            except Exception as e:
                doc_errors.append(f"Invalid extraction_schema.yaml: {e}")
            
            try:
                # Try to load database mapping
                self.get_database_mapping(doc_type)
            except Exception as e:
                doc_errors.append(f"Invalid database_mapping.yaml: {e}")
            
            if doc_errors:
                errors[doc_type] = doc_errors
        
        return errors
    
    def create_pydantic_model(self, document_type: str, model_name: str = None) -> type:
        """Dynamically create a Pydantic model from extraction schema"""
        from pydantic import BaseModel, Field, create_model
        
        schema = self.get_extraction_schema(document_type)
        model_fields = {}
        
        # Flatten all field sections into a single model
        for section_name, fields in schema.items():
            for field in fields:
                field_args = {
                    'description': field.description
                }
                
                if field.default is not None:
                    field_args['default'] = field.default
                elif not field.required:
                    field_args['default'] = None
                
                # Map blueprint types to Python types
                if field.field_type == 'string':
                    field_type = str
                elif field.field_type == 'list_of_strings':
                    field_type = List[str]
                    if field.default is None:
                        field_args['default'] = []
                elif field.field_type == 'list_of_objects':
                    field_type = List[Dict[str, Any]]
                    if field.default is None:
                        field_args['default'] = []
                elif field.field_type == 'object':
                    field_type = Optional[Dict[str, Any]]
                else:
                    field_type = Any
                
                # Handle optional fields
                if not field.required:
                    field_type = Optional[field_type]
                
                model_fields[field.name] = (field_type, Field(**field_args))
        
        # Create the model
        if model_name is None:
            model_name = f"{document_type.title()}Metadata"
            
        return create_model(model_name, **model_fields, __base__=BaseModel)


# Global blueprint loader instance
_blueprint_loader = None

def get_blueprint_loader(blueprints_dir: Union[str, Path] = "blueprints") -> BlueprintLoader:
    """Get the global blueprint loader instance"""
    global _blueprint_loader
    if _blueprint_loader is None:
        _blueprint_loader = BlueprintLoader(blueprints_dir)
    return _blueprint_loader


# Convenience functions
def load_extraction_schema(document_type: str) -> Dict[str, List[ExtractionField]]:
    """Load extraction schema for a document type"""
    return get_blueprint_loader().get_extraction_schema(document_type)

def load_database_mapping(document_type: str) -> Dict[str, EntityMapping]:
    """Load database mapping for a document type"""
    return get_blueprint_loader().get_database_mapping(document_type)

def load_visualization_config() -> VisualizationConfig:
    """Load visualization configuration"""
    return get_blueprint_loader().get_visualization_config()

def create_extraction_model(document_type: str) -> type:
    """Create a Pydantic model for extraction"""
    return get_blueprint_loader().create_pydantic_model(document_type)


if __name__ == "__main__":
    # Test the blueprint loader
    loader = BlueprintLoader()
    
    print("Available document types:", loader.list_document_types())
    
    # Validate blueprints
    errors = loader.validate_blueprints()
    if errors:
        print("Blueprint validation errors:")
        for blueprint, error_list in errors.items():
            print(f"  {blueprint}: {error_list}")
    else:
        print("All blueprints are valid!")
    
    # Test loading schemas
    for doc_type in loader.list_document_types():
        try:
            schema = loader.get_extraction_schema(doc_type)
            mapping = loader.get_database_mapping(doc_type)
            print(f"\n{doc_type} blueprint loaded successfully:")
            print(f"  Extraction fields: {sum(len(fields) for fields in schema.values())}")
            print(f"  Entity mappings: {len(mapping)}")
        except Exception as e:
            print(f"Error loading {doc_type}: {e}")
    
    # Test visualization config
    try:
        viz_config = loader.get_visualization_config()
        print(f"\nVisualization config loaded:")
        print(f"  Node types: {len(viz_config.colors)}")
        print(f"  Edge styles: {len(viz_config.edge_styles)}")
    except Exception as e:
        print(f"Error loading visualization config: {e}")