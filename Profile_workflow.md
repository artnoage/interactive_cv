# Claude Academic Profile Workflow

## Overview
This workflow guides an AI agent through analyzing academic papers to build a comprehensive researcher profile that captures expertise areas, methodological approaches, and intellectual contributions.

## Parameters
- **Input**: Path to folder containing paper analyses (e.g., `/academic_work/Transcript_Analysis/`)
- **Output**: Academic profile file with synthesis and assessment questions

## Workflow Steps

### Step 1: Initial Data Collection
1. Load all paper analysis files from the specified folder
2. Create a tracking document listing:
   - Paper titles
   - Publication years (if available)
   - Co-authors
   - Main research areas

### Step 2: Structured Data Extraction
For each paper analysis, extract and store in structured format (JSON/dictionary):

**Core Academic Markers**:
- **Primary Fields**: Main research areas (e.g., Optimal Transport, Machine Learning)
- **Sub-Fields**: Specialized areas (e.g., Stochastic Control, Information Geometry)
- **Mathematical Concepts**: Core theoretical elements (e.g., Wasserstein distances, variational inequalities)
- **Methodologies**: Technical approaches and frameworks
- **Applications**: Real-world problem domains
- **Key Terminology**: Significant recurring terms

**Technical Competencies**:
- Theoretical techniques mastered
- Computational methods employed
- Software/tools utilized
- Programming languages (if applicable)

**Innovation Patterns**:
- Problem types addressed
- Methodological contributions
- Novel connections established

### Step 3: Cross-Analysis & Knowledge Graph (Meta-Analysis Core)
Analyze connections BETWEEN papers to build comprehensive understanding:

**Conceptual Evolution**:
- Track how concepts from one paper inform or evolve in others
- Identify theoretical foundations that underpin multiple works
- Map progression of ideas across research timeline

**Methodological Connections**:
- Common mathematical frameworks across papers
- Technique refinements and adaptations
- Cross-pollination of methods between domains

**Research Trajectory Mapping**:
- Temporal evolution of research focus
- Branching into new areas while maintaining core expertise
- Integration of diverse mathematical tools

### Step 4: Profile Synthesis
Generate sections for:

**1. Research Identity**
- Primary field of expertise
- Secondary areas of competence
- Unique niche/specialization

**2. Technical Mastery**
- Core mathematical tools
- Computational skills
- Theoretical frameworks

**3. Research Style**
- Problem selection patterns
- Collaboration network
- Innovation approach

**4. Impact & Applications**
- Real-world applications
- Theoretical contributions
- Interdisciplinary connections

**5. Research Trajectory & Interconnections**
- Temporal evolution of research themes
- How concepts from early work inform later papers
- Emerging patterns and future directions
- Intellectual journey narrative

### Step 5: Spherical Assessment
Evaluate the "sphericalness" of the profile:
- **Breadth**: Coverage across different mathematical domains
- **Depth**: Level of expertise in each area
- **Connectivity**: Links between different research areas
- **Balance**: Distribution of theoretical vs. applied work

Score each dimension 1-10 and visualize as a radar chart description.

### Step 6: Generate Assessment Questions
Create tailored questions across five categories:

**1. Probe for Depth**:
- "Your work frequently utilizes [specific framework]. What are its advantages and limitations compared to [alternative approach]?"
- "In [specific paper], you employ [technique]. How does this choice reflect your mathematical philosophy?"

**2. Explore Intersections**:
- "How does your understanding of [concept from paper A] inform your approach to [problem in paper B]?"
- "What unexpected connections have you discovered between [field 1] and [field 2] through your research?"

**3. Challenge Assumptions**:
- "In your analysis of [topic], you rely on [assumption/method]. What would change if this constraint were relaxed?"
- "Which fundamental assumptions in your field do you think deserve re-examination?"

**4. Encourage Synthesis**:
- "Looking across your papers, what is the single most powerful mathematical tool you've developed, and how would you apply it to [completely different domain]?"
- "If you could combine insights from any three of your papers, which would create the most impactful new research direction?"

**5. Future Outlook**:
- "What emerging mathematical frameworks could revolutionize your work on [specific topic]?"
- "Based on your research trajectory, what problem do you predict will occupy the field in 10 years?"

### Step 7: Output Generation
Create the profile document with:
1. High-level summary (2-3 sentences capturing research essence)
2. Knowledge areas & expertise (detailed narrative by field)
3. Core competencies (structured lists):
   - Theoretical expertise
   - Methodological toolkit
   - Application focus
4. Research trajectory & interconnections (meta-analysis findings)
5. Spherical profile assessment (with scoring)
6. Questions for deeper inquiry (categorized by type)
7. Growth recommendations

## Implementation Notes

**For the Agent**:
- Read each analysis file completely
- Look for patterns across papers
- Note evolution over time
- Identify unique contributions
- Balance technical accuracy with accessibility

**Quality Checks**:
- Ensure all papers are represented
- Verify mathematical concepts are correctly categorized
- Check for coherent narrative in research evolution
- Validate that questions genuinely probe the researcher's expertise

**Output File Structure**:
```
academic_profile_[researcher_name].md
├── Executive Summary
├── Core Competencies
├── Knowledge Graph
├── Research Evolution
├── Spherical Profile Assessment
├── Assessment Questions
└── Growth Recommendations
```

## Example Usage
```
Input: /academic_work/Transcript_Analysis/
Output: academic_profile_vaios_laschos.md
```

The resulting profile should provide a holistic view of the researcher's intellectual landscape, highlighting both specialized expertise and interdisciplinary potential.