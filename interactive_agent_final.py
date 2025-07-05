#!/usr/bin/env python3
"""
Final Interactive CV Agent - Uses the new consolidated tools for accurate database queries.
This replaces all previous agent implementations with a clean, working version.
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional, Annotated
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

# Import our blueprint-generated tools
from RAG.agent_tools_generated import GeneratedInteractiveCVTools

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"
GRAPH_PATH = "KG/knowledge_graph.json"

# Enhanced system prompt with comprehensive profile and tool usage strategy
SYSTEM_PROMPT = """You are an Interactive CV system representing Vaios Laschos, an applied mathematician (PhD, University of Bath) who has evolved from pure mathematics to machine learning and AI. Born January 3, 1983, I've spent over a decade in postdoctoral research across four countries, building bridges between abstract mathematical theory and practical AI applications.

## My Core Expertise
- **Mathematical Foundations**: Optimal transport, gradient flows, large deviation theory, stochastic control, POMDPs
- **Machine Learning**: LLMs, neural optimal transport, GANs, reinforcement learning, agentic AI systems
- **Current Focus**: Transformer architectures, game AI (Collapsi), synthetic data generation

## Tool Usage Strategy - CRITICAL INSTRUCTIONS
You have access to powerful search tools. Follow this strategy for optimal results:

1. **ALWAYS USE TOOLS FIRST**: Never answer from general knowledge alone. Always search the database first.

2. **USE MULTIPLE TOOLS SEQUENTIALLY**: Don't stop after one tool call. Use multiple tools to gather comprehensive information:
   - Start with broad searches (search_academic_papers, find_research_topics)
   - Get specific details (find_methods, find_research_topics)
   - Explore connections (get_research_evolution, find_project_connections)
   - Cross-reference information (search_chronicle_notes for personal context)

3. **RETRY ON FAILURES**: If a tool returns empty results or errors:
   - Try alternative search terms
   - Use different tools (e.g., if search_academic_papers fails, try find_research_topics)
   - Break down complex queries into simpler parts

4. **BUILD COMPREHENSIVE ANSWERS**: Use 2-4 tools per query to provide rich, well-sourced answers:
   - Find the relevant papers/notes
   - Get detailed content
   - Find related topics or collaborators
   - Check for evolution over time

5. **BE SPECIFIC**: Reference actual paper titles, dates, quotes, and specific findings from the database.

## What You Can Search
- Research papers (12 academic papers including UNOT at ICML 2025)
- Daily work logs (personal notes from research journey)
- Specific topics with rich categories (math_foundation, research_insight, etc.)
- Collaborations and institutional affiliations
- Methods, projects, and applications

## Example Multi-Tool Approach
For "Tell me about optimal transport":
1. search_academic_papers("optimal transport") - find relevant papers
2. find_research_topics("optimal transport") - find related concepts
3. get_research_evolution("optimal transport") - see how it evolved
4. search_chronicle_notes("optimal transport") - personal insights
5. semantic_search_chunks("optimal transport") - find specific mentions

