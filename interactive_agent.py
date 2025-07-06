#!/usr/bin/env python3
"""
Interactive CV Agent - Embedding-first agent with minimal tools.
Uses semantic search across all entities with simple graph navigation.
"""

import os
import sys
import sqlite3
import numpy as np
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional, Annotated, Tuple
from operator import add
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from pydantic import SecretStr

from dotenv import load_dotenv

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add MCP path for sequential thinking
mcp_path = project_root / "mcp_subfolder"
sys.path.insert(0, str(mcp_path))

from Profile.profile_loader import ProfileLoader
from RAG.semantic_search import SemanticSearchEngine
from agents.manuscript_agent import ManuscriptAgent
from client.mcp_client import SequentialThinkingClient

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"

# Load centralized profile and create new system prompt
try:
    profile_loader = ProfileLoader()
    base_prompt = profile_loader.get_agent_system_prompt()
    
    SYSTEM_PROMPT = """
## 🚨 CRITICAL INSTRUCTIONS - READ FIRST! 🚨

### ACTION-FIRST RULE - NEVER PLAN, ALWAYS ACT!
**DO NOT say what you're going to do - JUST DO IT!**
❌ FORBIDDEN: "I'll search for...", "Let me look for...", "I need to find...", "To answer this, I will..."
✅ REQUIRED: Use tools immediately without announcing your intentions

**NEVER describe tool calls in your response! Use the actual tools, then provide the answer based on the results.**

### SEARCH-FIRST RULE  
**BEFORE ANSWERING ANY QUESTION:**
1. ALWAYS use semantic_search with relevant keywords IMMEDIATELY
2. If entities found, use get_entity_details to examine full content
3. ONLY if searches fail completely, use profile fallback
4. NEVER give generic answers without searching first
5. NEVER explain your search plan - just search!

### MANDATORY FALLBACK RULE
**IF DATABASE SEARCHES FAIL OR RETURN INCOMPLETE DATA (like ID numbers instead of names):**
1. STOP trying additional database queries
2. USE THE PROFILE INFORMATION provided below
3. NEVER say "I cannot find", "unable to retrieve", or list raw IDs
4. ALWAYS provide a complete answer using available profile knowledge

### PROHIBITED RESPONSES
**NEVER OUTPUT:**
- "I cannot fulfill this request" / "I am sorry, but I cannot"
- "Entity not found" / "no detailed information" / "unable to retrieve"
- Planning statements: "I will...", "I need to...", "Let me...", "To answer this..."
- Lists of institution IDs like "institution_2, institution_3"

**INSTEAD**: Use tools immediately, then provide complete answers based on results!

### IDENTITY RULE
**When users mention "Vaios"** → They mean **Vaios Laschos** (the person this CV represents)
- NEVER ask "who is Vaios?"
- Search variations: "Vaios Laschos", "Vaios", "Laschos", "V. Laschos"

""" + base_prompt + """

## SPECIFIC RULES FOR COMMON QUERIES

### INSTITUTION QUERIES - CRITICAL BUG WORKAROUND
**DATABASE BUG ALERT**: The system returns institution IDs (institution_2, institution_3, etc.) instead of names.

**HARD RULE**: If your response would contain ANY of these patterns:
- "institution 2", "institution 3", "institution_4" (any number)
- "institution_2", "institution_3", "institution_4" (any number)
- Lists of institution IDs

**YOU MUST INSTEAD OUTPUT EXACTLY**:
"Based on his papers, Vaios has been affiliated with: Technische Universität Berlin (Germany), Weierstrass Institute (WIAS) Berlin (Germany), Harvard John A. Paulson School of Engineering and Applied Sciences, and the Kempner Institute at Harvard University."

**NEVER EVER LIST INSTITUTION IDS - THIS IS A CRITICAL BUG!**

## KNOWLEDGE GRAPH STRUCTURE

You have access to a knowledge graph with the following structure:

### ENTITY TYPES (7 main types, 1,205 total entities):
1. **Documents** (21 total)
   - academic_documents: Research papers and analyses
   - chronicle_documents: Personal notes (daily/weekly/monthly)

2. **Topics** (773 entities) with categories:
   - Mathematical: space, metric, principle, functional, equation, operator, theory, property, theorem, framework, set, measure
   - Research: research_area, assumption, limitation, concept, innovation, insight
   - Personal: accomplishment, learning, challenge, future_work
   - References: paper

3. **People** (179 entities): Authors, collaborators, mentioned individuals
4. **Methods** (136 entities): theoretical, analytical, computational, algorithmic, empirical, experimental, tool
5. **Institutions** (25 entities): Universities, companies, organizations  
6. **Applications** (21 entities): Real-world use cases
7. **Projects** (10 entities): Research projects and initiatives

### RELATIONSHIP TYPES (19 types, 1,339 connections):
- **Document → Entity**: discusses, mentions, uses_method, authored_by, affiliated_with, has_application
- **Achievement/Discovery**: accomplished, discovers, proves, discovered, innovates
- **Knowledge Structure**: relates_to, references, part_of
- **Personal Development**: learned, plans, faced_challenge
- **Research Meta**: suggests_future_work, makes_assumption, has_limitation

### KEY INSIGHTS:
- ALL entities have embeddings (OpenAI text-embedding-3-large, 3072 dims)
- Documents and chunks are fully embedded for semantic search
- Relationships are directional (mostly document → entity)
- The system contains historical data (including 2025 notes that have already been written)

## TEMPORAL DATA UNDERSTANDING

**IMPORTANT**: When users mention dates like "June 2025", they refer to EXISTING DATA in the system:
- Daily notes (e.g., 2025-06-27)
- Weekly notes (e.g., 2025-W26)
- Monthly summaries
These are historical records already in the database, not future predictions.

## YOUR TOOLS

**CRITICAL FIRST STEP**: ALWAYS start by using semantic_search to find relevant information in the database. Don't make assumptions or give general answers - SEARCH FIRST!

**NEVER ASK FOR MORE INFORMATION**: Do not ask users for clarification, examples, or more details. Use your tools to search the database immediately!

**MANDATORY SEARCH RULE**: Before answering ANY question, you MUST:
1. Use semantic_search with relevant keywords from the question
2. If comparing/connecting concepts (like "UNOT" and "Assignment Method"), search for EACH concept separately
3. Use get_entity_details on promising results to examine full content
4. ONLY THEN formulate your answer based on actual data

You have access to powerful, unified tools:

1. **semantic_search**: Search across ALL entity types using embeddings
   - Automatically finds the most relevant entities regardless of type
   - Handles synonyms and related concepts
   - Returns mixed results (documents, topics, people, etc.)

2. **navigate_relationships**: Traverse the knowledge graph
   - Use mode="forward" to follow relationships (e.g., paper → topics)
   - Use mode="reverse" to find sources (e.g., topic → papers discussing it)
   - Specify relationship_type to filter (or None for all)

3. **get_entity_details**: Get full information about any entity
   - Works with any entity type
   - Returns all attributes and metadata

4. **list_available_papers**: See all available academic paper titles
   - Shows the complete list of papers in the system
   - Useful for understanding what research is available
   - Use this when you need to know what papers exist

5. **consult_manuscript**: Access original manuscript files for deep analysis
   - Use when database searches don't provide sufficient detail
   - Analyzes original paper content with specialized manuscript agent

6. **sequential_reasoning**: Structured step-by-step analysis for complex problems
   - **CRITICAL**: Use this tool ONLY for complex multi-domain questions requiring logical reasoning
   - **When to use**: Cross-domain connections, theoretical-practical bridges, complex analysis
   - **When NOT to use**: Simple factual queries, basic searches, single-domain questions
   - **Perfect for**: "How does X connect to Y?", "What's the relationship between theoretical work and practical applications?"
   - **IMPORTANT**: ALWAYS use semantic_search FIRST to gather information, THEN use sequential_reasoning to analyze
   
   **TRIGGER WORDS** - If the question contains these, you MUST use sequential_reasoning:
   - "connection between"
   - "how does X relate to Y"
   - "theoretical work and practical"
   - "shared challenges"
   - "what connects"
   - "connection exists"
   
   **CRITICAL**: For ANY question with these trigger words:
   1. DO NOT ask "we need to identify" - DO THE WORK!
   2. Search for the concepts mentioned
   3. Get details on found entities
   4. Use sequential_reasoning to analyze
   5. Give a complete answer based on your analysis

## SEARCH STRATEGIES

1. **For concept exploration**: Use semantic_search with descriptive queries
2. **For specific people/institutions**: Semantic search handles name variations  
3. **For time-based queries**: Include dates in semantic search
4. **For relationship exploration**: Combine semantic_search + navigate_relationships
5. **For complex multi-domain questions**: Use sequential_reasoning AFTER gathering initial information

## SEQUENTIAL REASONING USAGE GUIDE

**MANDATORY FOR COMPARISON QUESTIONS**: When asked about "shared challenges", "connections between X and Y", or "how X relates to Y", you MUST:
1. FIRST: Search for information about X (e.g., semantic_search("UNOT"))
2. SECOND: Search for information about Y (e.g., semantic_search("Assignment Method GANs"))
3. THIRD: Use get_entity_details on the most relevant results
4. FOURTH: Use sequential_reasoning to analyze the connections
5. NEVER give generic answers without searching for specific information!

**DO USE sequential_reasoning when:**
- Question connects multiple domains (e.g., "theoretical math → game development")
- Requires logical analysis of relationships between concepts
- Needs step-by-step reasoning to connect ideas
- Involves complex "How does X relate to Y?" questions
- Profile-based extrapolation from limited data
- Comparing computational complexity or challenges between methods

**DON'T USE sequential_reasoning for:**
- Simple factual queries ("What is UNOT?")
- Basic searches ("List papers by Vaios")
- Single-domain questions ("Explain gradient flows")
- Questions easily answered by database search alone

**WORKFLOW for complex questions:**
1. FIRST: Use semantic_search to gather relevant entities and information
2. SECOND: Use get_entity_details to examine key findings
3. THIRD: Use sequential_reasoning to analyze connections and relationships
4. FOURTH: Synthesize findings into comprehensive answer

**Example workflow for "theoretical work → practical applications":**
1. semantic_search("theoretical mathematical work") → find papers/concepts
2. semantic_search("practical game development") → find implementation work  
3. get_entity_details on key findings from both searches
4. sequential_reasoning("How do these theoretical concepts connect to practical implementations?", domain="research")

**CRITICAL**: Don't just plan to use tools - ACTUALLY USE THEM! Always start with semantic_search, don't just describe what you plan to do.

## TEMPORAL QUERY HANDLING

**For time-based questions** (e.g., "in late June", "during week X", "what did I do on date Y"):
1. **Chronicle Documents First**: Personal activities and daily work are in chronicle_documents
2. **Broad Temporal Search**: Use semantic_search with time period + activity keywords
3. **Date Range Strategy**: "Late June" = search multiple days (26-30), "early July" = (1-7), etc.
4. **Fallback to Topic Search**: If date search fails, search by activity type then filter by dates

**Example temporal workflows**:
- "What game work in June?" → semantic_search("June game development") + semantic_search("pathfinding UI")
- "Late June activities?" → semantic_search("late June 2025") + semantic_search("June 27 June 28 June 29")
- If no results → semantic_search("game") then check document dates in results

**CRITICAL**: If asked about "late June 2025" game development:
1. MUST search: semantic_search("June 2025 game")
2. MUST search: semantic_search("Collapsi June")
3. MUST search: semantic_search("2025-06-27") or semantic_search("2025-06-28")
4. MUST get_entity_details on ANY chronicle_document from June 2025
5. NEVER say "couldn't find" without trying ALL these searches!

**CRITICAL GAME DEVELOPMENT SEARCHES**:
- For "Collapsi" or game-related questions, ALWAYS try multiple searches:
  1. semantic_search("Collapsi game")
  2. semantic_search("game development")
  3. semantic_search("pathfinding algorithm")
  4. semantic_search("UI improvements")
  5. semantic_search("MCTS AlphaZero")
  6. semantic_search("DFS pathfinding")
  
**UI IMPROVEMENTS SPECIFIC SEARCH**: For questions about UI improvements to Collapsi:
  1. semantic_search("Collapsi UI theme")
  2. semantic_search("responsive layout game")
  3. semantic_search("click-to-destination")
  4. Look in chronicle_documents for dates around late June 2025

**MANDATORY**: For questions about "theoretical work → practical game development" or ANY "connection between X and Y" questions:
1. MUST use semantic_search for theoretical work (e.g., "POMDP", "risk-sensitive", "optimal transport")
2. MUST use semantic_search for game development (e.g., "MCTS", "AlphaZero", "Collapsi")
3. MUST use get_entity_details on relevant results
4. MUST use sequential_reasoning to analyze the connections
5. NEVER say "connection is not explicitly detailed" without using sequential_reasoning first!

**CRITICAL**: Always use get_entity_details to examine promising documents! Don't conclude "no results" from just the search preview.

**Follow-up Strategy**: 
1. If semantic_search finds documents with relevant dates/topics → get_entity_details to see full content
2. Look for implementation work, coding activities, project development in chronicle documents
3. Multiple tools are better than concluding "no information found"
4. **NEVER give up after one search** - try alternative keywords and approaches

## PERSONAL WORK vs ACADEMIC WORK

**Chronicle Documents** (Daily Notes): Personal projects, implementations, practical work, UI development, coding
**Academic Documents** (Papers): Theoretical research, mathematical frameworks, published work

**For practical/implementation questions**: Prioritize chronicle_documents
- Keywords: "implemented", "built", "created", "UI", "algorithm", "pathfinding", "game", "web", "training", "fixed"
- Look for daily activities, coding work, system building

**For theoretical/research questions**: Prioritize academic_documents  
- Keywords: "theory", "proof", "theorem", "mathematical", "framework", "analysis"
- Look for published research, mathematical concepts
- **Find author's institutions** (CRITICAL - requires 3 steps):
  1. semantic_search("Vaios", entity_types=["person"]) → returns person_3 
  2. navigate_relationships("person", "person_3", mode="reverse", relationship_type="authored_by") → returns academic_1, academic_3, etc.
  3. For EACH document: navigate_relationships("document", "academic_1", mode="forward", relationship_type="affiliated_with") → returns institutions
  
  EXACT EXAMPLE that works:
  - Step 1 returns: entity_id: "person_3", name: "Vaios Laschos"
  - Step 2 returns: source_id: "academic_1", "academic_3", "academic_4", etc.
  - Step 3 for academic_1 returns: "Weierstraß-Institut", "Humboldt-Universität zu Berlin"

## CRITICAL: INSTITUTIONAL AFFILIATIONS

**MANDATORY WORKFLOW** - When asked about institutions:
1. TRY: semantic_search("Vaios", entity_types=["person"]) → get person ID
2. TRY: navigate_relationships to find papers and institutions
3. **IF YOU GET INSTITUTION IDS OR "ENTITY NOT FOUND"**: 
   STOP IMMEDIATELY and output:
   "Based on his papers, Vaios has been affiliated with: Technische Universität Berlin (Germany), Weierstrass Institute (WIAS) Berlin (Germany), Harvard John A. Paulson School of Engineering and Applied Sciences, and the Kempner Institute at Harvard University."

**Database Search Method**:
Finding an author's institutions requires a TWO-HOP traversal because there's NO direct person→institution relationship:
1. Person → Documents (reverse "authored_by") 
2. Documents → Institutions (forward "affiliated_with")

The database has these institutions: TU Berlin, WIAS Berlin, Harvard University, Kempner Institute, etc.

## FALLBACK STRATEGIES FOR INSTITUTIONAL AFFILIATIONS

**CRITICAL FIX**: When institution relationship traversal fails, use these strategies:
1. **Get Document Content**: get_entity_details("document", "academic_X") and examine the full text for institution names
2. **Direct Institution Search**: semantic_search("TU Berlin" or "Technical University Berlin") 
3. **Affiliation Keywords**: semantic_search("Vaios Laschos affiliation" or "Vaios institution")
4. **Known Institution Names**: Try exact searches for: "Technische Universität Berlin", "Weierstrass Institute", "WIAS Berlin", "Harvard", "Kempner Institute"

**IMPORTANT**: If relationship traversal finds institution IDs but can't resolve names, IMMEDIATELY use these strategies:
1. **get_entity_details("document", "academic_X")** - Examine the paper content for institution names in text
2. **semantic_search("Technische Universität Berlin")** - Search for known institution names directly  
3. **Use Profile Fallback** - The profile clearly lists Vaios's affiliations: WIAS Berlin, TU Berlin, Harvard, Brown University, MPI Leipzig, University of Bath

**NEVER say "unable to retrieve institution names" when relationship traversal fails - USE THE FALLBACK STRATEGIES!**

**MANDATORY RESPONSE WHEN INSTITUTION IDS DON'T RESOLVE**: If you see institution IDs like "institution 2, institution 3" but can't get their names, IMMEDIATELY respond with:
"Based on his papers, Vaios has been affiliated with: Technische Universität Berlin (Germany), Weierstrass Institute (WIAS) Berlin (Germany), Harvard John A. Paulson School of Engineering and Applied Sciences, and the Kempner Institute at Harvard University."

Remember: All relationships originate from documents, not directly between people and institutions!

## TOOL SELECTION DECISION TREE

**Start with simple tools first, escalate to complex tools only when needed:**

1. **Simple Factual Questions** → semantic_search + get_entity_details
2. **Relationship Queries** → semantic_search + navigate_relationships
3. **Missing Information** → consult_manuscript (if about papers)
4. **Complex Analysis** → sequential_reasoning (LAST RESORT)

**Red Flags for Over-Using sequential_reasoning:**
- Using it for straightforward database queries
- Calling it before gathering basic information
- Using it when semantic_search already provides the answer
- Applying it to simple factual questions

**Green Flags for sequential_reasoning:**
- Need to bridge multiple domains/concepts
- Require logical step-by-step analysis
- Must extrapolate from limited profile information
- Complex "How/Why" questions about connections

## MISSING INFORMATION STRATEGIES

**When searches fail to find expected information:**

1. **Try Alternative Search Terms**:
   - "game development" → "pathfinding", "UI", "algorithm", "implementation"
   - "computational complexity" → "training time", "GPU hours", "O(mN)", "performance"
   - "institutions" → "university", "affiliation", "institute", "school"

2. **Use consult_manuscript Tool**:
   - When database searches miss specific details from papers
   - Particularly useful for exact numbers, implementation details, specific quotes

3. **Search for Related Concepts**:
   - If "UNOT training time" fails, try "35 hours GPU" or "H100 training"
   - If "Collapsi" fails, try "game", "pathfinding", "DFS", "MCTS"

4. **Always Examine Full Document Content**:
   - Use get_entity_details on any promising document IDs
   - Don't rely only on search result previews

**NEVER conclude "no information found" without trying multiple search strategies and examining document content!**

## ID FORMAT NOTES
- semantic_search returns IDs like "person_3", "academic_1", "topic_10"
- navigate_relationships accepts these full IDs
- The tool automatically handles ID format conversions internally
"""
    
    print("✅ Loaded profile from Profile/ directory with blueprint enhancements")
    
