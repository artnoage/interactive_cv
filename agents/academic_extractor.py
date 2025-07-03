#!/usr/bin/env python3
"""
Academic paper metadata extractor
Based on the academic extraction schema for research papers
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


class AcademicMetadata(BaseModel):
    """Schema for academic paper metadata extraction aligned with analysis guide"""
    
    # Core paper information
    title: str = Field(description="Paper title")
    authors: List[str] = Field(description="Paper authors", default=[])
    year: Optional[str] = Field(description="Publication year")
    venue: Optional[str] = Field(description="Journal/conference venue")
    domain: Optional[str] = Field(
        description="Primary domain: mathematics, computer_science, or physics"
    )
    core_contribution: str = Field(description="Main contribution of the paper")
    
    # Phase 1: Rapid Reconnaissance
    problem_addressed: Optional[str] = Field(
        description="The core problem being solved"
    )
    initial_assessment: Optional[str] = Field(
        description="Initial judgement of relevance and credibility"
    )
    
    # Phase 2: Deep Dive - Technical Content
    mathematical_concepts: List[Dict[str, str]] = Field(
        description="Mathematical concepts with: name, category, description", default=[]
    )
    
    methods: List[Dict[str, str]] = Field(
        description="Methods used with: name, type, description", default=[]
    )
    
    algorithms: List[Dict[str, str]] = Field(
        description="Algorithms with: name, purpose, key_idea, complexity", default=[]
    )
    
    # Critical Analysis Elements
    assumptions: List[str] = Field(
        description="Key assumptions and approximations made", default=[]
    )
    
    limitations: List[str] = Field(
        description="Limitations and boundaries of applicability", default=[]
    )
    
    # Evaluation & Validation
    evaluation_details: Optional[Dict[str, str]] = Field(
        description="Evaluation approach with: datasets, metrics, baselines, results"
    )
    
    proof_scrutiny: Optional[Dict[str, str]] = Field(
        description="For mathematical papers: proof_strategy, key_lemmas, potential_gaps"
    )
    
    # Phase 3: Synthesis & Future Work
    key_insights: List[str] = Field(
        description="Core insights distilled from the paper", default=[]
    )
    
    future_work: List[str] = Field(
        description="Open questions and future research directions", default=[]
    )
    
    practical_implications: List[str] = Field(
        description="Real-world applications and broader impact", default=[]
    )
    
    # Context & Connections
    research_areas: List[str] = Field(
        description="Research areas and fields", default=[]
    )
    
    innovations: List[str] = Field(
        description="Novel approaches and key innovations", default=[]
    )
    
    applications: List[Dict[str, str]] = Field(
        description="Applications with: domain, use_case, impact", default=[]
    )
    
    # People & Institutions
    people: List[str] = Field(
        description="People mentioned (full names only)", default=[]
    )
    
    institutions: List[str] = Field(
        description="Institutions and organizations mentioned", default=[]
    )


class AcademicExtractor:
    """Academic paper metadata extractor"""
    
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
                "X-Title": "Academic Paper Metadata Extractor",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=AcademicMetadata)
        
        # Academic analysis-focused prompt aligned with the analysis guide
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are extracting structured metadata from academic paper analyses that follow a specific three-phase structure.

The analyses are organized according to these phases:

PHASE 1 - RAPID RECONNAISSANCE:
- Executive Summary section
- Title, Abstract, and Introduction analysis
- Structure Overview
- Key Findings
- Initial Assessment

PHASE 2 - DEEP DIVE (Domain-specific):
For Mathematics papers, look for:
- Landscape understanding
- Core Result analysis
- Proof Scrutiny (proof strategy, key lemmas, potential gaps)
- Examples and Counterexamples
- Significance assessment

For Computer Science papers, look for:
- Problem Formulation
- Algorithm/System Analysis (complexity, innovation)
- Evaluation and Experiments (datasets, metrics, baselines, results)
- Reproducibility details
- Broader Impact assessment

For Physics papers, look for:
- Theoretical Framework
- Experimental Setup
- Data Analysis & Results
- Theory/Experiment connection

PHASE 3 - SYNTHESIS & FUTURE WORK:
- Key insights distilled
- Contextualization
- Open questions and limitations
- Future implications

CRITICAL ANALYSIS ELEMENTS (throughout):
- Assumptions and approximations
- Limitations and boundaries
- Alternative explanations
- Evidence quality

Extract metadata according to this structure:

1. First determine the domain (mathematics, computer_science, or physics)
2. Extract from phase-specific sections
3. Capture critical analysis elements (assumptions, limitations)
4. Include synthesis elements (future work, open questions)

Categories for mathematical concepts: theory, space, metric, operator, functional, equation, principle
Categories for methods: analytical, computational, algorithmic, theoretical, experimental
Application domains: machine_learning, robotics, finance, healthcare, physics, biology, engineering, optimization, control_systems, other

Be precise and technical. Extract full names for people (no usernames or placeholders)."""),
            
            ("human", """Extract comprehensive metadata from this academic paper analysis following the three-phase structure:

{content}

{format_instructions}""")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    def extract_metadata(self, content: str) -> AcademicMetadata:
        """Extract metadata from academic paper content"""
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
        metadata = AcademicMetadata(**metadata_dict)
        
        print(f"\n{'='*80}")
        print(f"ACADEMIC PAPER: {metadata.title}")
        if metadata.domain:
            print(f"DOMAIN: {metadata.domain.upper()}")
        print(f"{'='*80}")
        
        # Phase 1: Core Information
        if metadata.authors:
            print(f"\n👥 AUTHORS: {', '.join(metadata.authors)}")
        
        if metadata.year:
            print(f"📅 YEAR: {metadata.year}")
        
        if metadata.venue:
            print(f"📍 VENUE: {metadata.venue}")
        
        if metadata.problem_addressed:
            print(f"\n🎯 PROBLEM ADDRESSED: {metadata.problem_addressed}")
        
        print(f"\n🚀 CONTRIBUTION: {metadata.core_contribution}")
        
        # Phase 2: Technical Content
        if metadata.research_areas:
            print(f"\n🔬 RESEARCH AREAS: {', '.join(metadata.research_areas)}")
        
        if metadata.mathematical_concepts:
            print(f"\n📐 MATHEMATICAL CONCEPTS ({len(metadata.mathematical_concepts)}):")
            for concept in metadata.mathematical_concepts[:5]:  # Show top 5
                print(f"  • {concept['name']} ({concept.get('category', 'N/A')})")
        
        if metadata.methods:
            print(f"\n🔧 METHODS ({len(metadata.methods)}):")
            for method in metadata.methods[:5]:  # Show top 5
                print(f"  • {method['name']} ({method.get('type', 'N/A')})")
        
        if metadata.algorithms:
            print(f"\n⚙️ ALGORITHMS ({len(metadata.algorithms)}):")
            for algo in metadata.algorithms:
                print(f"  • {algo['name']}: {algo.get('purpose', 'N/A')}")
        
        # Critical Analysis
        if metadata.assumptions:
            print(f"\n⚠️ KEY ASSUMPTIONS:")
            for assumption in metadata.assumptions[:3]:  # Show top 3
                print(f"  • {assumption}")
        
        if metadata.limitations:
            print(f"\n🚧 LIMITATIONS:")
            for limitation in metadata.limitations[:3]:  # Show top 3
                print(f"  • {limitation}")
        
        # Phase 3: Synthesis
        if metadata.key_insights:
            print(f"\n💡 KEY INSIGHTS:")
            for insight in metadata.key_insights[:3]:  # Show top 3
                print(f"  • {insight}")
        
        if metadata.future_work:
            print(f"\n🔮 FUTURE WORK:")
            for work in metadata.future_work[:3]:  # Show top 3
                print(f"  • {work}")
        
        if metadata.practical_implications:
            print(f"\n🌍 PRACTICAL IMPLICATIONS:")
            for impl in metadata.practical_implications[:2]:  # Show top 2
                print(f"  • {impl}")
        
        # Additional
        if metadata.innovations:
            print(f"\n✨ INNOVATIONS:")
            for innovation in metadata.innovations[:3]:  # Show top 3
                print(f"  • {innovation}")
        
        if metadata.institutions:
            print(f"\n🏛️ INSTITUTIONS: {', '.join(metadata.institutions)}")
        
        return metadata_dict


def demo_extraction():
    """Demo extraction on academic papers"""
    extractor = AcademicExtractor()
    
    # Test on available academic paper analyses
    test_files = [
        Path("../raw_data/academic/Transcript_Analysis/Universal_Neural_Optimal_Transport_analysis.md"),
        Path("../raw_data/academic/Transcript_Analysis/Training_GANs_arbitrary_OT_costs_analysis.md"),
        Path("../raw_data/academic/Transcript_Analysis/Wasserstein_gradient_flows_large_deviations_analysis.md"),
    ]
    
    all_metadata = []
    
    for file_path in test_files:
        if file_path.exists():
            print(f"\n{'#'*80}")
            print(f"# {file_path.name}")
            print(f"{'#'*80}")
            
            metadata = extractor.extract_and_display(file_path)
            all_metadata.append(metadata)
        else:
            print(f"File not found: {file_path}")
    
    # Save results
    if all_metadata:
        output_file = "academic_extraction_results.json"
        with open(output_file, 'w') as f:
            json.dump(all_metadata, f, indent=2)
        print(f"\n✅ Saved to: {output_file}")


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Running academic paper metadata extraction...")
    demo_extraction()