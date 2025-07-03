#!/usr/bin/env python3
"""
Academic Paper Analyzer Agent
Analyzes research papers following the methodology in How_to_analyze.md
Produces structured analyses that can then be processed by the academic_extractor
"""

import os
import json
from typing import Dict, List, Optional, Literal, Any
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
    title: Optional[str] = Field(description="Paper title", default=None)
    authors: List[str] = Field(description="Paper authors", default=[])
    year: Optional[str] = Field(description="Publication year", default=None)
    venue: Optional[str] = Field(description="Journal/conference venue", default=None)
    domain: Optional[Literal["mathematics", "computer_science", "physics"]] = Field(
        description="Primary domain of the paper", default="mathematics"
    )
    analysis_date: str = Field(description="Date of analysis", default_factory=lambda: datetime.now().isoformat())
    
    # Phase 1: Rapid Reconnaissance
    executive_summary: Optional[str] = Field(
        description="2-3 paragraph summary of the paper's core contribution and significance", default=None
    )
    
    problem_addressed: Optional[str] = Field(
        description="The core problem being solved", default=None
    )
    
    core_contribution: Optional[str] = Field(
        description="Main contribution of the paper", default=None
    )
    
    initial_assessment: Optional[str] = Field(
        description="Initial judgement of relevance and credibility", default=None
    )
    
    claimed_contributions: List[str] = Field(
        description="Main contributions claimed by the authors", default=[]
    )
    
    structure_overview: Optional[str] = Field(
        description="Overview of paper structure", default=None
    )
    
    key_findings: List[str] = Field(
        description="Key findings from the paper", default=[]
    )
    
    # Phase 2: Deep Dive - Technical Content
    research_context: Optional[Dict[str, str]] = Field(
        description="Historical context, current state, prior limitations", default=None
    )
    
    methodology_analysis: Optional[Dict[str, List[str]]] = Field(
        description="Key technical innovations, mathematical framework", default=None
    )
    
    domain_specific_analysis: Optional[Dict[str, str]] = Field(
        description="Analysis specific to the paper's domain", default=None
    )
    
    critical_examination: Optional[Dict[str, List[str]]] = Field(
        description="Assumptions, limitations, evidence quality", default=None
    )
    
    mathematical_concepts: List[Dict[str, str]] = Field(
        description="Mathematical concepts with name, category, description", default=[]
    )
    
    methods: List[Dict[str, str]] = Field(
        description="Methods with name, type, description", default=[]
    )
    
    algorithms: List[Dict[str, str]] = Field(
        description="Algorithms with name, purpose, key_idea, complexity", default=[]
    )
    
    assumptions: List[str] = Field(
        description="Key assumptions made in the paper", default=[]
    )
    
    limitations: List[str] = Field(
        description="Limitations of the approach", default=[]
    )
    
    evaluation_details: Optional[Dict[str, str]] = Field(
        description="Evaluation approach details", default=None
    )
    
    proof_scrutiny: Optional[Dict[str, str]] = Field(
        description="Proof analysis for mathematical papers", default=None
    )
    
    # Phase 3: Synthesis & Future Work
    key_insights: List[str] = Field(
        description="Key insights distilled from the paper", default=[]
    )
    
    future_work: List[str] = Field(
        description="Future research directions", default=[]
    )
    
    practical_implications: List[str] = Field(
        description="Practical implications of the work", default=[]
    )
    
    # Context & Connections
    research_areas: List[str] = Field(
        description="Research areas this paper contributes to", default=[]
    )
    
    innovations: List[str] = Field(
        description="Key innovations introduced", default=[]
    )
    
    applications: List[Dict[str, str]] = Field(
        description="Applications with domain, use_case, impact", default=[]
    )
    
    people: List[str] = Field(
        description="People mentioned in the paper", default=[]
    )
    
    institutions: List[str] = Field(
        description="Institutions mentioned", default=[]
    )
    
    theoretical_results: List[str] = Field(
        description="Theoretical results presented", default=[]
    )
    
    related_concepts: List[str] = Field(
        description="Related concepts and ideas", default=[]
    )
    
    connections_to_other_work: Optional[Dict[str, List[str]]] = Field(
        description="Connections to other research work", default=None
    )
    
    # Meta information
    thinking_patterns: Optional[Dict[str, str]] = Field(
        description="Thinking patterns observed in the paper", default=None
    )
    
    quality_assessment: Optional[Dict[str, str]] = Field(
        description="Assessment of paper quality", default=None
    )