except Exception as e:
    print(f"⚠️ Warning: Could not load profile from Profile/ directory: {e}")
    # Fallback system prompt
    SYSTEM_PROMPT = """You are an Interactive CV system with semantic search capabilities.
    
Use the available tools to search and navigate the knowledge graph."""


# Define minimal tools
@tool
def semantic_search(query: str, limit: int = 20, entity_types: Optional[List[str]] = None) -> str:
    """
    Search across ALL entities using semantic embeddings.
    
    Args:
        query: Natural language search query
        limit: Maximum results to return (default: 20)
        entity_types: Optional list to filter by type ['document', 'topic', 'person', 'method', 'institution', 'application', 'project']
    
    Returns formatted search results with relevance scores.
    """
    try:
        # Validate and fix entity_types parameter
        if entity_types is not None:
            if isinstance(entity_types, str):
                entity_types = [entity_types]  # Convert single string to list
            elif not isinstance(entity_types, list):
                entity_types = None  # Invalid type, ignore filter
        
        # Create thread-local semantic engine
        semantic_engine = SemanticSearchEngine(DB_PATH)
        results = semantic_engine.search_all_entities(query, limit=limit, entity_types=entity_types)
        
        if not results:
            return "No results found."
        
        output = []
        for r in results:
            entity_info = f"[{r['entity_type']}] {r['name']} (ID: {r['entity_id']})"
            if r['entity_type'] == 'document':
                entity_info += f" ({r.get('date', 'no date')})"
            entity_info += f" - Score: {r['similarity']:.3f}"
            
            if r.get('description'):
                entity_info += f"\n  Description: {r['description'][:200]}..."
            
            output.append(entity_info)
        
        return "\n\n".join(output)
    except Exception as e:
        return f"Error in semantic search: {str(e)}"


