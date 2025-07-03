#!/usr/bin/env python3
"""
Chronicle metadata extractor that outputs JSON files
Modular approach parallel to academic workflow
"""

import os
import json
import re
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


class ChronicleMetadata(BaseModel):
    """Schema for chronicle note metadata extraction"""
    
    # Core information
    date: str = Field(description="Date/period identifier")
    note_type: str = Field(description="Type: daily, weekly, or monthly")
    title: str = Field(description="Title or summary of the note")
    summary: str = Field(description="Brief summary of work and achievements")
    
    # Entities matching database schema
    topics: List[str] = Field(
        description="Research topics, methods, concepts worked on", default=[]
    )
    
    projects: List[str] = Field(
        description="Projects worked on (project names only)", default=[]
    )
    
    people: List[str] = Field(
        description="People mentioned by full name (no usernames or placeholders)", default=[]
    )
    
    institutions: List[str] = Field(
        description="Organizations, universities, companies mentioned", default=[]
    )
    
    methods: List[str] = Field(
        description="Specific methods, techniques, or approaches used", default=[]
    )
    
    tools: List[str] = Field(
        description="Tools, technologies, frameworks, languages used", default=[]
    )
    
    # Work activities and outcomes
    accomplishments: List[str] = Field(
        description="Key accomplishments and completed work", default=[]
    )
    
    insights: List[str] = Field(
        description="Key insights, breakthroughs, or discoveries", default=[]
    )
    
    learning: List[str] = Field(
        description="What was learned, read, or discovered", default=[]
    )
    
    # Future work and challenges
    challenges: List[str] = Field(
        description="Problems faced and challenges", default=[]
    )
    
    future_work: List[str] = Field(
        description="Tasks or research directions for the future", default=[]
    )
    
    # Metrics and references
    metrics: Dict[str, Any] = Field(
        description="Quantitative results with numbers and context", default={}
    )
    
    papers: List[str] = Field(
        description="Academic papers referenced or worked on", default=[]
    )


class ChronicleMetadataExtractor:
    """Extracts metadata from chronicle notes and saves to JSON"""
    
    def __init__(self, model_name: str = "google/gemini-2.5-flash"):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            model=model_name,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Chronicle Metadata Extractor",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=ChronicleMetadata)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract structured metadata from chronicle notes (daily, weekly, or monthly).

Focus on extracting concrete entities that can be stored in a database:
- Topics: Research concepts, mathematical topics, technical areas
- Projects: Specific project names (e.g., "Interactive CV", "Knowledge Graph")
- People: Full names only (not usernames, handles, or "I/me")
- Institutions: Universities, companies, organizations
- Methods: Specific techniques or approaches used
- Tools: Technologies, frameworks, programming languages

Be specific and extract actual names/terms, not generic descriptions.