class AcademicAnalyzer:
    """Analyzes academic papers following the How_to_analyze.md methodology"""
    
    def __init__(self, use_pro_model: bool = False):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        model_name = "google/gemini-2.5-pro" if use_pro_model else "google/gemini-2.5-flash"
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
        self.use_pro_model = use_pro_model
    
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
            ("system", """You are an expert academic paper analyzer. Your task is to analyze academic papers and extract comprehensive metadata based on the provided content. Follow a systematic three-phase methodology to ensure thoroughness.

ANALYSIS METHODOLOGY:

Phase 1: Rapid Reconnaissance
- Read Title, Abstract, Introduction to grasp the core.
- Scan headings and figures for structure.
- Read conclusion for author's summary.
- Make initial assessment of relevance and credibility.

Phase 2: Deep Dive (Domain-Specific Analysis)
- Understand the landscape and subfield.
- Grasp the core result (theorem/lemma/proposition).
- Scrutinize proofs for gaps and hand-wavy arguments.
- Consider examples, counterexamples, and edge cases.
- Assess significance (solves open problem? unifies areas?).
- Analyze problem formulation, algorithms/systems, evaluation, reproducibility, and broader impact for CS papers.
- Analyze theoretical framework, experimental setup, data analysis, and theory/experiment connection for Physics papers.

Phase 3: Synthesis & Future Work
- Distill key insights.
- Contextualize within the field.
- Identify limitations and open questions.
- Project future implications.

CRITICAL EXAMINATION throughout:
- Evidence quality assessment.
- Logic chain validation.
- Alternative explanations.
- Boundary conditions and limitations.

Extract the following information, ensuring it aligns with the specified types and descriptions:

Core paper information:
- title: Paper title
- authors: List of paper authors (full names only)
- year: Publication year
- venue: Journal/conference venue
- domain: Primary domain (mathematics, computer_science, or physics)
- core_contribution: Main contribution of the paper

Phase 1: Rapid Reconnaissance
- executive_summary: 2-3 paragraph summary of the paper's core contribution and significance
- problem_addressed: The core problem being solved
- initial_assessment: Initial judgement of relevance and credibility
- claimed_contributions: Main contributions claimed by the authors
- structure_overview: Brief description of how the paper is organized
- key_findings: Most important results or discoveries

Phase 2: Deep Dive - Technical Content
- research_context: Historical context, current state, prior limitations, and advancement
- methodology_analysis: Key technical innovations, mathematical framework, implementation details
- domain_specific_analysis: Analysis specific to the paper's domain (math/CS/physics)
- critical_examination: Assumptions, limitations, alternative explanations, evidence quality
- mathematical_concepts: List of mathematical concepts with: name, category (theory, space, metric, operator, functional, equation, principle), description
- methods: List of methods used with: name, type (analytical, computational, algorithmic, theoretical, experimental), description
- algorithms: List of algorithms with: name, purpose, key_idea, complexity

Evaluation & Validation:
- evaluation_details: Evaluation approach with: datasets, metrics, baselines, results (for CS/Physics papers)
- proof_scrutiny: For mathematical papers: proof_strategy, key_lemmas, potential_gaps

Phase 3: Synthesis & Future Work:
- key_insights: Core insights distilled from the paper
- contextualization: How this changes understanding of the field
- open_questions: Questions raised by this work
- future_work: Open questions and future research directions
- practical_implications: Real-world applications and broader impact

Context & Connections:
- research_areas: Research areas and fields
- innovations: Novel approaches and key innovations
- applications: Applications with: domain, use_case, impact
- people: People mentioned (full names only), including collaborators
- institutions: Institutions and organizations mentioned
- theoretical_results: Key theoretical results or theorems proven in the paper
- related_concepts: Concepts closely related to the paper's topic but not directly part of its core contribution
- connections_to_other_work:         description="How this work builds on, enables, or relates to other specific papers or research directions (e.g., a dictionary with keys like 'builds_on', 'enables', 'related_to' and lists of strings as values)", default={{}}
    )

Meta information:
- thinking_patterns: Pattern recognition, systems thinking, probabilistic reasoning observed
- quality_assessment: Coherence, completeness, bias assessment

IMPORTANT: You MUST provide comprehensive content for ALL THREE PHASES:
- Phase 1: Basic information and initial assessment
- Phase 2: Deep technical analysis including mathematical_concepts, methods, algorithms, assumptions, limitations
- Phase 3: Synthesis including key_insights, future_work, practical_implications

For each field in the output schema:
- mathematical_concepts: Extract ALL mathematical concepts (spaces, metrics, operators, etc.)
- methods: List ALL methods used (analytical, computational, theoretical)
- algorithms: Detail any algorithms mentioned
- key_insights: Provide at least 3-5 key insights
- future_work: List future directions mentioned or implied
- research_areas: List all relevant research areas
- theoretical_results: List main theorems, lemmas, propositions

Be precise, technical, and critical in your extraction. Even if not explicitly stated, infer and extract based on your understanding of the paper.
"""),
            
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
            print("Attempting with manual parsing...")
            
            # Try to parse the LLM response manually
            try:
                # Get raw response from LLM without parser
                raw_response = self.llm.invoke(
                    self.prompt.format_messages(
                        content=content,
                        format_instructions=self.parser.get_format_instructions()
                    )
                )
                
                # Extract JSON from the response
                import re
                content_str = raw_response.content if isinstance(raw_response.content, str) else str(raw_response.content)
                json_match = re.search(r'\{.*\}', content_str, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    data = json.loads(json_str)
                    
                    # Fill in missing required fields with defaults
                    if 'title' not in data:
                        data['title'] = "Unknown Title"
                    if 'domain' not in data:
                        data['domain'] = 'mathematics'
                    
                    # Create PaperAnalysis with defaults for missing fields
                    return PaperAnalysis(**data)
            except Exception as manual_e:
                print(f"Manual parsing also failed: {manual_e}")
            
            # If all else fails, return a minimal analysis
            print("Returning minimal analysis due to parsing failures")
            return PaperAnalysis(
                title="Analysis Failed - Check Original Document",
                domain="mathematics",
                executive_summary="Failed to parse the paper analysis. Please check the original document.",
                problem_addressed="Unable to extract",
                core_contribution="Unable to extract"
            )
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a paper file and return analysis dict"""
        print(f"Analyzing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = self.analyze_paper(content)
        
        result = analysis.model_dump()
        result['analysis_date'] = datetime.now().isoformat()
        
        # Ensure all required fields are present, even if empty
        for field_name, field_info in PaperAnalysis.model_fields.items():
            if field_name not in result:
                if field_info.annotation == List[str]:
                    result[field_name] = []
                elif field_info.annotation == Dict[str, str] or field_info.annotation == Dict[str, List[str]]:
                    result[field_name] = {}
                elif field_info.annotation == Optional[str]:
                    result[field_name] = None
                elif field_info.annotation == str:
                    result[field_name] = ""
                elif field_info.annotation == Literal["mathematics", "computer_science", "physics"]:
                    # Default to a sensible value or handle as appropriate
                    result[field_name] = "mathematics" # Or raise an error if no default is suitable

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
        title = analysis.get('title', 'Unknown Paper')
        md = f"# Analysis of {title}\n\n"
        
        # Basic Information
        if analysis.get('authors'):
            md += f"**Authors**: {', '.join(analysis['authors'])}\n"
        if analysis.get('year'):
            md += f"**Year**: {analysis['year']}\n"
        if analysis.get('venue'):
            md += f"**Venue**: {analysis['venue']}\n"
        domain = analysis.get('domain', 'mathematics')
        md += f"**Domain**: {domain.replace('_', ' ').title()}\n"
        md += f"**Analysis Date**: {analysis['analysis_date']}\n\n"

        # Executive Summary
        md += "## Executive Summary\n\n"
        if analysis.get('executive_summary'):
            md += f"{analysis['executive_summary']}\n\n"
        else:
            md += "*No executive summary available*\n\n"
        
        # Phase 1: Rapid Reconnaissance
        md += "## Phase 1: Rapid Reconnaissance\n\n"
        
        md += "### Problem Addressed\n"
        if analysis.get('problem_addressed'):
            md += f"{analysis['problem_addressed']}\n\n"
        else:
            md += "*Problem not specified*\n\n"
        
        md += "### Core Contribution\n"
        if analysis.get('core_contribution'):
            md += f"{analysis['core_contribution']}\n\n"
        else:
            md += "*Core contribution not specified*\n\n"
        
        if analysis.get('initial_assessment'):
            md += "### Initial Assessment\n"
            md += f"{analysis['initial_assessment']}\n\n"

        if analysis.get('claimed_contributions'):
            md += "### Claimed Contributions\n"
            for contrib in analysis['claimed_contributions']:
                md += f"- {contrib}\n"
            md += "\n"

        if analysis.get('structure_overview'):
            md += "### Structure Overview\n"
            md += f"{analysis['structure_overview']}\n\n"

        if analysis.get('key_findings'):
            md += "### Key Findings\n"
            for finding in analysis['key_findings']:
                md += f"- {finding}\n"
            md += "\n"

        if analysis.get('research_context'):
            md += "## Research Context\n\n"
            for key, value in analysis['research_context'].items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"

        if analysis.get('methodology_analysis'):
            md += "## Methodology Analysis\n\n"
            for key, items in analysis['methodology_analysis'].items():
                md += f"### {key.replace('_', ' ').title()}\n"
                for item in items:
                    md += f"- {item}\n"
                md += "\n"

        if analysis.get('domain_specific_analysis'):
            md += f"## Domain-Specific Analysis ({analysis['domain'].replace('_', ' ').title()})\n\n"
            for key, value in analysis['domain_specific_analysis'].items():
                md += f"### {key.replace('_', ' ').title()}\n"
                md += f"{value}\n\n"

        if analysis.get('critical_examination'):
            md += "## Critical Examination\n\n"
            for key, items in analysis['critical_examination'].items():
                md += f"### {key.replace('_', ' ').title()}\n"
                for item in items:
                    md += f"- {item}\n"
                md += "\n"

        # Phase 2: Deep Dive - Technical Content
        md += "## Phase 2: Deep Dive - Technical Content\n\n"

        if analysis.get('mathematical_concepts'):
            md += "### Mathematical Concepts\n"
            for concept in analysis['mathematical_concepts']:
                md += f"- **{concept.get('name', 'N/A')}** (Category: {concept.get('category', 'N/A')}): {concept.get('description', 'N/A')}\n"
            md += "\n"

        if analysis.get('methods'):
            md += "### Methods\n"
            for method in analysis['methods']:
                md += f"- **{method.get('name', 'N/A')}** (Type: {method.get('type', 'N/A')}): {method.get('description', 'N/A')}\n"
            md += "\n"

        if analysis.get('algorithms'):
            md += "### Algorithms\n"
            for algo in analysis['algorithms']:
                md += f"- **{algo.get('name', 'N/A')}** (Purpose: {algo.get('purpose', 'N/A')})\n"
                if algo.get('key_idea'):
                    md += f"  - Key Idea: {algo['key_idea']}\n"
                if algo.get('complexity'):
                    md += f"  - Complexity: {algo['complexity']}\n"
            md += "\n"

        # Critical Analysis Elements
        md += "## Critical Analysis Elements\n\n"
        if analysis.get('assumptions'):
            md += "### Assumptions\n"
            for assumption in analysis['assumptions']:
                md += f"- {assumption}\n"
            md += "\n"

        if analysis.get('limitations'):
            md += "### Limitations\n"
            for limitation in analysis['limitations']:
                md += f"- {limitation}\n"
            md += "\n"

        # Evaluation & Validation
        if analysis.get('evaluation_details'):
            md += "## Evaluation & Validation\n\n"
            for key, value in analysis['evaluation_details'].items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"

        if analysis.get('proof_scrutiny'):
            md += "## Proof Scrutiny (for Mathematical Papers)\n\n"
            for key, value in analysis['proof_scrutiny'].items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"

        # Phase 3: Synthesis & Future Work
        md += "## Phase 3: Synthesis & Future Work\n\n"
        
        md += "### Key Insights\n"
        for insight in analysis.get('key_insights', []):
            md += f"- {insight}\n"
        md += "\n"
        
        md += "### Future Work\n"
        for work in analysis.get('future_work', []):
            md += f"- {work}\n"
        md += "\n"
        
        md += "### Practical Implications\n"
        for impl in analysis.get('practical_implications', []):
            md += f"- {impl}\n"
        md += "\n"

        # Context & Connections
        md += "## Context & Connections\n\n"
        if analysis.get('research_areas'):
            md += "### Research Areas\n"
            for area in analysis.get('research_areas', []):
                md += f"- {area}\n"
            md += "\n"

        if analysis.get('innovations'):
            md += "### Innovations\n"
            for innovation in analysis.get('innovations', []):
                md += f"- {innovation}\n"
            md += "\n"

        if analysis.get('applications'):
            md += "### Applications\n"
            for app in analysis.get('applications', []):
                md += f"- **Domain**: {app.get('domain', 'N/A')}\n"
                md += f"  - Use Case: {app.get('use_case', 'N/A')}\n"
                md += f"  - Impact: {app.get('impact', 'N/A')}\n"
            md += "\n"

        if analysis.get('people'):
            md += "### People Mentioned\n"
            for person in analysis.get('people', []):
                md += f"- {person}\n"
            md += "\n"

        if analysis.get('institutions'):
            md += "### Institutions Mentioned\n"
            for institution in analysis.get('institutions', []):
                md += f"- {institution}\n"
            md += "\n"

        if analysis.get('theoretical_results'):
            md += "### Theoretical Results\n"
            for result in analysis.get('theoretical_results', []):
                md += f"- {result}\n"
            md += "\n"

        if analysis.get('related_concepts'):
            md += "### Related Concepts\n"
            for concept in analysis.get('related_concepts', []):
                md += f"- {concept}\n"
            md += "\n"

        if analysis.get('connections_to_other_work'):
            md += "### Connections to Other Work\n"
            for category, items in analysis.get('connections_to_other_work', {}).items():
                md += f"**{category.replace('_', ' ').title()}**:\n"
                for item in items:
                    md += f"- {item}\n"
                md += "\n"

        # Meta information
        if analysis.get('thinking_patterns'):
            md += "## Thinking Patterns Observed\n\n"
            for key, value in analysis.get('thinking_patterns', {}).items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
        
        if analysis.get('quality_assessment'):
            md += "## Quality Assessment\n\n"
            for key, value in analysis.get('quality_assessment', {}).items():
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
        
        md += "---\n"
        md += f"*Analysis performed on: {analysis['analysis_date']}*\n"
        
        return md


def demo_analyzer():
    """Demo the academic analyzer on a sample paper"""
    analyzer_pro = AcademicAnalyzer(use_pro_model=True)
    
    # Test on the specified paper transcript
    test_file = Path("/home/artnoage/Projects/interactive_cv/raw_data/academic/Transcript_MDs/Cone_geometry_Hellinger_Kantorovich.md")
    
    if test_file.exists():
        print(f"Analyzing paper with Pro model: {test_file.name}")
        print("=" * 80)
        analysis_pro = analyzer_pro.analyze_file(test_file)
        analyzer_pro.save_analysis(analysis_pro, output_path=Path("./cone_geometry_hellinger_kantorovich_pro_analysis.md"))
    
    


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    print("Running academic paper analyzer...")
    demo_analyzer()