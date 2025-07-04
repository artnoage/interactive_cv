#!/usr/bin/env python3
"""
Document metadata extractor
Generic extractor that works with any document type based on configuration blueprints
"""

import os
import json
import sys
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Add blueprints to path
sys.path.append(str(Path(__file__).parent.parent / "blueprints" / "core"))
from blueprint_loader import get_blueprint_loader, create_extraction_model

load_dotenv()


class DocumentExtractor:
    """Generic metadata extractor driven by blueprint configurations"""
    
    def __init__(self, document_type: str, model_name: str = "google/gemini-2.5-flash"):
        self.document_type = document_type
        self.blueprint_loader = get_blueprint_loader()
        
        # Load blueprint configuration
        self.extraction_schema = self.blueprint_loader.get_extraction_schema(document_type)
        self.database_mapping = self.blueprint_loader.get_database_mapping(document_type)
        self.document_mapping = self.blueprint_loader.get_document_mapping(document_type)
        
        # Create Pydantic model dynamically from blueprint
        self.metadata_model = create_extraction_model(document_type)
        
        # Initialize LLM
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            model=model_name,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": f"Blueprint-Driven {document_type.title()} Extractor",
            }
        )
        
        # Create extraction prompt from blueprint
        self.extraction_prompt = self._build_extraction_prompt()
        self.parser = PydanticOutputParser(pydantic_object=self.metadata_model)
    
    def _build_extraction_prompt(self) -> ChatPromptTemplate:
        """Build extraction prompt dynamically from blueprint schema"""
        
        # Build field descriptions from blueprint
        field_descriptions = []
        
        for section_name, fields in self.extraction_schema.items():
            if not fields:
                continue
                
            section_title = section_name.replace('_', ' ').title()
            field_descriptions.append(f"\n## {section_title}")
            
            for field in fields:
                # Escape curly braces in field description
                description = field.description.replace('{', '{{').replace('}', '}}')
                field_desc = f"- **{field.name}**: {description}"
                
                if field.enum:
                    field_desc += f" (options: {', '.join(field.enum)})"
                
                if field.field_type == 'list_of_objects' and field.schema:
                    # Escape curly braces for prompt template
                    schema_str = str(field.schema).replace('{', '{{').replace('}', '}}')
                    field_desc += f"\n  Structure: {schema_str}"
                
                if field.required:
                    field_desc += " [REQUIRED]"
                
                field_descriptions.append(field_desc)
        
        field_descriptions_text = '\n'.join(field_descriptions)
        
        # Build extraction instructions
        extraction_instructions = []
        
        # Check for special instructions in blueprint
        schema_config = self.blueprint_loader._load_yaml(
            self.blueprint_loader.blueprints_dir / self.document_type / "extraction_schema.yaml"
        )
        
        if 'extraction_instructions' in schema_config:
            instructions = schema_config['extraction_instructions']
            for instruction_type, instruction_config in instructions.items():
                title = instruction_type.replace('_', ' ').title()
                extraction_instructions.append(f"\n### {title}")
                desc = instruction_config.get('description', '')
                # Escape curly braces in description
                desc = desc.replace('{', '{{').replace('}', '}}')
                extraction_instructions.append(desc)
                
                if 'rules' in instruction_config:
                    for rule in instruction_config['rules']:
                        # Escape curly braces in rules
                        rule_escaped = rule.replace('{', '{{').replace('}', '}}')
                        extraction_instructions.append(f"- {rule_escaped}")
        
        instructions_text = '\n'.join(extraction_instructions) if extraction_instructions else ""
        
        # Build the complete prompt
        if self.document_type == 'academic':
            document_description = "academic research paper analysis"
        elif self.document_type == 'personal':
            document_description = "personal work note or journal entry"
        else:
            document_description = f"{self.document_type} document"
        
        prompt_template = f"""You are an expert metadata extractor specializing in {document_description}.

Your task is to analyze the provided document and extract structured metadata according to the schema below.

## Extraction Schema
{field_descriptions_text}

{instructions_text if instructions_text else ""}

## General Guidelines
- Extract information that is explicitly stated or clearly implied in the document
- For list fields, provide comprehensive but focused items
- For object fields, include all available information following the specified structure
- Use proper capitalization and formatting
- Skip fields if information is not available rather than guessing
- Maintain accuracy and relevance in all extracted information

## Document Content
{{content}}

## Format Instructions
{{format_instructions}}

Please analyze the document and provide the extracted metadata in the specified JSON format."""

        return ChatPromptTemplate.from_template(prompt_template)
    
    def extract_metadata(self, content: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Extract metadata from document content using blueprint-driven prompting"""
        
        # Create the extraction chain
        chain = self.extraction_prompt | self.llm | self.parser
        
        # Extract metadata
        try:
            metadata = chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            # Convert Pydantic model to dict
            metadata_dict = metadata.model_dump()
            
            # Add extraction metadata
            metadata_dict.update({
                "file_path": file_path,
                "extraction_date": datetime.now().isoformat(),
                "extractor_version": "blueprint-v1.0",
                "document_type": self.document_type
            })
            
            return metadata_dict
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            raise
    
    def process_file(self, file_path: Path, output_dir: Path) -> Optional[Path]:
        """Process a single file and save extracted metadata"""
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            metadata = self.extract_metadata(content, str(file_path))
            
            # Create output filename
            output_filename = f"{file_path.stem}_metadata.json"
            output_path = output_dir / output_filename
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save metadata
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Extracted metadata: {output_path.name}")
            self.display_summary(metadata)
            
            return output_path
            
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
            return None
    
    def display_summary(self, metadata: Dict[str, Any]):
        """Display a summary of extracted metadata"""
        
        # Get entity counts from database mapping
        entity_counts = {}
        for field_name, mapping in self.database_mapping.items():
            if field_name in metadata and metadata[field_name]:
                field_data = metadata[field_name]
                if isinstance(field_data, list):
                    count = len(field_data)
                    if count > 0:
                        entity_counts[mapping.entity_type] = entity_counts.get(mapping.entity_type, 0) + count
        
        if entity_counts:
            print("  Entities extracted:")
            for entity_type, count in entity_counts.items():
                print(f"    - {entity_type}: {count}")
        
        # Show core information
        core_info = []
        if metadata.get('title'):
            core_info.append(f"Title: {metadata['title'][:60]}...")
        if metadata.get('date'):
            core_info.append(f"Date: {metadata['date']}")
        if metadata.get('domain'):
            core_info.append(f"Domain: {metadata['domain']}")
        
        if core_info:
            print("  " + " | ".join(core_info))
    
    def process_directory(self, input_dir: Path, output_dir: Path, 
                         pattern: str = "*.md") -> List[Path]:
        """Process all files in a directory"""
        
        input_files = list(input_dir.rglob(pattern))
        processed_files = []
        
        print(f"\nProcessing {len(input_files)} {self.document_type} files...")
        
        for i, file_path in enumerate(input_files, 1):
            print(f"\n[{i}/{len(input_files)}] Processing {file_path.name}...")
            
            output_path = self.process_file(file_path, output_dir)
            if output_path:
                processed_files.append(output_path)
        
        return processed_files


def main():
    """Test the blueprint-driven extractor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Blueprint-driven metadata extractor')
    parser.add_argument('document_type', choices=['academic', 'personal'],
                       help='Type of documents to process')
    parser.add_argument('--input', type=Path, required=True,
                       help='Input file or directory')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output directory for metadata JSON files')
    parser.add_argument('--model', default="google/gemini-2.5-flash",
                       help='Model to use for extraction')
    parser.add_argument('--pattern', default="*.md",
                       help='File pattern for directory processing')
    
    args = parser.parse_args()
    
    # Create extractor
    extractor = DocumentExtractor(args.document_type, args.model)
    
    print(f"Blueprint-Driven {args.document_type.title()} Metadata Extractor")
    print("=" * 60)
    print(f"Document type: {args.document_type}")
    print(f"Model: {args.model}")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    
    # Process input
    if args.input.is_file():
        # Single file
        result = extractor.process_file(args.input, args.output)
        if result:
            print(f"\n✓ Metadata saved to: {result}")
        else:
            print("\n✗ Failed to process file")
    else:
        # Directory
        results = extractor.process_directory(args.input, args.output, args.pattern)
        print(f"\n✓ Processed {len(results)} files")
        print(f"✓ Metadata saved to: {args.output}")


if __name__ == "__main__":
    main()