{format_instructions}"""),
            ("user", "{content}")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from a chronicle note"""
        content = file_path.read_text()
        
        # Determine note type from path
        note_type = self._determine_note_type(file_path)
        
        # Extract date from filename or content
        date = self._extract_date(file_path, content)
        
        try:
            # Extract metadata using LLM
            result = self.chain.invoke({
                "content": content[:10000],  # Limit content
                "format_instructions": self.parser.get_format_instructions()
            })
            
            metadata = result.model_dump()
            
            # Ensure required fields
            metadata['date'] = date
            metadata['note_type'] = note_type
            
            if not metadata.get('title'):
                metadata['title'] = f"{note_type.capitalize()} Note - {date}"
            
            # Add file metadata
            metadata['file_path'] = str(file_path)
            metadata['extracted_at'] = datetime.now().isoformat()
            
            return metadata
            
        except Exception as e:
            print(f"Extraction error for {file_path}: {e}")
            return {
                'title': f"{note_type.capitalize()} Note - {date}",
                'date': date,
                'note_type': note_type,
                'summary': f"Failed to extract metadata: {str(e)}",
                'file_path': str(file_path),
                'extracted_at': datetime.now().isoformat()
            }
    
    def _determine_note_type(self, file_path: Path) -> str:
        """Determine note type from file path"""
        path_str = str(file_path).lower()
        if 'daily' in path_str:
            return 'daily'
        elif 'weekly' in path_str:
            return 'weekly'
        elif 'monthly' in path_str:
            return 'monthly'
        else:
            # Try to infer from filename pattern
            filename = file_path.stem
            if re.match(r'^\d{4}-\d{2}-\d{2}$', filename):  # YYYY-MM-DD
                return 'daily'
            elif 'w' in filename.lower() and re.search(r'\d{2}', filename):  # Week pattern
                return 'weekly'
            elif re.match(r'^\d{4}-\d{2}$', filename):  # YYYY-MM
                return 'monthly'
            else:
                return 'daily'  # default
    
    def _extract_date(self, file_path: Path, content: str) -> str:
        """Extract date from filename or content"""
        filename = file_path.stem
        
        # Try various date patterns in filename
        # YYYY-MM-DD
        if match := re.match(r'^(\d{4}-\d{2}-\d{2})', filename):
            return match.group(1)
        
        # YYYY-WXX (weekly)
        if match := re.match(r'^(\d{4}-W\d{2})', filename):
            return match.group(1)
        
        # YYYY-MM (monthly)
        if match := re.match(r'^(\d{4}-\d{2})$', filename):
            return match.group(1)
        
        # Try to extract from content frontmatter
        if match := re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', content):
            return match.group(1)
        
        # Default to today
        return datetime.now().date().isoformat()
    
    def save_metadata(self, metadata: Dict[str, Any], output_dir: Path) -> Path:
        """Save metadata to JSON file"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename based on source file
        source_path = Path(metadata['file_path'])
        output_filename = f"{source_path.stem}_metadata.json"
        output_path = output_dir / output_filename
        
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def process_file(self, file_path: Path, output_dir: Path) -> Optional[Path]:
        """Process a single chronicle file"""
        print(f"Processing {file_path.name}...")
        
        metadata = self.extract_metadata(file_path)
        output_path = self.save_metadata(metadata, output_dir)
        
        # Display summary
        print(f"  ✓ Extracted: {len(metadata.get('topics', []))} topics, "
              f"{len(metadata.get('projects', []))} projects, "
              f"{len(metadata.get('people', []))} people, "
              f"{len(metadata.get('institutions', []))} institutions")
        print(f"  ✓ Saved to: {output_path}")
        
        return output_path
    
    def process_directory(self, input_dir: Path, output_dir: Path, 
                         pattern: str = "*.md") -> List[Path]:
        """Process all chronicle files in a directory"""
        processed_files = []
        
        # Find all markdown files recursively
        files = list(input_dir.rglob(pattern))
        print(f"Found {len(files)} files to process")
        
        for file_path in files:
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    output_path = self.process_file(file_path, output_dir)
                    if output_path:
                        processed_files.append(output_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        return processed_files
    
    def display_summary(self, metadata: Dict[str, Any]):
        """Display a summary of extracted metadata"""
        print(f"\n{'='*60}")
        print(f"CHRONICLE: {metadata.get('title', 'Unknown')}")
        print(f"TYPE: {metadata.get('note_type', 'Unknown').upper()}")
        print(f"DATE: {metadata.get('date', 'Unknown')}")
        print(f"{'='*60}")
        
        if metadata.get('summary'):
            print(f"\n📋 SUMMARY: {metadata['summary']}")
        
        # Entity counts
        entity_types = [
            ('topics', '🔬 TOPICS'),
            ('projects', '🚀 PROJECTS'),
            ('people', '👥 PEOPLE'),
            ('institutions', '🏛️ INSTITUTIONS'),
            ('methods', '🔧 METHODS'),
            ('tools', '⚙️ TOOLS'),
            ('accomplishments', '✅ ACCOMPLISHMENTS'),
            ('insights', '💡 INSIGHTS'),
            ('challenges', '⚠️ CHALLENGES'),
            ('future_work', '🔮 FUTURE WORK')
        ]
        
        for key, label in entity_types:
            if metadata.get(key):
                items = metadata[key]
                if isinstance(items, list) and items:
                    print(f"\n{label} ({len(items)}):")
                    for item in items[:5]:  # Show first 5
                        print(f"  • {item}")
                    if len(items) > 5:
                        print(f"  ... and {len(items) - 5} more")
        
        if metadata.get('metrics'):
            print(f"\n📊 METRICS:")
            for metric, value in metadata['metrics'].items():
                print(f"  • {metric}: {value}")


def main():
    """Process chronicle notes and save metadata"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract metadata from chronicle notes')
    parser.add_argument('--input', type=Path, default=Path("raw_data/chronicle"),
                       help='Input directory with chronicle notes')
    parser.add_argument('--output', type=Path, default=Path("raw_data/chronicle/extracted_metadata"),
                       help='Output directory for metadata JSON files')
    parser.add_argument('--pattern', default="*.md", help='File pattern to match')
    parser.add_argument('--show-summary', action='store_true', help='Display detailed summaries')
    
    args = parser.parse_args()
    
    extractor = ChronicleMetadataExtractor()
    
    print(f"Processing chronicle notes from {args.input}")
    print(f"Output directory: {args.output}")
    
    processed = extractor.process_directory(args.input, args.output, args.pattern)
    
    print(f"\n{'='*60}")
    print(f"Processed {len(processed)} files successfully")
    
    # Show sample if requested
    if args.show_summary and processed:
        print("\nSample extraction:")
        with open(processed[0]) as f:
            sample = json.load(f)
        extractor.display_summary(sample)


if __name__ == "__main__":
    main()