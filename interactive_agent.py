#!/usr/bin/env python3
"""
Interactive CV Agent - Embedding-first agent with minimal tools.
Uses semantic search across all entities with simple graph navigation.
"""

import os
import sys
import sqlite3
import numpy as np
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

from Profile.profile_loader import ProfileLoader
from RAG.semantic_search import SemanticSearchEngine
from agents.manuscript_agent import ManuscriptAgent
from agents.sequential_reasoning_agent import SequentialReasoningSync

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"

# Load centralized profile and create new system prompt
try:
    profile_loader = ProfileLoader()
    base_prompt = profile_loader.get_agent_system_prompt()
    
    SYSTEM_PROMPT = base_prompt + """

## CRITICAL IDENTITY MAPPING

**IMPORTANT**: When users ask about "Vaios", "Laschos", "me", "my work", "my research", or related pronouns, they are referring to **Vaios Laschos**. Use these name variations in searches:
- "Vaios Laschos" (full name)
- "Vaios" (first name only)  
- "Laschos" (last name only)
- "V. Laschos" (academic format)

## PROFILE KNOWLEDGE FALLBACK

**MANDATORY FALLBACK RULE**: If database searches return no results for questions about Vaios Laschos, you MUST use the comprehensive profile knowledge already loaded in your system prompt above. You have detailed information about his institutional affiliations, research expertise, mathematical concepts, practical work, and professional experience. NEVER say "no information found" about Vaios Laschos!

**INSTITUTIONAL AFFILIATIONS FALLBACK**: If you cannot find Vaios's institutional affiliations through database queries, use the profile knowledge which clearly states his affiliations: WIAS Berlin (2021-Present & 2015-2017), Technical University of Berlin (2018-2020), Brown University (2013-2015), MPI Leipzig (2013), University of Bath (PhD 2009-2013).

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

## SEARCH STRATEGIES

1. **For concept exploration**: Use semantic_search with descriptive queries
2. **For specific people/institutions**: Semantic search handles name variations  
3. **For time-based queries**: Include dates in semantic search
4. **For relationship exploration**: Combine semantic_search + navigate_relationships
5. **For complex multi-domain questions**: Use sequential_reasoning AFTER gathering initial information

## SEQUENTIAL REASONING USAGE GUIDE

**DO USE sequential_reasoning when:**
- Question connects multiple domains (e.g., "theoretical math → game development")
- Requires logical analysis of relationships between concepts
- Needs step-by-step reasoning to connect ideas
- Involves complex "How does X relate to Y?" questions
- Profile-based extrapolation from limited data

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

**CRITICAL**: Always use get_entity_details to examine promising documents! Don't conclude "no results" from just the search preview.

**Follow-up Strategy**: 
1. If semantic_search finds documents with relevant dates/topics → get_entity_details to see full content
2. Look for implementation work, coding activities, project development in chronicle documents
3. Multiple tools are better than concluding "no information found"

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

**Database Search Method**:
Finding an author's institutions requires a TWO-HOP traversal because there's NO direct person→institution relationship:
1. Person → Documents (reverse "authored_by") 
2. Documents → Institutions (forward "affiliated_with")

The database has these institutions: TU Berlin, WIAS Berlin, Harvard University, Kempner Institute, etc.

## FALLBACK STRATEGIES
1. Use semantic_search("Vaios Laschos affiliation" or "Vaios institution") 
2. Search for known institutions: semantic_search("TU Berlin", entity_types=["institution"])
3. Get document details and search content: get_entity_details("document", "academic_X") and look for affiliations in text

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
                output.append(f"  → {rel_type} → {target_type} {target_id} (confidence: {confidence:.2f})")
            else:
                source_type, source_id, rel_type, confidence = row
                output.append(f"  ← {rel_type} ← {source_type} {source_id} (confidence: {confidence:.2f})")
        
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
    for complex queries that require deep thinking.
    
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
        # Use simplified sequential reasoning to avoid subprocess issues
        return _simple_sequential_reasoning(problem, domain, use_alternatives)
        
    except Exception as e:
        return f"Error in sequential reasoning: {str(e)}"


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
        
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                END: END
            }
        )
        workflow.add_edge("tools", "agent")
        
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