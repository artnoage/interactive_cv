"""
Chronicle metadata extractor.
Integrates with the existing LLM-based metadata extraction.
"""

import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from .base import BaseExtractor

# Import the existing metadata extractor
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from metadata_extractor import MetadataExtractor, ChronicleMetadata


class ChronicleExtractor(BaseExtractor):
    """Extract metadata from chronicle notes."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db"):
        super().__init__(db_path)
        self.metadata_extractor = MetadataExtractor()
    
    def get_doc_type(self, file_path: Path) -> str:
        """Chronicle files are always 'chronicle' type."""
        return "chronicle"
    
    def extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from chronicle content using hybrid approach."""
        metadata = {}
        
        # 1. Extract frontmatter if present
        frontmatter = self._extract_frontmatter(content)
        if frontmatter:
            metadata.update(frontmatter)
        
        # 2. Use LLM for deep content extraction
        llm_metadata = self._extract_with_llm(file_path, content)
        
        # 3. Merge metadata (LLM takes precedence for richer data)
        for key, value in llm_metadata.items():
            if key in metadata and isinstance(metadata[key], list) and isinstance(value, list):
                # Merge lists and remove duplicates
                metadata[key] = list(set(metadata[key] + value))
            else:
                metadata[key] = value
        
        # 4. Extract additional patterns from content
        pattern_metadata = self._extract_patterns(content)
        
        # Merge pattern metadata
        for key, value in pattern_metadata.items():
            if key in metadata and isinstance(metadata[key], list):
                metadata[key] = list(set(metadata[key] + value))
            elif key not in metadata:
                metadata[key] = value
        
        # 5. Ensure date is set
        if 'date' not in metadata:
            metadata['date'] = self._extract_date_from_path(file_path)
        
        return metadata
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from content."""
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                return {}
        return {}
    
    def _extract_with_llm(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Use LLM to extract rich metadata."""
        try:
            # Extract metadata using the MetadataExtractor
            result = self.metadata_extractor.extract_metadata(content)
            
            if result:
                # Convert ChronicleMetadata object to dict
                result_dict = result.dict()
                
                # Extract the fields we need for the database
                metadata = {
                    'topics': result_dict.get('keywords', []),  # Use keywords as topics
                    'people': result_dict.get('people_involved', []),
                    'projects': [p['project_name'] for p in result_dict.get('project_updates', [])],
                    'tools': result_dict.get('technologies_used', []),
                    'papers': result_dict.get('papers_referenced', []),
                    'insights': [i['insight'] for i in result_dict.get('technical_insights', [])],
                    'project_progress': result_dict.get('project_updates', []),
                    'technical_achievements': result_dict.get('achievements', []),
                    'learning_notes': result_dict.get('research_connections', []),
                    'problems_solved': result_dict.get('problems_addressed', []),
                }
                
                # Add summary fields
                if result_dict.get('work_focus'):
                    metadata['work_focus'] = result_dict['work_focus']
                if result_dict.get('day_summary'):
                    metadata['daily_summary'] = result_dict['day_summary']
                
                # Add innovations and metrics
                if result_dict.get('innovations'):
                    metadata['innovations'] = result_dict['innovations']
                if result_dict.get('performance_metrics'):
                    metadata['performance_metrics'] = result_dict['performance_metrics']
                
                return metadata
            
        except Exception as e:
            print(f"LLM extraction failed for {file_path}: {e}")
        
        return {}
    
    def _extract_patterns(self, content: str) -> Dict[str, List[str]]:
        """Extract additional patterns from content."""
        metadata = {
            'topics': [],
            'people': [],
            'references': []
        }
        
        # Extract hashtags as topics
        hashtags = re.findall(r'#(\w+)', content)
        metadata['topics'].extend(hashtags)
        
        # Extract @mentions as people
        mentions = re.findall(r'@(\w+)', content)
        metadata['people'].extend(mentions)
        
        # Extract wiki-style links
        wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)
        metadata['references'].extend(wiki_links)
        
        # Remove duplicates
        for key in metadata:
            metadata[key] = list(set(metadata[key]))
        
        return metadata
    
    def _extract_date_from_path(self, file_path: Path) -> str:
        """Extract date from file path or name."""
        # Try to extract date from filename (e.g., 2024-01-15.md)
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.name)
        if date_match:
            return date_match.group(1)
        
        # Fall back to file modification time
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.strftime('%Y-%m-%d')
    
    def process_chronicle_folder(self, chronicle_path: str) -> List[int]:
        """Process all markdown files in chronicle folder."""
        chronicle_dir = Path(chronicle_path)
        processed_ids = []
        
        # Find all markdown files
        md_files = list(chronicle_dir.rglob("*.md"))
        print(f"Found {len(md_files)} markdown files in {chronicle_path}")
        
        for md_file in md_files:
            doc_id = self.process_file(md_file)
            if doc_id:
                processed_ids.append(doc_id)
        
        print(f"Processed {len(processed_ids)} files successfully")
        return processed_ids