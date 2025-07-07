# Agents

This directory contains specialized AI agents for the Interactive CV project.

## Agent Types

### Academic Workflow
1. **Academic Analyzer** (`academic_analyzer.py`) - Analyzes raw papers → produces structured analyses
2. **Generic Extractor** (`extractor.py`) - Configuration-driven metadata extraction for any document type

### Personal Notes Workflow
- **Generic Extractor** (`extractor.py`) - Direct metadata extraction using blueprint configurations

### Data Quality
- **Entity Deduplicator** (`entity_deduplicator.py`) - Finds and merges duplicate entities

## Academic Analyzer (`academic_analyzer.py`)

Analyzes research papers following the methodology in `How_to_analyze.md`.

**Features:**
- Three-phase analysis structure (Reconnaissance, Deep Dive, Synthesis)
- Domain-specific analysis (mathematics, computer_science, physics)
- Critical examination (assumptions, limitations, evidence quality)
- Generates structured markdown analyses
- Thinking patterns and quality assessment

**Usage:**
```python
from agents import AcademicAnalyzer

# Use the default (flash) model
analyzer_flash = AcademicAnalyzer()
# Or use the pro model
analyzer_pro = AcademicAnalyzer(use_pro_model=True)

# Analyze a paper
analysis = analyzer_flash.analyze_file(Path("paper.md"))

# Save as structured markdown
output_path = analyzer_flash.save_analysis(analysis)
```

**Output:** Creates a comprehensive analysis following the three-phase structure, ready for entity extraction.

## Generic Extractor (`extractor.py`)

Configuration-driven metadata extractor that works with any document type using blueprint configurations.

**Features:**
- Domain-agnostic extraction using YAML blueprints
- Supports both academic and personal document types
- Configurable field mapping and validation
- Uses blueprint-driven schema loading
- Model selection support (Flash/Pro)
- Works on analyses produced by the Academic Analyzer
- Direct extraction from personal notes

**Usage:**
```bash
# Extract academic papers (uses blueprints/academic/ configurations)
python agents/extractor.py academic \
  --input academic/ --output raw_data/academic/extracted_metadata/

# Extract personal notes (uses blueprints/personal/ configurations)  
python agents/extractor.py personal \
  --input personal_notes/ --output raw_data/personal_notes/extracted_metadata/

# Options:
# --model google/gemini-2.5-flash    # LLM model to use
# --pattern "*.md"                   # File pattern to process
```

## Workflow Examples

### Academic Paper Processing
```bash
# Step 1: Analyze the paper
python agents/academic_analyzer.py --input academic/ --output raw_data/academic/generated_analyses/

# Step 2: Extract entities from the analysis using configuration-driven extractor
python agents/extractor.py academic \
  --input raw_data/academic/generated_analyses/ \
  --output raw_data/academic/extracted_metadata/
```

### Personal Notes Processing
```bash
# Direct extraction from notes to JSON using blueprint configurations
python agents/extractor.py personal \
  --input personal_notes/ \
  --output raw_data/personal_notes/extracted_metadata/
```

## Judge Agent (`judge_agent.py`)

Specialized evaluation agent that uses LLM-based assessment to compare agent responses against expected answers for quality assurance and testing.

**Features:**
- **LLM-Based Evaluation**: Uses Gemini Flash 2.5 for intelligent answer comparison
- **Quality Scoring**: Provides numerical scores (0-100) for answer correctness
- **Multiple Quality Levels**: EXCELLENT (90-100), GOOD (70-89), FAIR (50-69), POOR (0-49)
- **Detailed Feedback**: Provides explanations for scores and suggestions for improvement
- **Testing Integration**: Designed for automated testing workflows and evaluation pipelines

**Usage:**
```python
from agents.judge_agent import JudgeAgent, AnswerQuality

# Initialize judge
judge = JudgeAgent()

# Evaluate an answer
result = judge.evaluate_answer(
    question="What is UNOT?",
    expected_answer="Universal Neural Optimal Transport...",
    actual_answer="UNOT is a neural network approach...",
    context="Academic paper about optimal transport"
)

print(f"Score: {result.score}/100")
print(f"Quality: {result.quality}")
print(f"Explanation: {result.explanation}")
```

