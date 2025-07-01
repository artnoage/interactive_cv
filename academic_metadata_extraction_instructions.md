# Academic Metadata Extraction Instructions

## Overview
You are tasked with extracting comprehensive metadata from academic paper analyses. Each analysis contains detailed information about a research paper. Your goal is to extract structured metadata that captures the essence of each paper's contributions, methods, and connections to other work.

## Input Files
- **Location**: `/academic/Transcript_Analysis/` directory
- **Format**: Markdown files ending with `_analysis.md`
- **Structure**: Each file contains sections like Executive Summary, Methodology Analysis, Key Results, etc.

## Output Format
Create a JSON file called `academic_metadata.json` with the following structure for each paper:

```json
{
  "papers": [
    {
      "file_path": "academic/Transcript_Analysis/[filename].md",
      "paper_title": "Extract from the analysis title or first heading",
      "authors": ["List of authors if mentioned"],
      "year": "Publication year if mentioned",
      "venue": "Journal or conference if mentioned",
      
      "core_contribution": "One sentence describing the main contribution",
      "problem_solved": "What problem does this paper address?",
      
      "mathematical_concepts": [
        "Monge-Ampère equation",
        "Kantorovich potential",
        "Wasserstein distance",
        "etc."
      ],
      
      "methods_and_techniques": [
        "neural networks",
        "gradient flows",
        "Monte Carlo methods",
        "etc."
      ],
      
      "algorithms_introduced": [
        "Name and brief description of any algorithms"
      ],
      
      "theoretical_results": [
        "Key theorems or theoretical findings"
      ],
      
      "applications": [
        "domain adaptation",
        "generative modeling",
        "risk-sensitive control",
        "etc."
      ],
      
      "key_innovations": [
        "What's novel about this work?",
        "What makes it different from prior work?"
      ],
      
      "research_areas": [
        "optimal transport",
        "stochastic control",
        "machine learning",
        "etc."
      ],
      
      "related_concepts": [
        "Concepts that connect to other papers or fields"
      ],
      
      "collaborators": [
        "Co-authors and institutions mentioned"
      ],
      
      "limitations": [
        "Known limitations or challenges"
      ],
      
      "future_directions": [
        "Suggested future work or open problems"
      ],
      
      "connections_to_other_work": {
        "builds_on": ["Papers or concepts this work extends"],
        "enables": ["What this work makes possible"],
        "related_to": ["Similar or connected papers"]
      },
      
      "practical_impact": "How this work could be applied in practice",
      
      "code_available": "boolean or link if mentioned",
      
      "key_equations": [
        "Important mathematical formulations if any"
      ],
      
      "datasets_used": [
        "Any datasets mentioned"
      ]
    }
  ]
}
```

## Extraction Guidelines

### 1. Title and Basic Info
- Extract the paper title from the analysis heading or content
- Look for author names, publication year, and venue
- If not explicitly stated, mark as "not specified"

### 2. Core Contributions
- Find the main contribution in the Executive Summary or Introduction
- Summarize in one clear sentence
- Identify the specific problem being solved

### 3. Mathematical and Technical Content
- Extract all mathematical concepts mentioned (equations, theorems, spaces)
- List computational methods and algorithms
- Note any theoretical results or proofs

### 4. Applications and Impact
- Identify all mentioned applications
- Note both theoretical and practical impacts
- Look for experimental results or use cases

### 5. Connections and Context
- Find references to other papers or researchers
- Identify which research areas the paper contributes to
- Note how it builds on or enables other work

### 6. Critical Analysis
- Extract mentioned limitations
- Find suggested future directions
- Note any open problems

## Special Instructions

1. **Be Comprehensive**: Extract all relevant concepts, even if they seem minor
2. **Use Original Language**: When possible, use the exact terminology from the analysis
3. **Identify Patterns**: Look for recurring themes across papers (e.g., "optimal transport" appearing in multiple papers)
4. **Note Relationships**: Pay special attention to how papers relate to each other
5. **Include Context**: Don't just list items - include brief context when helpful

## Quality Checks

Before finalizing, ensure:
- [ ] All papers in the directory are processed
- [ ] Each paper has at least: title, core contribution, methods, and research areas
- [ ] Mathematical concepts are accurately captured
- [ ] Connections between papers are identified
- [ ] The JSON is valid and properly formatted

## Example Entry

```json
{
  "file_path": "academic/Transcript_Analysis/Universal_Neural_Optimal_Transport_analysis.md",
  "paper_title": "Universal Neural Optimal Transport",
  "authors": ["not specified"],
  "year": "not specified",
  "venue": "not specified",
  
  "core_contribution": "A universal framework for learning optimal transport maps using neural networks by training them to solve the Monge-Ampère equation",
  "problem_solved": "Existing neural OT methods are specialized to specific cost functions; this provides a flexible, universal solver",
  
  "mathematical_concepts": [
    "Monge-Ampère equation",
    "Kantorovich potential",
    "Wasserstein distance",
    "convex optimization",
    "PDE theory"
  ],
  
  "methods_and_techniques": [
    "Physics-Informed Neural Networks (PINNs)",
    "automatic differentiation",
    "gradient-based optimization"
  ],
  
  "applications": [
    "domain adaptation",
    "generative modeling",
    "color correction",
    "mesh generation"
  ],
  
  "key_innovations": [
    "Using Monge-Ampère equation as a loss function",
    "Learning the potential instead of the transport map directly",
    "Decoupling from specific cost functions"
  ],
  
  "research_areas": [
    "optimal transport",
    "deep learning",
    "computational mathematics"
  ]
}
```

## Final Output
Save all extracted metadata as `academic_metadata.json` in the project root directory.