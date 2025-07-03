#!/usr/bin/env python3
"""
Simplified metadata extractor for chronicle notes
Focuses on core entities for interactive CV
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


class SimpleChronicleMetadata(BaseModel):
    """Simplified schema supporting daily, weekly, and monthly notes"""
    
    # Core information
    date: str = Field(description="Date/period identifier")
    note_type: str = Field(description="Type: daily, weekly, or monthly")
    summary: str = Field(description="Brief summary of work and achievements")
    
    # Common template fields
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
    
    accomplishments: List[str] = Field(
        description="Key accomplishments and completed work", default=[]
    )
    
    # Daily-specific fields
    insights: List[str] = Field(
        description="Key insights, breakthroughs, or discoveries", default=[]
    )
    
    learning: List[str] = Field(
        description="What was learned, read, or discovered", default=[]
    )
    
    mood: Optional[str] = Field(description="Mood/energy level if mentioned")
    
    # Weekly-specific fields
    achievements: List[str] = Field(
        description="Notable weekly achievements", default=[]
    )
    
    challenges: List[str] = Field(
        description="Problems faced and challenges", default=[]
    )
    
    # Monthly-specific fields
    skills_developed: List[str] = Field(
        description="New skills/techniques learned", default=[]
    )
    
    strategic_insights: List[str] = Field(
        description="High-level strategic realizations", default=[]
    )
    
    # Performance metrics
    metrics: Dict[str, str] = Field(
        description="Quantitative results with numbers and context", default={}
    )


class SimpleMetadataExtractor:
    """Simplified chronicle metadata extractor"""
    
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
                "X-Title": "Interactive CV Metadata Extractor",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=SimpleChronicleMetadata)
        
        # Flexible prompt for daily, weekly, and monthly notes
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are extracting structured metadata from work notes (daily, weekly, or monthly).

First, determine the note type:
- Daily: Daily Note, dated YYYY-MM-DD
- Weekly: Weekly Note, mentions "Week X" or weekly periods
- Monthly: Monthly Note, mentions month/quarter

Extract appropriate fields based on note type:

COMMON FIELDS (all note types):
- Topics: Research areas, methods, concepts
- Projects: Specific project names mentioned
- Tools: Technologies, languages, frameworks used
- People: Full names only (no usernames, placeholders, or partial names)
- Accomplishments: What was completed or achieved
- Metrics: Any quantitative results with numbers

DAILY-SPECIFIC:
- Insights: Key discoveries, breakthroughs, or realizations
- Learning: What was read, studied, or discovered
- Mood: Energy level/mood if mentioned

WEEKLY-SPECIFIC:
- Achievements: Notable weekly achievements from frontmatter
- Challenges: Problems faced from frontmatter

MONTHLY-SPECIFIC:
- Skills developed: New skills/techniques learned
- Strategic insights: High-level realizations

Be concise and specific."""),
            
            ("human", """Extract metadata from this note:

{content}

{format_instructions}""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def extract_metadata(self, content: str) -> SimpleChronicleMetadata:
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
        
        result = metadata.model_dump()
        result['file_path'] = str(file_path)
        result['extracted_at'] = datetime.now().isoformat()
        
        return result
    
    def extract_and_display(self, file_path: Path):
        """Extract and display key metadata"""
        metadata_dict = self.process_file(file_path)
        metadata = SimpleChronicleMetadata(**metadata_dict)
        
        print(f"\n{'='*60}")
        print(f"METADATA: {metadata.date} ({metadata.note_type.upper()})")
        print(f"{'='*60}")
        
        print(f"\n📋 {metadata.summary}")
        
        if metadata.topics:
            print(f"\n🎯 TOPICS: {', '.join(metadata.topics)}")
        
        if metadata.projects:
            print(f"\n🚀 PROJECTS: {', '.join(metadata.projects)}")
        
        if metadata.accomplishments:
            print(f"\n✅ ACCOMPLISHMENTS:")
            for acc in metadata.accomplishments:
                print(f"  • {acc}")
        
        # Daily-specific fields
        if metadata.note_type == "daily":
            if metadata.insights:
                print(f"\n💡 INSIGHTS:")
                for insight in metadata.insights:
                    print(f"  • {insight}")
            
            if metadata.learning:
                print(f"\n📚 LEARNING:")
                for learn in metadata.learning:
                    print(f"  • {learn}")
            
            if metadata.mood:
                print(f"\n😊 MOOD: {metadata.mood}")
        
        # Weekly-specific fields
        if metadata.note_type == "weekly":
            if metadata.achievements:
                print(f"\n🏆 ACHIEVEMENTS:")
                for achievement in metadata.achievements:
                    print(f"  • {achievement}")
            
            if metadata.challenges:
                print(f"\n⚠️ CHALLENGES:")
                for challenge in metadata.challenges:
                    print(f"  • {challenge}")
        
        # Monthly-specific fields
        if metadata.note_type == "monthly":
            if metadata.skills_developed:
                print(f"\n🎓 SKILLS DEVELOPED:")
                for skill in metadata.skills_developed:
                    print(f"  • {skill}")
            
            if metadata.strategic_insights:
                print(f"\n🔍 STRATEGIC INSIGHTS:")
                for insight in metadata.strategic_insights:
                    print(f"  • {insight}")
        
        # Common fields
        if metadata.tools:
            print(f"\n🔧 TOOLS: {', '.join(metadata.tools)}")
        
        if metadata.people:
            print(f"\n👥 PEOPLE: {', '.join(metadata.people)}")
        
        if metadata.metrics:
            print(f"\n📊 METRICS:")
            for metric, value in metadata.metrics.items():
                print(f"  • {metric}: {value}")
        
        return metadata_dict


def demo_extraction():
    """Demo extraction on sample notes"""
    extractor = SimpleMetadataExtractor()
    
    # Test on available notes (daily, weekly, monthly)
    test_files = [
        Path("chronicle/Daily Notes/2025-06-29.md"),
        Path("chronicle/Daily Notes/2025-06-30.md"),
        Path("chronicle/Weekly Notes/2025-W26.md"),
        Path("chronicle/Monthly Notes/2025-06.md"),
    ]
    
    all_metadata = []
    
    for file_path in test_files:
        if file_path.exists():
            print(f"\n{'#'*60}")
            print(f"# {file_path.name}")
            print(f"{'#'*60}")
            
            metadata = extractor.extract_and_display(file_path)
            all_metadata.append(metadata)
        else:
            print(f"File not found: {file_path}")
    
    # Save results
    if all_metadata:
        output_file = "extraction_results_simple.json"
        with open(output_file, 'w') as f:
            json.dump(all_metadata, f, indent=2)
        print(f"\n✅ Saved to: {output_file}")


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Running simplified metadata extraction...")
    demo_extraction()