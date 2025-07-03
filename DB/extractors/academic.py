"""
Academic extractor using the normalized database schema.
Processes academic paper analyses following the three-phase structure.
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from .base import BaseExtractor

load_dotenv()


class AcademicMetadata(BaseModel):
    """Schema for academic paper metadata extraction aligned with normalized database"""
    
    # Core paper information
    title: str = Field(description="Paper title")
    authors: List[str] = Field(description="Paper authors", default=[])
    year: Optional[str] = Field(description="Publication year")
    venue: Optional[str] = Field(description="Journal/conference venue")
    domain: Optional[str] = Field(
        description="Primary domain: mathematics, computer_science, or physics"
    )
    document_type: str = Field(
        description="Type: paper or analysis", default="analysis"
    )
    
    # Core contribution
    core_contribution: str = Field(description="Main contribution of the paper")
    problem_addressed: Optional[str] = Field(
        description="The core problem being solved"
    )
    
    # Entities for database storage
    topics: List[str] = Field(
        description="Research topics and mathematical concepts", default=[]
    )
    
    mathematical_concepts: List[Dict[str, str]] = Field(
        description="Mathematical concepts with: name, category (theory/space/metric/operator/functional/equation/principle), description", default=[]
    )
    
    methods: List[Dict[str, str]] = Field(
        description="Methods with: name, type (analytical/computational/algorithmic/theoretical/experimental), description", default=[]
    )
    
    algorithms: List[Dict[str, str]] = Field(
        description="Algorithms with: name, purpose, key_idea, complexity", default=[]
    )
    
    people: List[str] = Field(
        description="People mentioned (full names only)", default=[]
    )
    
    institutions: List[str] = Field(
        description="Institutions and organizations mentioned", default=[]
    )
    
    applications: List[Dict[str, str]] = Field(
        description="Applications with: domain, use_case, impact", default=[]
    )
    
    research_areas: List[str] = Field(
        description="High-level research areas and fields", default=[]
    )
    
    # Critical analysis elements
    assumptions: List[str] = Field(
        description="Key assumptions and approximations made", default=[]
    )
    
    limitations: List[str] = Field(
        description="Limitations and boundaries of applicability", default=[]
    )
    
    future_work: List[str] = Field(
        description="Open questions and future research directions", default=[]
    )
    
    # Key insights and innovations
    key_insights: List[str] = Field(
        description="Core insights distilled from the paper", default=[]
    )
    
    innovations: List[str] = Field(
        description="Novel approaches and key innovations", default=[]
    )
    
    # Related concepts for graph building
    builds_on: List[str] = Field(
        description="Concepts, theories, or methods this work builds upon", default=[]
    )
    
    enables: List[str] = Field(
        description="Future work or applications this enables", default=[]
    )
    
    theoretical_results: List[str] = Field(
        description="Key theoretical results or theorems proven", default=[]
    )
    
    related_concepts: List[str] = Field(
        description="Concepts closely related but not part of core contribution", default=[]
    )
    
    # Evaluation details (stored as JSON in relationships)
    evaluation_summary: Optional[str] = Field(
        description="Summary of evaluation approach and results"
    )
    
    # Mathematical details (for math papers)
    proof_strategy: Optional[str] = Field(
        description="Main proof strategy for mathematical papers"
    )


class AcademicExtractor(BaseExtractor):
    """Academic extractor for the normalized database schema"""
    
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
                "X-Title": "Academic Paper Extractor V2",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=AcademicMetadata)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are extracting structured metadata from academic paper analyses that follow a three-phase structure.

The analyses follow this structure:
- Phase 1: Rapid Reconnaissance (Executive Summary, Problem, Initial Assessment)
- Phase 2: Deep Dive (Domain-specific technical analysis)
- Phase 3: Synthesis & Future Work (Key insights, Open questions)

Extract entities for the database schema:
1. Topics: General research topics and areas
2. Mathematical Concepts: Specific mathematical objects with categories (theory/space/metric/operator/functional/equation/principle)
3. Methods: Techniques with types (analytical/computational/algorithmic/theoretical/experimental)
4. Algorithms: Named algorithms with purpose and complexity
5. Research Areas: High-level fields (mathematics, computer_science, physics, etc.)
6. People: Full names only (no usernames)
7. Institutions: Universities, research centers, companies
8. Applications: Concrete applications with domain, use_case, and impact
9. Assumptions: Key assumptions made
10. Limitations: Boundaries and limitations
11. Future Work: Open questions and research directions
12. Innovations: Novel contributions
13. Builds On: Prior work this builds upon
14. Enables: What this work enables
15. Theoretical Results: Key theorems or results proven
16. Related Concepts: Concepts related but not core

Domain detection:
- mathematics: proofs, theorems, mathematical structures
- computer_science: algorithms, systems, experiments
- physics: physical models, experiments

Be thorough but concise. Extract entity names, not full descriptions."""),
            
            ("human", """Extract metadata from this academic paper analysis:

{content}

{format_instructions}""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def get_doc_type(self, file_path: Path) -> str:
        """Academic documents are always 'academic' type"""
        return 'academic'
    
    def extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from academic paper analysis"""
        try:
            # Use LLM to extract structured metadata
            result = self.chain.invoke({
                "content": content[:15000],  # Limit content length
                "format_instructions": self.parser.get_format_instructions()
            })
            
            metadata = result.model_dump()
            
            # Extract date from content or use current date
            if not metadata.get('date'):
                # Try to extract year from the content
                import re
                year_match = re.search(r'20\d{2}', content)
                if year_match:
                    metadata['date'] = f"{year_match.group()}-01-01"
                else:
                    metadata['date'] = datetime.now().date().isoformat()
            
            # Ensure we have a title
            if not metadata.get('title'):
                # Try to extract from file name
                metadata['title'] = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            # Add file metadata
            metadata['file_path'] = str(file_path)
            metadata['extracted_at'] = datetime.now().isoformat()
            
            return metadata
            
        except Exception as e:
            print(f"Extraction error: {e}")
            # Return minimal metadata on error
            return {
                'title': file_path.stem.replace('_', ' ').title(),
                'date': datetime.now().date().isoformat(),
                'document_type': 'analysis',
                'core_contribution': f"Failed to extract metadata: {str(e)}",
                'file_path': str(file_path),
                'extracted_at': datetime.now().isoformat()
            }
    
    def process_directory(self, directory: Path, pattern: str = "*_analysis.md") -> List[int]:
        """Process all matching analysis files in a directory"""
        processed_ids = []
        
        for file_path in directory.glob(pattern):
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
    
    def display_summary(self, metadata: Dict[str, Any]):
        """Display a summary of extracted metadata"""
        print(f"\n{'='*80}")
        print(f"ACADEMIC PAPER: {metadata.get('title', 'Unknown')}")
        if metadata.get('domain'):
            print(f"DOMAIN: {metadata['domain'].upper()}")
        print(f"{'='*80}")
        
        # Core info
        if metadata.get('authors'):
            print(f"\n👥 AUTHORS: {', '.join(metadata['authors'])}")
        
        if metadata.get('core_contribution'):
            print(f"\n🚀 CONTRIBUTION: {metadata['core_contribution']}")
        
        # Entity counts
        entity_types = [
            ('topics', '🔬 TOPICS'),
            ('mathematical_concepts', '📐 MATHEMATICAL CONCEPTS'),
            ('methods', '🔧 METHODS'),
            ('algorithms', '⚙️ ALGORITHMS'),
            ('research_areas', '🎯 RESEARCH AREAS'),
            ('applications', '🌍 APPLICATIONS'),
            ('assumptions', '⚠️ ASSUMPTIONS'),
            ('limitations', '🚧 LIMITATIONS'),
            ('future_work', '🔮 FUTURE WORK'),
            ('innovations', '✨ INNOVATIONS'),
            ('theoretical_results', '📊 THEORETICAL RESULTS')
        ]
        
        for key, label in entity_types:
            if metadata.get(key):
                items = metadata[key]
                if isinstance(items, list) and len(items) > 0:
                    print(f"\n{label} ({len(items)}):")
                    for i, item in enumerate(items[:5]):  # Show first 5
                        if isinstance(item, dict):
                            # For structured items (concepts, methods, algorithms, applications)
                            if 'name' in item:
                                extra_info = []
                                if 'category' in item:
                                    extra_info.append(f"category: {item['category']}")
                                if 'type' in item:
                                    extra_info.append(f"type: {item['type']}")
                                if 'domain' in item:
                                    extra_info.append(f"domain: {item['domain']}")
                                if 'complexity' in item:
                                    extra_info.append(f"complexity: {item['complexity']}")
                                info_str = f" ({', '.join(extra_info)})" if extra_info else ""
                                print(f"  • {item['name']}{info_str}")
                            else:
                                # For applications or other dict structures
                                print(f"  • {item}")
                        else:
                            # For simple string items
                            print(f"  • {item}")
                    if len(items) > 5:
                        print(f"  ... and {len(items) - 5} more")


def demo_extraction():
    """Demo extraction on academic papers"""
    extractor = AcademicExtractor()
    
    # Test on available analyses
    test_dir = Path("../raw_data/academic/Transcript_Analysis")
    
    if test_dir.exists():
        print(f"Processing analyses in: {test_dir}")
        processed_ids = extractor.process_directory(test_dir)
        
        if processed_ids:
            print(f"\n✅ Processed {len(processed_ids)} academic analyses")
            print(f"Document IDs: {processed_ids}")
    else:
        print(f"Directory not found: {test_dir}")
        
        # Try single file
        test_file = Path("../raw_data/academic/Transcript_Analysis/Universal_Neural_Optimal_Transport_analysis.md")
        if test_file.exists():
            print(f"\nProcessing single file: {test_file.name}")
            doc_id = extractor.process_file(test_file)
            if doc_id:
                print(f"✓ Successfully processed - Document ID: {doc_id}")


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Academic Extractor V2 - Using new database schema")
    demo_extraction()