**Command Line:**
```bash
# Evaluate answers from JSON test results
python agents/judge_agent.py --test-results results.json --output evaluated_results.json
```

## Manuscript Agent (`manuscript_agent.py`)

Deep document analysis agent with specialized tools for reading and analyzing original manuscript files to answer specific questions about research content.

**Features:**
- **Multi-Tool Agent**: Uses LangChain agent framework with specialized tools
- **File Reading Capabilities**: Direct access to original manuscript files
- **Content Search**: Search within specific documents for relevant passages
- **Cross-Reference Analysis**: Find connections between different parts of manuscripts
- **Detailed Extraction**: Extract specific information requested by queries
- **Integration Ready**: Designed to be called by the main interactive agent

**Tools Available:**
- `read_file`: Read complete manuscript files
- `search_file_content`: Search for specific terms within documents
- `list_files`: Discover available manuscript files
- `extract_sections`: Extract specific sections or passages

**Usage:**
```python
from agents.manuscript_agent import ManuscriptAgent

# Initialize agent
agent = ManuscriptAgent()

# Analyze manuscript for specific information
response = agent.analyze_manuscript(
    query="What methodology does the UNOT paper use for training?",
    manuscript_path="raw_data/academic/Transcript_MDs/Universal_Neural_Optimal_Transport.md"
)

print(response)
```

**Integration with Main Agent:**
The manuscript agent is designed to be called by the main interactive agent when detailed document analysis is needed:
```python
# Called automatically by interactive agent's `consult_manuscript` tool
result = consult_manuscript(
    "What are the mathematical foundations of the Wasserstein gradient flow paper?",
    "Wasserstein_gradient_flows_large_deviations"
)
```

## Entity Deduplicator (`entity_deduplicator.py`)

Identifies and merges duplicate entities in the knowledge graph using string matching, embeddings, and LLM verification.

**Features:**
- Multi-level duplicate detection (exact match, fuzzy string, embedding similarity)
- **Transitive clustering**: Groups chains of duplicates (e.g., A→B, B→C means A,B,C are all duplicates)
- **Parallel LLM verification**: Up to 20 workers for faster processing
- **Smart canonical selection**: Chooses best entity from cluster based on:
  - Relationship count (most connected wins)
  - Proper capitalization
  - No kebab-case or underscores
  - Proper spacing after punctuation
  - Length (more complete names)
  - Additional metadata