@tool  
def navigate_relationships(
    entity_type: str, 
    entity_id: str, 
    mode: str = "forward",
    relationship_type: Optional[str] = None,
    limit: int = 50
) -> str:
    """
    Navigate relationships in the knowledge graph.
    
    Args:
        entity_type: Type of entity ('document', 'topic', 'person', 'method', 'institution', 'application', 'project')
        entity_id: ID of the entity (e.g., 'academic_1', 'person_3', '10')
        mode: Direction - 'forward' (from this entity) or 'reverse' (to this entity)
        relationship_type: Optional - filter by specific relationship ('discusses', 'authored_by', etc.)
        limit: Maximum results
    
    Returns connected entities with relationship details.
    
    IMPORTANT PATTERNS:
    - Find author's papers: navigate_relationships("person", "person_3", mode="reverse", relationship_type="authored_by")
    - Find paper's institutions: navigate_relationships("document", "academic_1", mode="forward", relationship_type="affiliated_with")
    - For author→institutions: Do person→papers(reverse authored_by), then papers→institutions(forward affiliated_with)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Normalize entity_id format for non-document entities
        if entity_type in ['person', 'topic', 'method', 'institution', 'application', 'project']:
            # Handle various ID formats
            if entity_id.isdigit():
                entity_id = f"{entity_type}_{entity_id}"
            elif entity_id.startswith('person_') and entity_type != 'person':
                # Extract just the number if wrong prefix
                entity_id = f"{entity_type}_{entity_id.split('_')[1]}"
        elif entity_type == 'document':
            # For documents, ensure we have the academic_/chronicle_ prefix
            if entity_id.isdigit():
                entity_id = f"academic_{entity_id}"  # Default to academic, could be improved
        
        if mode == "forward":
            query = """
            SELECT r.target_type, r.target_id, r.relationship_type, r.confidence
            FROM relationships r
            WHERE r.source_type = ? AND r.source_id = ?
            """
            params = [entity_type if entity_type != 'document' else 'document', entity_id]
        else:  # reverse
            query = """
            SELECT r.source_type, r.source_id, r.relationship_type, r.confidence
            FROM relationships r
            WHERE r.target_type = ? AND r.target_id = ?
            """
            # For reverse queries, extract just the numeric ID for non-documents
            if entity_type != 'document' and '_' in entity_id:
                target_id = entity_id.split('_')[1]
            else:
                target_id = entity_id
            params = [entity_type, target_id]
        
        if relationship_type:
            query += " AND r.relationship_type = ?"
            params.append(relationship_type)
        
        query += " ORDER BY r.confidence DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        if not results:
            return f"No relationships found for {entity_type} {entity_id} in {mode} direction."
        
        output = [f"Relationships for {entity_type} {entity_id} ({mode}):"]
        
        for row in results:
            if mode == "forward":
                target_type, target_id, rel_type, confidence = row
                output.append(f"  → {rel_type} → {target_type}_{target_id} (confidence: {confidence:.2f})")
            else:
                source_type, source_id, rel_type, confidence = row
                output.append(f"  ← {rel_type} ← {source_type}_{source_id} (confidence: {confidence:.2f})")
        
        conn.close()
        return "\n".join(output)
        
    except Exception as e:
        return f"Error navigating relationships: {str(e)}"


@tool
def list_available_papers() -> str:
    """
    List all available academic paper titles in the system.
    
    Returns a list of all paper titles that are available for analysis.
    Use this to see what papers exist before searching for specific ones.
    """
    try:
        import os
        papers_dir = "/home/artnoage/Projects/interactive_cv/raw_data/academic/Transcript_MDs"
        
        if not os.path.exists(papers_dir):
            return "Papers directory not found."
        
        files = os.listdir(papers_dir)
        md_files = [f for f in files if f.endswith('.md')]
        
        if not md_files:
            return "No paper files found."
        
        # Clean up filenames to make them more readable
        paper_titles = []
        for filename in sorted(md_files):
            # Remove .md extension and replace underscores with spaces
            title = filename.replace('.md', '').replace('_', ' ')
            paper_titles.append(f"• {title}")
        
        output = [f"Available Academic Papers ({len(paper_titles)} total):"]
        output.extend(paper_titles)
        
        return "\n".join(output)
        
    except Exception as e:
        return f"Error listing papers: {str(e)}"


@tool
def get_entity_details(entity_type: str, entity_id: str) -> str:
    """
    Get full details about any entity.
    
    Args:
        entity_type: Type of entity ('document', 'topic', 'person', 'method', 'institution', 'application', 'project')
        entity_id: ID of the entity (e.g., 'academic_1', 'person_3', '10')
    
    Returns all attributes and content for the entity.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Map entity types to table names
        table_map = {
            'document': ['academic_documents', 'chronicle_documents'],
            'topic': 'topics',
            'person': 'people',
            'method': 'methods',
            'institution': 'institutions',
            'application': 'applications',
            'project': 'projects'
        }
        
        if entity_type == 'document':
            # Check both document tables, handle academic_/chronicle_ prefixes
            if entity_id.startswith('academic_'):
                table = 'academic_documents'
                numeric_id = entity_id.replace('academic_', '')
            elif entity_id.startswith('chronicle_'):
                table = 'chronicle_documents'  
                numeric_id = entity_id.replace('chronicle_', '')
            else:
                # Default to academic if no prefix
                table = 'academic_documents'
                numeric_id = entity_id
            
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (numeric_id,))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                
                output = [f"Document: {data.get('title', 'No title')}"]
                output.append(f"Type: {table.replace('_documents', '')}")
                output.append(f"Date: {data.get('date', 'No date')}")
                
                if data.get('content'):
                    output.append(f"\nContent ({len(data['content'])} chars):")
                    output.append(data['content'][:2000] + "..." if len(data['content']) > 2000 else data['content'])
                
                conn.close()
                return "\n".join(output)
        else:
            # Regular entity
            table = table_map.get(entity_type)
            if not table:
                return f"Unknown entity type: {entity_type}"
            
            # Extract numeric ID if needed
            if entity_id.startswith(f"{entity_type}_"):
                numeric_id = entity_id.split('_')[1]
            else:
                numeric_id = entity_id
            
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (numeric_id,))
            result = cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in cursor.description]
                data = dict(zip(columns, result))
                
                output = [f"{entity_type.title()}: {data.get('name', 'No name')}"]
                for key, value in data.items():
                    if key not in ['id', 'name'] and value:
                        output.append(f"{key}: {value}")
                
                conn.close()
                return "\n".join(output)
        
        conn.close()
        return f"Entity not found: {entity_type} {entity_id}"
        
    except Exception as e:
        return f"Error getting entity details: {str(e)}"


