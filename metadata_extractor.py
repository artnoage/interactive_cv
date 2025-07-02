#!/usr/bin/env python3
"""
Metadata extractor for chronicle notes
Production-ready extractor with refined prompts
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


class ChronicleMetadata(BaseModel):
    """Schema for chronicle metadata extraction"""
    
    # Core information
    date: str = Field(description="Date in YYYY-MM-DD format")
    mood: Optional[str] = Field(description="Mood or energy level mentioned")
    day_summary: str = Field(description="2-3 sentence executive summary of the day's work and achievements")
    
    # Project progress with context
    project_updates: List[Dict[str, str]] = Field(
        description="Projects worked on with fields: project_name, work_completed, technical_approach, measurable_outcome, next_steps"
    )
    
    # Technical insights with significance
    technical_insights: List[Dict[str, str]] = Field(
        description="Key technical discoveries with: insight, context, why_significant, application"
    )
    
    # Problems solved with learning
    problems_solved: List[Dict[str, str]] = Field(
        description="Challenges overcome with: problem_description, solution_approach, implementation_details, lesson_learned"
    )
    
    # Quantitative achievements
    performance_metrics: Dict[str, str] = Field(
        description="All quantitative results mentioned (percentages, benchmarks, improvements, counts) with context"
    )
    
    # Knowledge and skills
    skills_demonstrated: List[str] = Field(
        description="Technical skills and competencies demonstrated through the work"
    )
    
    concepts_applied: List[str] = Field(
        description="Theoretical concepts or methods applied in practice"
    )
    
    # Tools and stack
    technologies_used: Dict[str, List[str]] = Field(
        description="Tech stack organized by: {languages: [], frameworks: [], libraries: [], tools: [], platforms: []}"
    )
    
    # Collaboration and attribution
    people_mentioned: List[Dict[str, str]] = Field(
        description="People with: name, role, contribution or context"
    )
    
    # Research connections
    research_connections: List[str] = Field(
        description="How the practical work connects to academic research, papers, or theoretical knowledge"
    )
    
    # Future direction
    planned_next_steps: List[Dict[str, str]] = Field(
        description="Future tasks with: task, priority (high/medium/low), purpose, expected_timeline"
    )
    
    # Innovation markers
    innovations: List[str] = Field(
        description="Novel approaches, creative solutions, or new methods developed"
    )


class MetadataExtractor:
    """Chronicle metadata extractor with refined prompts"""
    
    def __init__(self, model_name: str = "google/gemini-2.5-flash"):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model=model_name,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Interactive CV Metadata Extractor",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=ChronicleMetadata)
        
        # Best performing prompt (Research-Focused approach)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are analyzing daily research notes from Vaios, a mathematician transitioning to ML/AI.
Extract structured metadata that captures the essence of his work and progress.
Focus on:
- Technical achievements and why they matter
- Quantitative improvements (always include specific numbers)
- How practical work connects to theoretical knowledge
- Learning journey and insights gained
Be specific and include context for each item."""),
            
            ("human", """Extract comprehensive metadata from this daily research note.

Look for:
1. What projects were worked on and what specific progress was made?
2. What technical insights or breakthroughs occurred and why do they matter?
3. What problems were solved and what was learned from solving them?
4. What quantitative results were achieved (percentages, metrics, improvements)?
5. How does today's work connect to broader research goals?

Content:
{content}

{format_instructions}""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def extract_metadata(self, content: str) -> ChronicleMetadata:
        """Extract metadata from chronicle note content"""
        try:
            result = self.chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"Extraction error: {e}")
            raise
    
    def process_file(self, file_path: Path) -> Dict:
        """Process a single file and return metadata dict"""
        print(f"Processing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self.extract_metadata(content)
        
        result = metadata.dict()
        result['file_path'] = str(file_path)
        result['extracted_at'] = datetime.now().isoformat()
        result['extraction_version'] = "1.0"
        
        return result
    
    def extract_and_display(self, file_path: Path):
        """Extract and display key metadata in readable format"""
        metadata_dict = self.process_file(file_path)
        metadata = ChronicleMetadata(**metadata_dict)
        
        print(f"\n{'='*80}")
        print(f"METADATA EXTRACTION: {metadata.date}")
        print(f"{'='*80}")
        
        print(f"\n📋 SUMMARY:\n{metadata.day_summary}")
        
        if metadata.project_updates:
            print(f"\n🚀 PROJECTS ({len(metadata.project_updates)}):")
            for proj in metadata.project_updates:
                print(f"\n  • {proj['project_name']}:")
                print(f"    - Work: {proj.get('work_completed', 'N/A')}")
                if 'measurable_outcome' in proj:
                    print(f"    - Outcome: {proj['measurable_outcome']}")
        
        if metadata.technical_insights:
            print(f"\n💡 KEY INSIGHTS ({len(metadata.technical_insights)}):")
            for insight in metadata.technical_insights:
                print(f"\n  • {insight['insight']}")
                print(f"    - Why it matters: {insight.get('why_significant', 'N/A')}")
        
        if metadata.performance_metrics:
            print(f"\n📊 METRICS:")
            for metric, value in metadata.performance_metrics.items():
                print(f"  • {metric}: {value}")
        
        if metadata.innovations:
            print(f"\n🔬 INNOVATIONS:")
            for innovation in metadata.innovations:
                print(f"  • {innovation}")
        
        if metadata.research_connections:
            print(f"\n🎓 RESEARCH CONNECTIONS:")
            for connection in metadata.research_connections:
                print(f"  • {connection}")
        
        return metadata_dict


def demo_extraction():
    """Demonstrate extraction on sample notes"""
    extractor = MetadataExtractor()
    
    # Test on available notes
    test_files = [
        Path("chronicle/Daily Notes/2025-06-29.md"),
        Path("chronicle/Daily Notes/2025-06-30.md"),
    ]
    
    all_metadata = []
    
    for file_path in test_files:
        if file_path.exists():
            print(f"\n{'#'*80}")
            print(f"# Extracting from: {file_path.name}")
            print(f"{'#'*80}")
            
            metadata = extractor.extract_and_display(file_path)
            all_metadata.append(metadata)
        else:
            print(f"File not found: {file_path}")
    
    # Save all metadata
    if all_metadata:
        output_file = "extraction_results.json"
        with open(output_file, 'w') as f:
            json.dump(all_metadata, f, indent=2)
        print(f"\n\n✅ All metadata saved to: {output_file}")


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Running metadata extraction...")
    demo_extraction()