#!/usr/bin/env python3
"""
Academic Paper Analyzer Agent
Analyzes research papers following the methodology in How_to_analyze.md
Produces structured analyses that can then be processed by the academic_extractor
"""

import os
import json
from typing import Dict, List, Optional, Literal
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


class PaperAnalysis(BaseModel):
    """Schema for comprehensive paper analysis following the three-phase structure"""
    
    # Basic Information
    title: str = Field(description="Paper title")
    file_path: str = Field(description="Path to the original paper")
    domain: Literal["mathematics", "computer_science", "physics"] = Field(
        description="Primary domain of the paper"
    )
    analysis_date: str = Field(description="Date of analysis")
    
    # Phase 1: Rapid Reconnaissance
    executive_summary: str = Field(
        description="2-3 paragraph summary of the paper's core contribution and significance"
    )
    
    core_problem: str = Field(
        description="The fundamental problem this paper addresses"
    )
    
    proposed_solution: str = Field(
        description="The paper's approach to solving the problem"
    )
    
    claimed_contributions: List[str] = Field(
        description="Main contributions claimed by the authors"
    )
    
    structure_overview: str = Field(
        description="Brief description of how the paper is organized"
    )
    
    key_findings: List[str] = Field(
        description="Most important results or discoveries"
    )
    
    initial_assessment: str = Field(
        description="Initial judgment of relevance, credibility, and significance"
    )
    
    # Phase 2: Deep Dive
    research_context: Dict[str, str] = Field(
        description="Historical context, current state, prior limitations, and advancement"
    )
    
    methodology_analysis: Dict[str, List[str]] = Field(
        description="Key technical innovations, mathematical framework, implementation details"
    )
    
    # Domain-specific analysis
    domain_specific_analysis: Dict[str, str] = Field(
        description="Analysis specific to the paper's domain (math/CS/physics)"
    )
    
    critical_examination: Dict[str, List[str]] = Field(
        description="Assumptions, limitations, alternative explanations, evidence quality"
    )
    
    # Phase 3: Synthesis & Future Work
    key_insights: List[str] = Field(
        description="Core insights distilled from the paper"
    )
    
    contextualization: str = Field(
        description="How this changes understanding of the field"
    )
    
    open_questions: List[str] = Field(
        description="Questions raised by this work"
    )
    
    future_implications: List[str] = Field(
        description="Potential future research directions and applications"
    )
    
    # Meta information
    thinking_patterns: Dict[str, str] = Field(
        description="Pattern recognition, systems thinking, probabilistic reasoning observed",
        default={}
    )
    
    quality_assessment: Dict[str, str] = Field(
        description="Coherence, completeness, bias assessment",
        default={}
    )