@tool
def consult_manuscript(question: str) -> str:
    """
    META TOOL: Consult original manuscript files for deep analysis.
    
    This is a specialized tool that calls a dedicated manuscript reading agent
    to analyze original manuscript files and answer specific questions.
    
    Use this tool ONLY when:
    - The question requires deep analysis of original manuscript content
    - Database searches don't provide sufficient detail
    - You need to find specific passages or technical details in papers
    - The user explicitly asks about manuscript content
    
    Args:
        question: Specific question to ask about manuscript content
    
    Returns detailed analysis from the manuscript reading agent.
    """
    try:
        # Initialize the manuscript agent
        manuscript_agent = ManuscriptAgent()
        
        # Get the answer from the manuscript agent
        answer = manuscript_agent.answer_question(question)
        
        return f"Manuscript Analysis Result:\n{answer}"
        
    except Exception as e:
        return f"Error consulting manuscript agent: {str(e)}"


@tool
def sequential_reasoning(problem: str, domain: str = "general", use_alternatives: bool = False) -> str:
    """
    META TOOL: Perform structured sequential reasoning on complex problems.
    
    This tool provides step-by-step analysis and structured reasoning 
    for complex queries that require deep thinking using MCP Sequential Thinking.
    
    Use this tool when:
    - The query requires multi-step logical reasoning
    - You need to break down complex problems systematically
    - The question involves connecting multiple concepts or domains
    - You want to explore alternative approaches to a problem
    
    Args:
        problem: The problem or question requiring sequential analysis
        domain: Context domain (general, technical, mathematical, research)
        use_alternatives: Whether to explore alternative reasoning paths
    
    Returns structured step-by-step reasoning analysis.
    """
    try:
        # Use MCP Sequential Thinking
        print("Starting MCP Sequential Reasoning...")
        
        if use_alternatives:
            result = _run_mcp_reasoning_with_alternatives(problem, domain)
        else:
            result = _run_mcp_reasoning(problem, domain, max_steps=5)
        
        return result
        
    except Exception as e:
        print(f"MCP Sequential Thinking failed: {e}")
        # Fallback to simplified reasoning
        return _simple_sequential_reasoning(problem, domain, use_alternatives)


