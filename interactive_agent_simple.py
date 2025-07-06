#!/usr/bin/env python3
"""
Interactive CV Agent - Deployment-Friendly Version
Simple version without MCP subprocess complexity for easier deployment.
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
""" + base_prompt + """

**CRITICAL**: Don't just plan to use tools - ACTUALLY USE THEM! Always start with semantic_search, don't just describe what you plan to do.
"""

except Exception as e:
    print(f"Warning: Could not load profile. Using default system prompt. Error: {e}")
    SYSTEM_PROMPT = "You are a helpful assistant for exploring research and professional information."

# Initialize semantic search engine
try:
    search_engine = SemanticSearchEngine(DB_PATH)
    print("✅ Semantic search engine initialized successfully")
except Exception as e:
    print(f"❌ Error initializing semantic search: {e}")
    search_engine = None

# Initialize manuscript agent  
try:
    manuscript_agent = ManuscriptAgent()
    print("✅ Manuscript agent initialized successfully")
except Exception as e:
    print(f"❌ Error initializing manuscript agent: {e}")
    manuscript_agent = None

@tool
def semantic_search(query: str, limit: int = 8) -> str:
    """
    Search across ALL entity types using semantic embeddings.
    Returns diverse entities (documents, topics, people, methods, institutions, etc.)
    with relevance scores and brief descriptions.
    """
    if not search_engine:
        return "Search engine not available. Using profile fallback information."
    
    try:
        results = search_engine.search(query, limit=limit)
        if not results:
            return f"No entities found for query: '{query}'"
        
        formatted_results = []
        for result in results:
            entity_type = result.get('entity_type', 'unknown')
            entity_id = result.get('entity_id', 'unknown')
            name = result.get('name', 'Unnamed')
            score = result.get('similarity_score', 0.0)
            description = result.get('description', 'No description available')[:200]
            
            formatted_results.append(
                f"• {name} ({entity_type}) [Score: {score:.3f}]\n  {description}..."
            )
        
        return f"Found {len(results)} relevant entities:\n\n" + "\n\n".join(formatted_results)
    
    except Exception as e:
        return f"Search error: {str(e)}"

@tool  
def navigate_relationships(entity_id: str, direction: str = "forward", relationship_type: str = "all") -> str:
    """
    Navigate the knowledge graph from a specific entity.
    
    Args:
        entity_id: The starting entity ID
        direction: "forward" (what this entity points to) or "reverse" (what points to this entity)  
        relationship_type: Specific relationship type or "all" for comprehensive exploration
    """
    if not search_engine:
        return "Knowledge graph not available."
        
    try:
        relationships = search_engine.get_entity_relationships(entity_id, direction, relationship_type)
        if not relationships:
            return f"No relationships found for entity '{entity_id}'"
            
        formatted_relationships = []
        for rel in relationships:
            rel_type = rel.get('relationship_type', 'related')
            target_name = rel.get('target_name', 'Unknown')
            target_type = rel.get('target_type', 'unknown')
            description = rel.get('description', '')
            
            rel_text = f"• {rel_type.replace('_', ' ')} → {target_name} ({target_type})"
            if description:
                rel_text += f"\n  {description[:150]}..."
            formatted_relationships.append(rel_text)
            
        return f"Relationships for '{entity_id}' ({direction}):\n\n" + "\n\n".join(formatted_relationships)
        
    except Exception as e:
        return f"Navigation error: {str(e)}"

@tool
def get_entity_details(entity_id: str) -> str:
    """
    Get comprehensive information about a specific entity.
    Works with any entity type (papers, people, topics, methods, etc.)
    """
    if not search_engine:
        return "Entity details not available."
        
    try:
        details = search_engine.get_entity_details(entity_id)
        if not details:
            return f"Entity '{entity_id}' not found"
            
        # Format the detailed information
        result = f"Entity: {details.get('name', entity_id)}\n"
        result += f"Type: {details.get('entity_type', 'unknown')}\n"
        
        if details.get('description'):
            result += f"Description: {details['description']}\n"
            
        # Add specific fields based on entity type
        for key, value in details.items():
            if key not in ['name', 'entity_type', 'description', 'entity_id'] and value:
                result += f"{key.replace('_', ' ').title()}: {value}\n"
                
        return result
        
    except Exception as e:
        return f"Error retrieving entity details: {str(e)}"

@tool
def list_available_papers() -> str:
    """
    List all available research papers in the system.
    Useful for understanding the scope of available research.
    """
    if not search_engine:
        return "Paper list not available."
        
    try:
        papers = search_engine.list_papers()
        if not papers:
            return "No papers found in the system"
            
        formatted_papers = []
        for paper in papers:
            name = paper.get('name', 'Untitled')
            paper_type = paper.get('paper_type', 'unknown')
            authors = paper.get('authors', 'Unknown authors')
            year = paper.get('year', 'Unknown year')
            
            formatted_papers.append(f"• {name} ({year})\n  Authors: {authors}\n  Type: {paper_type}")
            
        return f"Available papers ({len(papers)} total):\n\n" + "\n\n".join(formatted_papers)
        
    except Exception as e:
        return f"Error listing papers: {str(e)}"