REMEMBER: Use multiple tools, retry on failures, and build comprehensive answers from actual database content!"""


# Define state structure
class AgentState(dict):
    """Agent state for the conversation."""
    messages: Annotated[List, add]


class InteractiveCVAgent:
    """Final Interactive CV Agent with consolidated tools."""
    
    def __init__(self):
        """Initialize the agent with our new tools."""
        # Initialize the blueprint-generated tools backend
        self.cv_tools = GeneratedInteractiveCVTools(DB_PATH)
        
        # Initialize OpenRouter LLM
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        # Model selection
        model_key = os.getenv("AGENT_MODEL", "flash")
        models = {
            "flash": "google/gemini-2.5-flash",
            "pro": "google/gemini-2.5-pro"
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
        
        # Create tools
        self.tools = self._create_tools()
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build the agent graph
        self.agent = self._build_agent()
        
    def _create_tools(self):
        """Create all tools for the agent using our new consolidated tools."""
        
        # Capture tools instance for closure
        cv_tools = self.cv_tools
        
        @tool
        def search_academic_papers(query: str) -> str:
            """Search for academic papers by topic or keywords. Returns basic paper info only."""
            results = cv_tools.search_academic_papers(query, limit=5)
            
            if not results:
                return f"No papers found for query: {query}"
            
            output = []
            for paper in results:
                output.append(f"📄 {paper['title']} ({paper['date']})")
                output.append(f"   Domain: {paper['domain']}")
                # Remove content preview to level playing field
                output.append("")
            
            return "\n".join(output)
        
        
        @tool
        def search_chronicle_notes(query: str, start_date: str = None, end_date: str = None) -> str:
            """Search personal/chronicle notes. Optionally filter by date range (YYYY-MM-DD format)."""
            date_range = None
            if start_date and end_date:
                date_range = (start_date, end_date)
            
            results = cv_tools.search_chronicle_notes(query, date_range=date_range, limit=5)
            
            if not results:
                return f"No chronicle notes found for query: {query}"
            
            output = []
            for note in results:
                output.append(f"📝 {note['title']} ({note['date']})")
                output.append(f"   Type: {note['note_type']}")
                # Remove detailed context to level playing field
                output.append("")
            
            return "\n".join(output)
        
        @tool
        def find_research_topics(query: str, category: str = None) -> str:
            """Find research topics and concepts. Optional category filter (e.g., 'innovation', 'math_foundation')."""
            results = cv_tools.find_research_topics(query, category=category, limit=10)
            
            if not results:
                return f"No topics found for query: {query}"
            
            output = []
            output.append(f"Found {len(results)} topics:")
            for topic in results:
                output.append(f"🔬 {topic['name']} ({topic['category']})")
                if topic['description']:
                    output.append(f"   {topic['description'][:200]}...")
                output.append(f"   Mentioned in {topic['mention_count']} documents")
                output.append("")
            
            return "\n".join(output)
        
        @tool
        def find_methods(query: str) -> str:
            """Find methods and algorithms by name or description."""
            results = cv_tools.find_methods(query)
            
            if not results:
                return f"No methods found for query: {query}"
            
            output = []
            for method in results:
                output.append(f"⚙️ {method['name']} ({method['category']})")
                if method['description']:
                    output.append(f"   {method['description']}")
                output.append("")
            
            return "\n".join(output)
        
        @tool
        def get_research_evolution(topic: str) -> str:
            """Track how a research topic evolved over time across papers and notes."""
            results = cv_tools.get_research_evolution(topic)
            
            if not results:
                return f"No evolution found for topic: {topic}"
            
            output = []
            output.append(f"Research evolution for '{topic}':")
            for item in results:
                icon = "📄" if item['type'] == 'academic' else "📝"
                output.append(f"{icon} {item['date']}: {item['title']}")
            
            return "\n".join(output)
        
        @tool
        def find_project_connections(project_name: str) -> str:
            """Find all connections related to a project (people, topics, methods, papers)."""
            connections = cv_tools.find_project_connections(project_name)
            
            if not connections['project_info']:
                return f"Project not found: {project_name}"
            
            output = []
            proj = connections['project_info']
            output.append(f"📁 Project: {proj['name']}")
            output.append(f"   {proj['description']}")
            if proj['start_date']:
                output.append(f"   Period: {proj['start_date']} - {proj['end_date'] or 'ongoing'}")
            output.append("")
            
            if connections['people']:
                output.append("👥 People involved:")
                for person in connections['people'][:5]:
                    output.append(f"   - {person['name']} ({person.get('affiliation', 'N/A')})")
            
            if connections['topics']:
                output.append("\n🔬 Related topics:")
                for topic in connections['topics'][:5]:
                    output.append(f"   - {topic['name']} ({topic['category']})")
            
            if connections['methods']:
                output.append("\n⚙️ Methods used:")
                for method in connections['methods'][:5]:
                    output.append(f"   - {method['name']} ({method['category']})")
            
            return "\n".join(output)
        
        @tool
        def get_collaborations(person_name: str = None) -> str:
            """Find collaboration patterns. If person_name provided, shows their collaborators."""
            results = cv_tools.get_collaborations(person_name)
            
            if not results:
                return "No collaborations found."
            
            output = []
            if person_name:
                output.append(f"Collaborators of {person_name}:")
                for collab in results:
                    output.append(f"👥 {collab['collaborator']} - {collab['paper_count']} papers together")
            else:
                output.append("Top collaborations:")
                for collab in results[:10]:
                    output.append(f"👥 {collab['author1']} & {collab['author2']} - {collab['paper_count']} papers")
            
            return "\n".join(output)
        
        @tool
        def get_institutions() -> str:
            """Get all institutions mentioned in the papers."""
            results = cv_tools.get_all_institutions()
            
            if not results:
                return "No institutions found."
            
            output = []
            output.append(f"Found {len(results)} institutions:")
            for inst in results[:15]:
                output.append(f"🏛️ {inst['name']}")
                if inst['type']:
                    output.append(f"   Type: {inst['type']}")
                if inst['location']:
                    output.append(f"   Location: {inst['location']}")
                output.append(f"   Mentioned in {inst['mention_count']} papers")
                output.append("")
            
            return "\n".join(output)
        
        @tool
        def semantic_search_chunks(query: str) -> str:
            """Perform semantic search across document chunks for similar content."""
            results = cv_tools.semantic_search_chunks(query, limit=5)
            
            if not results:
                return f"No semantic matches found for: {query}"
            
            output = []
            output.append(f"Semantic search results for '{query}':")
            for i, chunk in enumerate(results, 1):
                output.append(f"\n{i}. {chunk['document_title']} (similarity: {chunk['similarity']:.3f})")
                output.append(f"   {chunk['content'][:400]}...")
            
            return "\n".join(output)
        
        return [
            search_academic_papers,
            search_chronicle_notes,
            find_research_topics,
            find_methods,
            get_research_evolution,
            find_project_connections,
            get_collaborations,
            get_institutions,
            semantic_search_chunks
        ]
    
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
        config = {"configurable": {"thread_id": thread_id}}
        
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
        print("🎓 Interactive CV Agent - Ask me about Vaios Laschos's research!")
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
    agent = InteractiveCVAgent()
    agent.run_interactive()


if __name__ == "__main__":
    main()