- LLM verification using Gemini 2.5 Flash
- Context-aware deduplication (knows about Vaios' research)
- Safe merge system with dry-run mode
- Entity-specific similarity thresholds
- Batch processing to minimize API costs
- Comprehensive audit logging
- **Conflict resolution**: Handles duplicate relationships during merge

**Usage:**
```python
from agents import EntityDeduplicator

# Initialize deduplicator
deduplicator = EntityDeduplicator(
    db_path="DB/metadata.db",
    similarity_threshold=0.85
)

# Find duplicates for a specific entity type (dry run)
deduplicator.deduplicate_entity_type('topic', dry_run=True)

# Deduplicate all entity types with backup
deduplicator.deduplicate_all(dry_run=False)
```

**Command Line:**
```bash
# Verify database first
python DB/verify_entities.py

# Generate entity embeddings (required for similarity)
python DB/embeddings.py --entities-only --verify

# Find duplicates (dry run)
python agents/entity_deduplicator.py --dry-run

# Merge duplicates with backup and parallel processing
python agents/entity_deduplicator.py --parallel-workers 20 --merge --backup

# Deduplicate only topics
python agents/entity_deduplicator.py --entity-type topic --merge

# Advanced options
python agents/entity_deduplicator.py --parallel-workers 10 --no-clustering --merge
```

**New Command Line Options:**
- `--parallel-workers N`: Number of parallel LLM workers (default 5, up to 20)
- `--no-clustering`: Disable transitive clustering (not recommended)

**Deduplication Process:**
1. **String Matching**: Finds exact matches (case-insensitive) and fuzzy matches
2. **Embedding Similarity**: Uses cosine similarity on entity embeddings
3. **Transitive Clustering**: Groups all connected duplicates using DFS
4. **LLM Verification**: Confirms duplicates with context about entities (parallel)
5. **Canonical Selection**: Chooses best entity from each cluster
6. **Smart Merging**: Transfers all relationships to canonical entity, handles conflicts

**Thresholds by Entity Type:**
- **People**: 0.9 (names need high similarity)
- **Institutions**: 0.9 (organizations need precision)
- **Topics**: 0.85 (some variation expected)
- **Methods**: 0.85 (technical terms)
- **Projects/Applications**: 0.8 (more flexibility)

**Implementation Details:**
- `find_duplicate_clusters()`: Groups transitively connected duplicates using DFS
- `choose_canonical_entity()`: Scores entities to pick the best one from a cluster
- `verify_duplicates_parallel()`: Parallel LLM verification using ThreadPoolExecutor
- `merge_cluster()`: Merges entire clusters instead of just pairs
- Relationship conflict handling prevents UNIQUE constraint violations

## Analysis Methodology (`How_to_analyze.md`)

Comprehensive methodology document that defines the structured approach for analyzing academic papers used by the Academic Analyzer agent.

**Purpose**: Provides a standardized, three-phase analysis framework that ensures consistent, thorough examination of research papers across different domains.

**Three-Phase Structure:**
1. **Reconnaissance Phase**: Initial paper overview, methodology identification, and context establishment
2. **Deep Dive Phase**: Detailed analysis of mathematical foundations, experimental design, and technical contributions
3. **Synthesis Phase**: Critical evaluation, limitations assessment, and broader impact analysis

**Key Features:**
- **Domain-Adaptive**: Works across mathematics, computer science, physics, and interdisciplinary research
- **Quality Assurance**: Built-in checks for thoroughness and analytical depth
- **Structured Output**: Consistent markdown format suitable for further processing
- **Critical Thinking**: Emphasizes assumptions, limitations, and evidence quality assessment

**Usage by Academic Analyzer:**
The `academic_analyzer.py` agent follows this methodology to produce structured analyses that are then processed by the extraction pipeline. This ensures all academic papers receive consistent, high-quality analysis before metadata extraction.

## Configuration

All agents require:
- `OPENROUTER_API_KEY` in your `.env` file
- Python packages: langchain, openai, pydantic

For entity deduplication also requires:
- `OPENAI_API_KEY` (for embeddings)
- numpy, difflib (for similarity calculations)

## Blueprint Configuration Files

- **Academic**: `blueprints/academic/extraction_schema.yaml` & `blueprints/academic/database_mapping.yaml`
- **Personal**: `blueprints/personal/extraction_schema.yaml` & `blueprints/personal/database_mapping.yaml`
- **Core**: `blueprints/core/database_schema.yaml` & `blueprints/core/visualization.yaml`

## System Evolution History

### Major Refactoring Changes
1. **Renamed Folder**: `data_extractors/` → `agents/` with updated imports
2. **Created Academic Analyzer**: New agent following `How_to_analyze.md` methodology
3. **Unified Extractor**: Single `extractor.py` replacing separate academic/chronicle extractors
4. **Added Model Selection**: Support for `google/gemini-2.5-pro` and `google/gemini-2.5-flash`
5. **Blueprint Architecture**: Configuration-driven system with domain-code separation
6. **Cleaned Up Legacy Code**: Removed redundant extractors and config files

### Workflow Evolution
- **Academic**: Two-step process (Analyzer → Generic Extractor)
- **Personal Notes**: Direct extraction using Generic Extractor with blueprint configurations
- **Configuration-Driven**: All extraction rules in YAML blueprints

## Integration Points

These agents integrate with:
- Metadata database system (see [Database System](../DB/README.md))
- Knowledge graph generation (see [Knowledge Graph](../KG/README.md))
- RAG pipeline for queries
- Sync scripts for automation
- Entity embeddings for deduplication
- Blueprint configuration system

## 📚 Related Documentation

- **[Main Project README](../README.md)**: Overall system architecture and quick start
- **[Database System](../DB/README.md)**: How extracted metadata is stored and processed
- **[Knowledge Graph](../KG/README.md)**: How entities become interactive visualizations
- **[Web UI](../web_ui/README.md)**: How to explore the results interactively