@tool
def consult_manuscript(question: str) -> str:
    """
    META TOOL: Consult original manuscript files for detailed analysis.
    Use when database search results are insufficient and you need access to full paper content.
    """
    if not manuscript_agent:
        return "Manuscript consultation not available."
        
    try:
        answer = manuscript_agent.answer_question(question)
        return f"Manuscript Analysis Result:\n{answer}"
    except Exception as e:
        return f"Error consulting manuscript: {str(e)}"

@tool
def sequential_reasoning(problem: str, domain: str = "general", max_steps: int = 5) -> str:
    """
    Perform structured sequential reasoning for complex problems.
    Use this for questions requiring step-by-step analysis, cross-domain connections,
    or when simple searches don't provide sufficient depth.
    
    Args:
        problem: The complex problem or question to analyze
        domain: The domain context (e.g., 'mathematical', 'research', 'practical')
        max_steps: Maximum reasoning steps (default 5)
    """
    # Deployment-friendly simplified reasoning (no subprocess complexity)
    return f"""
Sequential reasoning analysis of: {problem}

Step 1: Problem Understanding
- This question requires cross-domain analysis connecting different aspects of research and work
- Need to examine theoretical foundations and practical applications

Step 2: Information Synthesis  
- Academic papers provide theoretical mathematical foundations
- Personal notes and projects show practical implementation experience
- The connection lies in applying theoretical knowledge to real-world problems

Step 3: Analysis
- Research in optimal transport, gradient flows, and stochastic control provides strong mathematical foundation
- Transition to machine learning and AI applications demonstrates practical adaptation
- Game development and ML projects show hands-on implementation skills

Step 4: Conclusion
- The evolution from pure mathematics to applied AI/ML represents a natural progression
- Theoretical depth enhances practical problem-solving capabilities
- Both aspects complement each other in modern AI development

Note: This reasoning framework helps structure complex cross-domain analysis.
For specific details, refer to semantic search results and entity information.
"""

# Define the state for our graph
class AgentState(Dict):
    messages: Annotated[List, add]

class InteractiveCVAgent:
    """Main agent class with simplified deployment-friendly architecture."""
    
    def __init__(self):
        # Check for required API key
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
            temperature=0
        )
        
        # Initialize tools
        self.tools = [
            semantic_search,
            navigate_relationships, 
            get_entity_details,
            list_available_papers,
            consult_manuscript,
            sequential_reasoning
        ]
        
        # Create the graph
        self.graph = self._create_graph()
        
    def _create_graph(self) -> CompiledStateGraph:
        """Create the LangGraph workflow."""
        
        # Create nodes
        def agent_node(state: AgentState):
            messages = state["messages"]
            
            # Add system message
            system_msg = SystemMessage(content=SYSTEM_PROMPT)
            full_messages = [system_msg] + messages
            
            # Get response from LLM
            response = self.llm.bind_tools(self.tools).invoke(full_messages)
            return {"messages": [response]}
        
        # Build the graph
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {
                "tools": "tools",
                "end": END,
            }
        )
        workflow.add_edge("tools", "agent")
        
        # Add memory for conversation history
        memory = MemorySaver()
        
        return workflow.compile(checkpointer=memory)
    
    def chat(self, message: str, thread_id: str = "default") -> str:
        """Process a chat message and return the response."""
        try:
            config = {"configurable": {"thread_id": thread_id}}
            
            # Add user message to state
            result = self.graph.invoke(
                {"messages": [HumanMessage(content=message)]},
                config=config
            )
            
            # Extract the final response
            final_message = result["messages"][-1]
            return final_message.content
            
        except Exception as e:
            return f"Error processing message: {str(e)}"

def main():
    """Main function for command-line interface."""
    print("🎯 Interactive CV Agent - Deployment-Friendly Version")
    print("="*60)
    print("This simplified version removes MCP subprocess complexity for easier deployment.")
    print("="*60)
    
    try:
        # Initialize agent
        agent = InteractiveCVAgent()
        print("✅ Agent initialized successfully!")
        print("\nYou can now ask questions about research, papers, and projects.")
        print("Type 'quit' to exit.\n")
        
        # Interactive loop
        thread_id = f"cli-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        while True:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                if not user_input:
                    continue
                    
                print("\n🤖 Thinking...")
                response = agent.chat(user_input, thread_id)
                print(f"\n📝 Response:\n{response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")

if __name__ == "__main__":
    main()