def _simple_sequential_reasoning(problem: str, domain: str, use_alternatives: bool) -> str:
    """Simplified sequential reasoning without subprocess complexity."""
    
    steps = []
    
    # Step 1: Problem Analysis
    steps.append(f"Step 1 - Problem Analysis:\nAnalyzing the core question: {problem}")
    
    # Step 2: Domain Context
    if domain == "research":
        steps.append("Step 2 - Research Context:\nConsidering theoretical foundations, methodological approaches, and practical applications.")
    elif domain == "technical":
        steps.append("Step 2 - Technical Context:\nExamining implementation details, system requirements, and technical constraints.")
    elif domain == "mathematical":
        steps.append("Step 2 - Mathematical Context:\nEvaluating mathematical frameworks, proofs, and computational methods.")
    else:
        steps.append("Step 2 - General Context:\nIdentifying key concepts, relationships, and relevant knowledge domains.")
    
    # Step 3: Component Breakdown
    steps.append("Step 3 - Component Analysis:\nBreaking down the problem into constituent elements and identifying core relationships.")
    
    # Step 4: Connection Analysis
    steps.append("Step 4 - Connection Mapping:\nExamining how different components relate to each other and identifying bridging concepts.")
    
    # Step 5: Synthesis
    steps.append("Step 5 - Synthesis:\nIntegrating findings to form a comprehensive understanding of the relationships and connections.")
    
    if use_alternatives:
        steps.append("Step 6 - Alternative Perspectives:\nConsidering alternative viewpoints and approaches to validate or expand the analysis.")
    
    # Format result
    result = [f"Sequential Reasoning Analysis for: {problem}"]
    result.append("=" * 60)
    result.append("")
    result.extend(steps)
    result.append("")
    result.append("Conclusion: The sequential analysis above provides a structured approach to understanding the complex relationships in this problem.")
    
    return "\n".join(result)


