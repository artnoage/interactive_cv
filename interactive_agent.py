#!/usr/bin/env python3
"""
Interactive CV Agent - Embedding-first agent with minimal tools.
Uses semantic search across all entities with simple graph navigation.
"""

import os
import sys
import sqlite3
from datetime import datetime
from typing import List, Optional, Annotated, TypedDict, cast, Any
from operator import add
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from pydantic import SecretStr

from dotenv import load_dotenv

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add MCP path for sequential thinking
mcp_path = project_root / "mcp_subfolder"
sys.path.insert(0, str(mcp_path))

# Profile content is now loaded from external files
from RAG.semantic_search import SemanticSearchEngine
from agents.manuscript_agent import ManuscriptAgent
# from client.mcp_client import SequentialThinkingClient  # Commented out until MCP client is fixed

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"

def load_prompt_file(filename: str) -> str:
    """Load prompt content from a file."""
    try:
        with open(f"prompts/{filename}", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Prompt file {filename} not found, using fallback")
        return "Interactive CV Agent prompt file not found."

# Load system prompt from file
SYSTEM_PROMPT = load_prompt_file("main_agent_prompt.txt")
PEP_TALK_PROMPT_TEMPLATE = load_prompt_file("pep_talk_coach_prompt.txt")
print("✅ Prompts loaded from external files")


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
        params.append(str(limit))
        
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
        # Use MCP Sequential Thinking (fallback to simplified reasoning for now)
        print("Starting Sequential Reasoning...")
        
        # For now, use simplified reasoning until MCP client is fixed
        return _simple_sequential_reasoning(problem, domain, use_alternatives)
        
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


# MCP functions removed - using simplified reasoning for now


# MCP formatting functions removed - using simplified reasoning for now


# Define state structure
class AgentState(TypedDict):
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
        
        # Model selection - Default to Flash for cost efficiency
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
            """The motivational coach that intervenes ONLY when the answer has no useful information at all."""
            messages = state["messages"]
            
            # Only intervene once - check if we've already given a pep talk
            pep_talk_count = sum(1 for msg in messages 
                               if isinstance(msg, AIMessage) and "HEY AGENT!" in str(msg.content))
            
            # If we've already given a pep talk, let everything through
            if pep_talk_count >= 1:
                return {"messages": messages}
            
            # Get the last AI message
            last_message = messages[-1]
            
            # Check if it's an AI message with content (not tool calls)
            if isinstance(last_message, AIMessage) and last_message.content and not last_message.tool_calls:
                # Handle both string and list content
                content_text = last_message.content
                if isinstance(content_text, list):
                    content_text = str(content_text)
                content = content_text.lower()
                
                # Only intervene for truly non-informative responses
                non_informative_patterns = [
                    # Planning/procrastination without actual information
                    "i'll search for", "i will search", "let me search", "i need to",
                    "to answer this", "i'll look for", "let me find", "i need to find",
                    "i'll need to", "we need to", "i should", "first i'll",
                    
                    # Technical failures without information
                    "i cannot find", "unable to retrieve", "entity not found",
                    "no information available", "no data found", "not found in the database",
                    
                    # Generic placeholder responses
                    "institution_", "institution 2", "institution 3",  # institution IDs
                    "person_", "method_", "topic_",  # other generic IDs
                    
                    # Empty or error responses
                    "error getting answer", "failed to", "cannot access"
                ]
                
                # Check if the response is truly non-informative
                is_non_informative = any(pattern in content for pattern in non_informative_patterns)
                
                # Also check for extremely short responses (less than 20 characters)
                is_too_short = len(content.strip()) < 20
                
                # Check for responses that are just error messages or placeholders
                is_error_only = any(error in content for error in [
                    "error:", "exception:", "failed:", "unable to", "cannot", "not found"
                ]) and len(content.strip()) < 100
                
                if is_non_informative or is_too_short or is_error_only:
                    # Give general advice without seeing the question
                    pep_talk_message = """🎯 HEY AGENT! Your response doesn't provide useful information to the user. 

Here's what you should do:
• Use your tools to find specific information
• Provide actual names, not generic IDs (e.g., "University of Bath", not "institution_1")
• Give concrete details from your knowledge base
• If you can't find something, try different search terms or tools
• Use semantic_search, navigate_relationships, and get_entity_details
• For complex questions, try sequential_reasoning
• For technical details, try consult_manuscript

Remember: The user needs real information, not planning statements!"""
                    
                    pep_talk = AIMessage(content=pep_talk_message)
                    
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
        result = self.agent.invoke(initial_state, cast(Any, config))
        
        # Extract the final AI message
        for message in reversed(result["messages"]):
            if isinstance(message, AIMessage):
                # Handle both string and list content
                content = message.content
                if isinstance(content, list):
                    return str(content)
                return content
        
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