class AcademicAnalyzer:
    """Analyzes academic papers following the How_to_analyze.md methodology"""
    
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
                "X-Title": "Academic Paper Analyzer",
            },
            temperature=0.1,
            max_tokens=8000  # Increased for comprehensive analysis
        )
        
        self.parser = PydanticOutputParser(pydantic_object=PaperAnalysis)
        
        # Load the analysis guide content
        self.analysis_guide = self._load_analysis_guide()
        
        # Create the analysis prompt
        self.prompt = self._create_analysis_prompt()
        
        self.chain = self.prompt | self.llm | self.parser
    
    def _load_analysis_guide(self) -> str:
        """Load the How_to_analyze.md guide"""
        guide_path = Path(__file__).parent.parent / "raw_data" / "academic" / "How_to_analyze.md"
        if guide_path.exists():
            with open(guide_path, 'r') as f:
                return f.read()
        else:
            # Fallback to embedded key principles
            return """
            Phase 1: Rapid Reconnaissance - Grasp core problem, solution, and contributions
            Phase 2: Deep Dive - Critical technical analysis based on domain
            Phase 3: Synthesis - Distill insights and future implications
            """
    
    def _create_analysis_prompt(self) -> ChatPromptTemplate:
        """Create the comprehensive analysis prompt"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert academic paper analyzer following a systematic three-phase methodology.

ANALYSIS METHODOLOGY:

Phase 1: Rapid Reconnaissance (~15-30 minutes equivalent depth)
- Read Title, Abstract, Introduction to grasp the core
- Scan headings and figures for structure
- Read conclusion for author's summary
- Make initial assessment of relevance and credibility

Phase 2: Deep Dive (Domain-Specific Analysis)

For MATHEMATICS papers:
- Understand the landscape and subfield
- Grasp the core result (theorem/lemma/proposition)
- Scrutinize proofs for gaps and hand-wavy arguments
- Consider examples, counterexamples, and edge cases
- Assess significance (solves open problem? unifies areas?)

For COMPUTER SCIENCE papers:
- Precise problem formulation (inputs/outputs/constraints)
- Algorithm/system analysis (complexity, innovation)
- Evaluation scrutiny (datasets, metrics, baselines, statistical significance)
- Reproducibility assessment
- Broader impact consideration

For PHYSICS papers:
- Theoretical framework and assumptions
- Experimental setup and error analysis
- Data analysis and results presentation
- Theory/experiment connection
- Resolution of existing tensions

Phase 3: Synthesis & Future Work
- Distill key insights in 1-2 sentences
- Contextualize within the field
- Identify limitations and open questions
- Project future implications

CRITICAL EXAMINATION throughout:
- Evidence quality assessment
- Logic chain validation
- Alternative explanations
- Boundary conditions and limitations

THINKING PATTERNS to apply:
- Pattern Recognition: recurring themes and techniques
- Systems Thinking: interactions and feedback loops
- Probabilistic Reasoning: confidence levels, not certainties
- Dialectical Thinking: opposing viewpoints and synthesis

First determine the paper's domain, then apply the appropriate analytical framework."""),
            
            ("human", """Analyze this academic paper following the three-phase methodology:

{content}

Provide a comprehensive analysis covering all three phases. Be specific, technical, and critical.

{format_instructions}""")
        ])
    
    def analyze_paper(self, content: str) -> PaperAnalysis:
        """Analyze a paper and return structured analysis"""
        try:
            result = self.chain.invoke({
                "content": content,
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"Analysis error: {e}")
            raise
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a paper file and return analysis dict"""
        print(f"Analyzing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = self.analyze_paper(content)
        
        result = analysis.model_dump()
        result['file_path'] = str(file_path)
        result['analysis_date'] = datetime.now().isoformat()
        
        return result
    
    def save_analysis(self, analysis: Dict, output_path: Optional[Path] = None) -> Path:
        """Save analysis to markdown file"""
        if not output_path:
            # Create output filename based on input
            input_path = Path(analysis['file_path'])
            output_name = input_path.stem + "_analysis.md"
            output_path = input_path.parent / "analyses" / output_name
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Format analysis as markdown
        md_content = self._format_analysis_as_markdown(analysis)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Analysis saved to: {output_path}")
        return output_path
    
    def _format_analysis_as_markdown(self, analysis: Dict) -> str:
        """Format analysis dict as structured markdown"""
        md = f"# Analysis of \"{analysis['title']}\"\n\n"
        
        # Executive Summary
        md += "## Executive Summary\n\n"
        md += f"{analysis['executive_summary']}\n\n"
        
        # Phase 1: Rapid Reconnaissance
        md += "## Phase 1: Rapid Reconnaissance\n\n"
        
        md += "### Core Problem\n"
        md += f"{analysis['core_problem']}\n\n"
        
        md += "### Proposed Solution\n"
        md += f"{analysis['proposed_solution']}\n\n"
        
        md += "### Claimed Contributions\n"
        for contrib in analysis['claimed_contributions']:
            md += f"- {contrib}\n"
        md += "\n"
        
        md += "### Structure Overview\n"
        md += f"{analysis['structure_overview']}\n\n"
        
        md += "### Key Findings\n"
        for finding in analysis['key_findings']:
            md += f"- {finding}\n"
        md += "\n"
        
        md += "### Initial Assessment\n"
        md += f"{analysis['initial_assessment']}\n\n"
        
        # Research Context
        md += "## Research Context\n\n"
        for key, value in analysis['research_context'].items():
            md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
        
        # Methodology Analysis
        md += "## Methodology Analysis\n\n"
        for key, items in analysis['methodology_analysis'].items():
            md += f"### {key.replace('_', ' ').title()}\n"
            for item in items:
                md += f"- {item}\n"
            md += "\n"
        
        # Domain-Specific Analysis
        md += f"## Domain-Specific Analysis ({analysis['domain'].replace('_', ' ').title()})\n\n"
        for key, value in analysis['domain_specific_analysis'].items():
            md += f"### {key.replace('_', ' ').title()}\n"
            md += f"{value}\n\n"
        
        # Critical Examination
        md += "## Critical Examination\n\n"
        for key, items in analysis['critical_examination'].items():
            md += f"### {key.replace('_', ' ').title()}\n"
            for item in items:
                md += f"- {item}\n"
            md += "\n"
        
        # Phase 3: Synthesis
        md += "## Synthesis & Future Work\n\n"
        
        md += "### Key Insights\n"
        for insight in analysis['key_insights']:
            md += f"- {insight}\n"
        md += "\n"
        
        md += "### Contextualization\n"
        md += f"{analysis['contextualization']}\n\n"
        
        md += "### Open Questions\n"
        for question in analysis['open_questions']:
            md += f"- {question}\n"
        md += "\n"
        
        md += "### Future Implications\n"
        for implication in analysis['future_implications']:
            md += f"- {implication}\n"
        md += "\n"
        
        # Meta information
        if analysis.get('thinking_patterns'):
            md += "## Thinking Patterns Observed\n\n"
            for key, value in analysis['thinking_patterns'].items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
        
        if analysis.get('quality_assessment'):
            md += "## Quality Assessment\n\n"
            for key, value in analysis['quality_assessment'].items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
        
        md += "---\n"
        md += f"*Analysis performed on: {analysis['analysis_date']}*\n"
        
        return md


def demo_analyzer():
    """Demo the academic analyzer on a sample paper"""
    analyzer = AcademicAnalyzer()
    
    # Test on a sample paper transcript
    test_file = Path("../raw_data/academic/Transcript_MDs/Universal_Neural_Optimal_Transport.md")
    
    if test_file.exists():
        print(f"Analyzing paper: {test_file.name}")
        print("=" * 80)
        
        analysis = analyzer.analyze_file(test_file)
        
        # Save the analysis
        output_path = analyzer.save_analysis(analysis)
        
        print("\nAnalysis Summary:")
        print(f"Domain: {analysis['domain']}")
        print(f"Core Problem: {analysis['core_problem'][:100]}...")
        print(f"Key Insights: {len(analysis['key_insights'])}")
        print(f"Open Questions: {len(analysis['open_questions'])}")
        print(f"Future Implications: {len(analysis['future_implications'])}")
    else:
        print(f"Test file not found: {test_file}")


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Running academic paper analyzer...")
    demo_analyzer()