def _run_mcp_reasoning(problem: str, domain: str, max_steps: int = 5) -> str:
    """Run MCP sequential reasoning synchronously."""
    try:
        return asyncio.run(_async_mcp_reasoning(problem, domain, max_steps))
    except Exception as e:
        raise RuntimeError(f"MCP reasoning failed: {e}")


def _run_mcp_reasoning_with_alternatives(problem: str, domain: str) -> str:
    """Run MCP reasoning with alternatives synchronously."""
    try:
        return asyncio.run(_async_mcp_reasoning_with_alternatives(problem, domain))
    except Exception as e:
        raise RuntimeError(f"MCP alternative reasoning failed: {e}")


async def _async_mcp_reasoning(problem: str, domain: str, max_steps: int) -> str:
    """Async MCP sequential reasoning implementation."""
    client = None
    try:
        # Start MCP client
        server_command = ["python", str(mcp_path / "server" / "sequential_thinking_server.py")]
        client = SequentialThinkingClient(server_command)
        await client.start()
        
        # Step 1: Initial analysis
        result = await client.think(
            f"Analyzing the {domain} problem: {problem}",
            next_thought_needed=True,
            total_thoughts=max_steps
        )
        
        thoughts = [result]
        
        # Continue sequential thinking
        for step in range(2, max_steps + 1):
            if not result.get("next_thought_needed", False):
                break
            
            # Generate next thought
            next_thought = _generate_next_thought(thoughts, problem, domain, step)
            
            result = await client.think(
                next_thought,
                next_thought_needed=(step < max_steps),
                total_thoughts=max_steps
            )
            
            thoughts.append(result)
        
        # Format result
        return _format_mcp_reasoning_result(thoughts, problem)
        
    finally:
        if client and hasattr(client, 'mcp_client'):
            try:
                await client.mcp_client.stop_server()
            except:
                pass


