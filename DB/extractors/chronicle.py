"""
Chronicle extractor using the normalized database schema.
Processes daily, weekly, and monthly notes.
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, date
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from .base import BaseExtractor

load_dotenv()


class ChronicleMetadata(BaseModel):
    """Schema for chronicle note metadata extraction"""
    
    # Core information
    date: str = Field(description="Date/period identifier")
    note_type: str = Field(description="Type: daily, weekly, or monthly")
    title: str = Field(description="Title or summary of the note")
    summary: str = Field(description="Brief summary of work and achievements")
    
    # Entities
    topics: List[str] = Field(
        description="Research topics, methods, concepts worked on", default=[]
    )
    
    projects: List[str] = Field(
        description="Projects worked on (project names only)", default=[]
    )
    
    tools: List[str] = Field(
        description="Tools and technologies used", default=[]
    )
    
    people: List[str] = Field(
        description="People mentioned by full name (no usernames or placeholders)", default=[]
    )
    
    institutions: List[str] = Field(
        description="Organizations, universities, companies mentioned", default=[]
    )
    
    # Accomplishments and insights
    accomplishments: List[str] = Field(
        description="Key accomplishments and completed work", default=[]
    )
    
    insights: List[str] = Field(
        description="Key insights, breakthroughs, or discoveries", default=[]
    )
    
    learning: List[str] = Field(
        description="What was learned, read, or discovered", default=[]
    )
    
    # Challenges and future work
    challenges: List[str] = Field(
        description="Problems faced and challenges", default=[]
    )
    
    future_work: List[str] = Field(
        description="Tasks or research directions for the future", default=[]
    )
    
    # Metrics
    metrics: Dict[str, str] = Field(
        description="Quantitative results with numbers and context", default={}
    )
    
    # References
    papers: List[str] = Field(
        description="Academic papers referenced or worked on", default=[]
    )
    
    references: List[str] = Field(
        description="Other notes or documents referenced", default=[]
    )


class ChronicleExtractor(BaseExtractor):
    """Chronicle extractor for the v2 database schema"""
    
    def __init__(self, db_path: str = "DB/metadata.db",
                 model_name: str = "google/gemini-2.5-flash"):
        super().__init__(db_path)
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            model=model_name,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Interactive CV Chronicle Extractor V2",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=ChronicleMetadata)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are extracting structured metadata from work notes (daily, weekly, or monthly).

Extract all relevant entities and relationships from the note.

Guidelines:
- Determine note type from content (daily, weekly, or monthly)
- Extract full names for people (no usernames or partial names)
- Identify all projects, tools, and research topics mentioned
- Capture quantitative metrics with context
- Extract insights, learning, and accomplishments
- Note any challenges or future work items
- Identify organizations and institutions mentioned

Be thorough but precise in extraction."""),
            
            ("human", """Extract metadata from this note:

{content}

{format_instructions}""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def get_doc_type(self, file_path: Path) -> str:
        """Chronicle documents are always 'chronicle' type"""
        return 'chronicle'
    
    def extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from chronicle note content"""
        try:
            # Use LLM to extract structured metadata
            result = self.chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            metadata = result.model_dump()
            
            # Try to extract date from path if not in metadata
            if not metadata.get('date'):
                date_str = self._extract_date_from_path(file_path)
                if date_str:
                    metadata['date'] = date_str
            
            # Set title from summary if not provided
            if not metadata.get('title'):
                metadata['title'] = metadata.get('summary', '')[:100]
            
            # Add file path for reference
            metadata['file_path'] = str(file_path)
            metadata['extracted_at'] = datetime.now().isoformat()
            
            return metadata
            
        except Exception as e:
            print(f"Extraction error: {e}")
            # Return minimal metadata on error
            return {
                'date': self._extract_date_from_path(file_path) or datetime.now().date().isoformat(),
                'note_type': self._guess_note_type(file_path),
                'title': file_path.stem,
                'summary': f"Failed to extract metadata: {str(e)}",
                'file_path': str(file_path),
                'extracted_at': datetime.now().isoformat()
            }
    
    def _guess_note_type(self, file_path: Path) -> str:
        """Guess note type from file path"""
        path_str = str(file_path).lower()
        if 'daily' in path_str:
            return 'daily'
        elif 'weekly' in path_str or '-w' in path_str:
            return 'weekly'
        elif 'monthly' in path_str:
            return 'monthly'
        else:
            return 'daily'  # Default
    
    def process_directory(self, directory: Path, pattern: str = "*.md") -> List[int]:
        """Process all matching files in a directory"""
        processed_ids = []
        
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                try:
                    doc_id = self.process_file(file_path)
                    if doc_id:
                        processed_ids.append(doc_id)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        # Update graph tables after batch processing
        if processed_ids:
            self.update_graph_tables()
        
        return processed_ids


def demo_extraction():
    """Demo extraction on sample notes"""
    extractor = ChronicleExtractor()
    
    # Test on available notes
    test_files = [
        Path("chronicle/Daily Notes/2025-06-29.md"),
        Path("chronicle/Daily Notes/2025-06-30.md"),
        Path("chronicle/Weekly Notes/2025-W26.md"),
        Path("chronicle/Monthly Notes/2025-06.md"),
    ]
    
    processed_ids = []
    
    for file_path in test_files:
        if file_path.exists():
            print(f"\n{'='*60}")
            print(f"Processing: {file_path.name}")
            print(f"{'='*60}")
            
            try:
                doc_id = extractor.process_file(file_path)
                if doc_id:
                    processed_ids.append(doc_id)
                    print(f"✓ Successfully processed - Document ID: {doc_id}")
            except Exception as e:
                print(f"✗ Error: {e}")
        else:
            print(f"File not found: {file_path}")
    
    if processed_ids:
        print(f"\n✅ Processed {len(processed_ids)} documents")
        print(f"Document IDs: {processed_ids}")
    
    return processed_ids


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Chronicle Extractor V2 - Using new database schema")
    demo_extraction()