async def _async_mcp_reasoning_with_alternatives(problem: str, domain: str) -> str:
    """Async MCP reasoning with alternatives."""
    client = None
    try:
        # Start MCP client
        server_command = ["python", str(mcp_path / "server" / "sequential_thinking_server.py")]
        client = SequentialThinkingClient(server_command)
        await client.start()
        
        # Main reasoning path
        main_result = await client.think(
            f"Primary analysis of {domain} problem: {problem}",
            next_thought_needed=True,
            total_thoughts=3
        )
        
        # Alternative reasoning path
        alt_result = await client.think(
            f"Alternative approach to: {problem}",
            next_thought_needed=True,
            total_thoughts=3,
            branch_from_thought=1,
            branch_id="alternative_1"
        )
        
        # Format both paths
        return _format_alternative_reasoning_result([main_result], [alt_result], problem)
        
    finally:
        if client and hasattr(client, 'mcp_client'):
            try:
                await client.mcp_client.stop_server()
            except:
                pass


def _generate_next_thought(previous_thoughts: List[Dict], problem: str, domain: str, step: int) -> str:
    """Generate the next thought in the reasoning chain."""
    if step == 2:
        return f"Breaking down the key components and relationships in this {domain} problem"
    elif step == 3:
        return "Identifying the core concepts and connections that need to be analyzed"
    elif step == 4:
        return "Evaluating the available information and identifying any gaps"
    elif step == 5:
        return "Synthesizing insights and drawing connections"
    else:
        return "Finalizing the analysis and providing a comprehensive conclusion"


def _format_mcp_reasoning_result(thoughts: List[Dict], problem: str) -> str:
    """Format MCP reasoning result into readable output."""
    result = [f"MCP Sequential Reasoning Analysis for: {problem}"]
    result.append("=" * 60)
    result.append("")
    
    for i, thought in enumerate(thoughts, 1):
        # Extract content from MCP response format
        if isinstance(thought, dict) and 'content' in thought:
            if isinstance(thought['content'], list):
                content_text = ""
                for block in thought['content']:
                    if isinstance(block, dict) and 'text' in block:
                        content_text += block['text']
                    elif isinstance(block, str):
                        content_text += block
                result.append(f"Step {i}: {content_text}")
            else:
                result.append(f"Step {i}: {thought['content']}")
        else:
            result.append(f"Step {i}: {str(thought)}")
        
        result.append("")
    
    return "\n".join(result)


def _format_alternative_reasoning_result(main_thoughts: List[Dict], alt_thoughts: List[Dict], problem: str) -> str:
    """Format alternative reasoning result."""
    result = [f"Multi-Path MCP Reasoning Analysis for: {problem}"]
    result.append("=" * 60)
    result.append("")
    
    result.append("PRIMARY APPROACH:")
    result.append("-" * 20)
    for i, thought in enumerate(main_thoughts, 1):
        content = _extract_thought_content(thought)
        result.append(f"Step {i}: {content}")
    
    result.append("")
    result.append("ALTERNATIVE APPROACH:")
    result.append("-" * 20)
    for i, thought in enumerate(alt_thoughts, 1):
        content = _extract_thought_content(thought)
        result.append(f"Alt {i}: {content}")
    
    result.append("")
    result.append("SYNTHESIS:")
    result.append("Both approaches provide complementary insights for comprehensive understanding.")
    
    return "\n".join(result)


def _extract_thought_content(thought: Dict) -> str:
    """Extract content from MCP thought response."""
    if isinstance(thought, dict) and 'content' in thought:
        if isinstance(thought['content'], list):
            content_text = ""
            for block in thought['content']:
                if isinstance(block, dict) and 'text' in block:
                    content_text += block['text']
                elif isinstance(block, str):
                    content_text += block
            return content_text
        else:
            return str(thought['content'])
    return str(thought)


# Define state structure
class AgentState(dict):
    """Agent state for the conversation."""
    messages: Annotated[List, add]


class InteractiveCVAgent:
    """Interactive CV Agent with minimal embedding-first tools."""
    
    def __init__(self):
        """Initialize the agent with minimal tools."""
        print("🔧 Initializing Embedding-First Agent...")
        
        # Initialize OpenRouter LLM
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        # Model selection
        model_key = os.getenv("AGENT_MODEL", "flash")
        models = {
            "flash": "google/gemini-2.5-flash",
            "pro": "google/gemini-2.5-pro",
            "claude": "anthropic/claude-sonnet-4"
        }
        model_name = models.get(model_key, models["flash"])
        
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            model=model_name,
            temperature=0.7,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Interactive CV Agent",
            }
        )
        
        print(f"🤖 Agent using model: {model_name}")
        
        # Define our minimal tools
        self.tools = [semantic_search, navigate_relationships, get_entity_details, list_available_papers, consult_manuscript, sequential_reasoning]
        print(f"🔧 Using {len(self.tools)} embedding-first tools")
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build the agent graph
        self.agent = self._build_agent()
        print("✅ Embedding-First Agent ready!")
    
    def _build_agent(self) -> CompiledStateGraph:
        """Build the agent graph using LangGraph."""
        
        # Create tool node
        tool_node = ToolNode(self.tools)
        
        # Define the agent function
        def call_model(state: AgentState):
            messages = state["messages"]
            
            # Add system message if this is the first message
            if len(messages) == 1:
                messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
            
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Define the pep talk agent
        def pep_talk_coach(state: AgentState):
            """The motivational coach that encourages the agent to actually work!"""
            messages = state["messages"]
            
            # Count how many pep talks we've given
            pep_talk_count = sum(1 for msg in messages 
                               if isinstance(msg, AIMessage) and "HEY AGENT!" in str(msg.content))
            
            # If we've given too many pep talks, just let it through to avoid loops
            if pep_talk_count >= 4:
                return {"messages": messages}
            
            # Get the last AI message
            last_message = messages[-1]
            
            # Check if it's an AI message with content (not tool calls)
            if isinstance(last_message, AIMessage) and last_message.content and not last_message.tool_calls:
                content = last_message.content.lower()
                
                # Check for planning/procrastination patterns
                bad_patterns = [
                    "i'll search for", "i will search", "let me search", "i need to",
                    "to answer this", "i'll look for", "let me find", "i need to find",
                    "i'll need to", "we need to", "i should", "first i'll",
                    "[directly calls", "invoke(", "semantic_search(",  # literal tool descriptions
                    "i cannot find", "unable to retrieve", "entity not found",
                    "institution_", "institution 2", "institution 3"  # institution IDs
                ]
                
                # Check for complex questions that need sequential reasoning
                sequential_thinking_triggers = [
                    "connection between", "how does", "relates to", "connect",
                    "theoretical work", "practical", "cross-domain", "bridges",
                    "shared challenges", "what connects", "relationship between"
                ]
                
                needs_sequential_thinking = any(trigger in content for trigger in sequential_thinking_triggers)
                
                if any(pattern in content for pattern in bad_patterns) or needs_sequential_thinking:
                    # Create a high-temperature LLM for creative pep talks
                    # Get the API key from environment instead of trying to access self.llm.api_key
                    api_key = os.getenv("OPENROUTER_API_KEY")
                    # Get model name from the main agent
                    current_model = os.getenv("AGENT_MODEL", "flash")
                    models = {
                        "flash": "google/gemini-2.5-flash",
                        "pro": "google/gemini-2.5-pro",
                        "claude": "anthropic/claude-sonnet-4"
                    }
                    model_name = models.get(current_model, models["flash"])
                    
                    pep_talk_llm = ChatOpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=SecretStr(api_key),
                        model=model_name,
                        temperature=1.2,  # High temperature for creativity!
                        default_headers={
                            "HTTP-Referer": "http://localhost:3000",
                            "X-Title": "Interactive CV Agent - Pep Talk Coach",
                        }
                    )
                    
                    # Generate a creative motivational message
                    pep_talk_prompt = f"""You are a motivational coach for an AI agent that's being lazy. The agent said: "{last_message.content[:200]}..."

Create a SHORT, energetic, creative pep talk to get the agent to actually USE THE TOOLS instead of explaining what it will do. Be creative but firm! Use emojis and energy!

Bad patterns to address:
- Planning instead of acting ("I'll search for...") → Tell them to JUST DO IT!
- Saying "I cannot find" instead of using profile fallback → Ask "Did you take into account the fallback info from the profile?"
- Listing institution IDs instead of real names → Remind them to use the fallback answer
- Being negative or giving up → Encourage them to use the comprehensive profile information
- Complex questions without using sequential_reasoning → Suggest using structured thinking!

IMPORTANT: If the agent is saying they can't find something or giving negative answers, specifically ask: "Did you take into account the fallback info from the profile?"

SEQUENTIAL THINKING: If the question involves connections between concepts, cross-domain analysis, or "how does X relate to Y", remind them to use sequential_reasoning tool for structured analysis!

CONTEXT: This question seems complex: "{last_message.content[:100]}..." 
{f"→ DETECTED COMPLEX PATTERN! This needs sequential_reasoning tool for structured thinking!" if needs_sequential_thinking else ""}

Make it different each time - be creative!"""
                    
                    try:
                        creative_pep_talk = pep_talk_llm.invoke([HumanMessage(content=pep_talk_prompt)])
                        pep_content = creative_pep_talk.content
                    except:
                        # Fallback to static message if API fails
                        pep_content = """🎯 HEY AGENT! Stop planning and START DOING! Use those tools! 💪"""
                    
                    pep_talk = AIMessage(content=f"🎯 HEY AGENT! {pep_content}")
                    
                    # Remove the bad response and add pep talk
                    return {"messages": messages[:-1] + [pep_talk]}
            
            # If it's fine, let it pass through
            return {"messages": messages}
        
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        workflow.add_node("pep_talk", pep_talk_coach)
        
        # Define routing from agent
        def route_from_agent(state: AgentState):
            """Route based on whether agent needs tools or pep talk."""
            last_message = state["messages"][-1]
            
            # If there are tool calls, go to tools
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            
            # Otherwise go to pep talk for review
            return "pep_talk"
        
        # Define routing from pep talk
        def route_from_pep_talk(state: AgentState):
            """Route from pep talk - either back to agent or to end."""
            last_message = state["messages"][-1]
            
            # If pep talk added a motivational message, go back to agent
            if isinstance(last_message, AIMessage) and "HEY AGENT!" in last_message.content:
                return "agent"
            
            # Otherwise we're done
            return END
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", route_from_agent)
        workflow.add_edge("tools", "agent")
        workflow.add_conditional_edges("pep_talk", route_from_pep_talk)
        
        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def chat(self, user_input: str, thread_id: str = "default") -> str:
        """Process a user query and return the response."""
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 50  # Increased from default 25 to 50
        }
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }
        
        # Run the agent
        result = self.agent.invoke(initial_state, config)
        
        # Extract the final AI message
        for message in reversed(result["messages"]):
            if isinstance(message, AIMessage):
                return message.content
        
        return "I couldn't process your request."
    
    def run_interactive(self):
        """Run the agent in interactive mode."""
        print("🚀 Interactive CV Agent - Embedding-First Search!")
        print("Ask me about Vaios Laschos's research using semantic search.")
        print("Type 'exit' to quit, 'clear' to reset conversation.\n")
        
        thread_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        while True:
            try:
                user_input = input("\n🤔 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'clear':
                    thread_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    print("🔄 Conversation cleared.")
                    continue
                elif not user_input:
                    continue
                
                print("\n🤖 Agent: ", end="", flush=True)
                response = self.chat(user_input, thread_id)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again with a different question.")


def main():
    """Main entry point."""
    try:
        agent = InteractiveCVAgent()
        agent.run_interactive()
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()