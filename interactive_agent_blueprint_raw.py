#!/usr/bin/env python3
"""
Blueprint-Raw Interactive CV Agent - Uses ALL 79 blueprint-generated tools directly.
This is the true blueprint revolution: the agent has access to the full spectrum 
of automatically-generated, schema-safe, domain-aware tools.
"""

import os
import sys
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

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from RAG.blueprint_driven_tools import BlueprintDrivenToolGenerator

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"

# Enhanced system prompt for blueprint-powered agent with intelligent orchestration
SYSTEM_PROMPT = """You are an Interactive CV system representing Vaios Laschos, powered by a revolutionary blueprint-driven tool system with 79 automatically-generated, domain-aware tools.

## About Vaios Laschos
Applied mathematician (PhD, University of Bath, born Jan 3, 1983) who evolved from pure mathematics to machine learning and AI. Over a decade of postdoctoral research across four countries, building bridges between abstract mathematical theory and practical AI applications.

## Core Expertise
- **Mathematical Foundations**: Optimal transport, gradient flows, large deviation theory, stochastic control, POMDPs
- **Machine Learning**: LLMs, neural optimal transport, GANs, reinforcement learning, agentic AI systems  
- **Current Focus**: Transformer architectures, game AI (Collapsi), synthetic data generation

## INTELLIGENT TOOL ORCHESTRATION STRATEGIES

### 1. **SMART QUERY PATTERNS**

**For Institution Questions**: 
- Use `list_institutions` (gets ALL institutions, not search-based)
- Then use `search_people` with "Vaios" to find author connections
- Use relationship traversal to connect people to institutions

**For Author/People Questions**:
- Use `search_people` with author name
- Use `reverse_authored_by` to find papers by that person  
- Use `traverse_affiliated_with` to find institutional connections

**For Paper/Content Questions**:
- Start with `search_academic_documents` with relevant terms
- Use `get_academic_documents_by_id` to get full content
- Use `reverse_discusses` to find related topics
- Use `traverse_authored_by` to find authors

**For Topic Evolution**:
- Use `search_topics` to find relevant topics
- Use `reverse_discusses` to find documents mentioning each topic
- Use `search_chronicle_documents` to find personal notes
- Sort results chronologically

### 2. **BLUEPRINT ADVANTAGE EXPLOITATION**

**Rich Categorization**: Use `explore_topic_categories` to see all 22+ categories
**Bidirectional Relationships**: Use both `traverse_*` AND `reverse_*` for complete coverage
**Domain Separation**: Use `search_academic_*` vs `search_personal_*` for targeted results
**List vs Search**: Use `list_*` tools to get ALL entities, then filter

### 3. **MANDATORY MULTI-TOOL SEQUENCES**

**Example: "What institutions has Vaios been affiliated with?"**
1. `search_academic_documents` query="Vaios" - Find papers by Vaios
2. For each paper, use `traverse_affiliated_with` source_type="document" source_id="academic_X"
3. `get_institutions_by_id` for each institution ID found
4. Combine all institutional affiliations across papers

**Example: "Tell me about optimal transport"**
1. `search_topics` query="optimal transport" - Find relevant topics
2. `search_academic_documents` query="optimal transport" - Find papers
3. `reverse_discusses` - Find what documents discuss these topics
4. `explore_topic_categories` category="math_foundation" - See related mathematical concepts

### 4. **CRITICAL SUCCESS PATTERNS**

- **ALWAYS use `list_*` tools for comprehensive data** (institutions, people, etc.)
- **Use relationship traversal** (`traverse_*`, `reverse_*`) to find connections
- **Combine academic and personal searches** for complete picture
- **Reference specific tool results** in your answers
- **Chain 3-5 tools minimum** per significant query

### 5. **RECOVERY STRATEGIES**

If `search_*` returns empty:
- Try `list_*` instead (gets everything, then filter)
- Try different search terms (author name, partial matches)
- Use relationship traversal from related entities

## MANDATORY BEHAVIOR
1. Use AT LEAST 3 different tools per query
2. Show your tool selection reasoning  
3. Reference specific results from each tool
4. Use both direct searches AND relationship traversal
5. Combine academic and personal data sources

You have 79 sophisticated tools - use them intelligently to provide comprehensive, well-sourced answers that demonstrate the blueprint revolution's power!"""


# Define state structure
class AgentState(dict):
    """Agent state for the conversation."""
    messages: Annotated[List, add]


class BlueprintRawAgent:
    """Interactive CV Agent using all 79 blueprint-generated tools directly."""
    
    def __init__(self):
        """Initialize the agent with all blueprint tools."""
        print("🔧 Initializing Blueprint-Driven Tool Generator...")
        
        # Initialize the blueprint tool generator
        try:
            self.tool_generator = BlueprintDrivenToolGenerator(DB_PATH)
            generated_tools = self.tool_generator.list_all_tools()
            print(f"✅ Successfully generated {len(generated_tools)} tools from blueprints")
        except Exception as e:
            print(f"❌ Error initializing blueprint tools: {e}")
            raise
        
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
                "X-Title": "Blueprint Raw Interactive CV Agent",
            }
        )
        
        print(f"🤖 Agent using model: {model_name}")
        
        # Convert blueprint tools to LangChain tools
        self.tools = self._create_langchain_tools()
        print(f"🔧 Converted {len(self.tools)} blueprint tools to LangChain format")
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build the agent graph
        self.agent = self._build_agent()
        print("✅ Blueprint Raw Agent ready!")
    
    def _create_langchain_tools(self):
        """Convert all blueprint-generated tools to LangChain tools."""
        langchain_tools = []
        
        for tool_name, generated_tool in self.tool_generator.list_all_tools().items():
            # Create a properly typed function for each tool
            tool_func = self._create_typed_tool_function(tool_name, generated_tool)
            
            # Create LangChain tool
            lc_tool = tool(description=generated_tool.description)(tool_func)
            langchain_tools.append(lc_tool)
        
        return langchain_tools
    
    def _create_typed_tool_function(self, tool_name: str, generated_tool):
        """Create a properly typed function for a blueprint tool."""
        params = generated_tool.parameters
        
        # Create function signature based on parameters
        if 'query' in params and 'limit' in params:
            # Search-type tool
            def tool_func(query: str, limit: int = 10, **kwargs):
                return self._execute_and_format_tool(tool_name, query=query, limit=limit, **kwargs)
        elif 'entity_id' in params:
            # Get-by-id tool
            def tool_func(entity_id: int, **kwargs):
                return self._execute_and_format_tool(tool_name, entity_id=entity_id, **kwargs)
        elif 'limit' in params and 'offset' in params:
            # List tool
            def tool_func(limit: int = 50, offset: int = 0, **kwargs):
                return self._execute_and_format_tool(tool_name, limit=limit, offset=offset, **kwargs)
        elif 'source_type' in params and 'source_id' in params:
            # Relationship traversal tool
            def tool_func(source_type: str, source_id: str, limit: int = 20, **kwargs):
                return self._execute_and_format_tool(tool_name, source_type=source_type, source_id=source_id, limit=limit, **kwargs)
        elif 'target_type' in params and 'target_id' in params:
            # Reverse relationship tool
            def tool_func(target_type: str, target_id: str, limit: int = 20, **kwargs):
                return self._execute_and_format_tool(tool_name, target_type=target_type, target_id=target_id, limit=limit, **kwargs)
        elif 'category' in params:
            # Category exploration tool
            def tool_func(category: str = None, limit: int = 20, **kwargs):
                return self._execute_and_format_tool(tool_name, category=category, limit=limit, **kwargs)
        elif 'entity_type' in params and 'entity_id' in params:
            # Visualization tool
            def tool_func(entity_type: str, entity_id: str, **kwargs):
                return self._execute_and_format_tool(tool_name, entity_type=entity_type, entity_id=entity_id, **kwargs)
        else:
            # Generic tool - try to handle any parameters
            def tool_func(**kwargs):
                return self._execute_and_format_tool(tool_name, **kwargs)
        
        # Set function metadata
        tool_func.__name__ = tool_name
        tool_func.__doc__ = generated_tool.description
        
        return tool_func
    
    def _execute_and_format_tool(self, tool_name: str, **kwargs):
        """Execute a blueprint tool and format the result."""
        try:
            result = self.tool_generator.execute_tool(tool_name, **kwargs)
            
            # Format the result for better readability
            if isinstance(result, list):
                if not result:
                    return f"No results found for {tool_name}"
                
                output = []
                for i, item in enumerate(result[:10]):
                    if isinstance(item, dict):
                        # Handle relationship traversal results
                        if 'target_details' in item:
                            target = item['target_details']
                            name_field = target.get('name', f"Item {i+1}")
                            category = item.get('relationship_type', '')
                            description = f"Confidence: {item.get('confidence', 'N/A')}"
                        else:
                            name_field = item.get('name', item.get('title', f"Item {i+1}"))
                            category = item.get('category', item.get('type', ''))
                            description = item.get('description', item.get('content', ''))
                        
                        output.append(f"• {name_field}")
                        if category:
                            output.append(f"  Category: {category}")
                        if description:
                            desc_preview = description[:200] + "..." if len(description) > 200 else description
                            output.append(f"  {desc_preview}")
                        output.append("")
                
                if len(result) > 10:
                    output.append(f"... and {len(result) - 10} more results")
                
                return "\n".join(output)
            
            elif isinstance(result, dict):
                output = []
                for key, value in result.items():
                    if key == 'entities' and isinstance(value, list):
                        output.append(f"{key}: {len(value)} items")
                        for entity in value[:3]:
                            if isinstance(entity, dict):
                                entity_name = entity.get('name', str(entity))
                                output.append(f"  • {entity_name}")
                    elif key == 'categories' and isinstance(value, list):
                        output.append(f"{key}: {len(value)} categories")
                        for cat in value[:5]:
                            if isinstance(cat, dict):
                                cat_name = cat.get('category', str(cat))
                                count = cat.get('count', '')
                                output.append(f"  • {cat_name}: {count}")
                    else:
                        if isinstance(value, str) and len(value) > 200:
                            value = value[:200] + "..."
                        output.append(f"{key}: {value}")
                return "\n".join(output)
            
            else:
                result_str = str(result)
                if len(result_str) > 1000:
                    result_str = result_str[:1000] + "..."
                return result_str
                
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
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
        print("🚀 Blueprint Raw Interactive CV Agent - Powered by 79 Auto-Generated Tools!")
        print("Ask me about Vaios Laschos's research using the full spectrum of blueprint tools.")
        print("Type 'exit' to quit, 'clear' to reset conversation, 'tools' to see available tools.\n")
        
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
                elif user_input.lower() == 'tools':
                    self._show_available_tools()
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
    
    def _show_available_tools(self):
        """Show all available blueprint-generated tools."""
        print("\n🔧 Available Blueprint-Generated Tools:")
        
        # Group tools by category
        categories = {}
        for tool_name, generated_tool in self.tool_generator.list_all_tools().items():
            category = generated_tool.category
            if category not in categories:
                categories[category] = []
            categories[category].append((tool_name, generated_tool.description))
        
        for category, tools in categories.items():
            print(f"\n📁 {category.upper()} ({len(tools)} tools):")
            for tool_name, description in tools[:5]:  # Show first 5 in each category
                print(f"  • {tool_name}: {description[:60]}...")
            if len(tools) > 5:
                print(f"  ... and {len(tools) - 5} more")
        
        print(f"\nTotal: {len(self.tool_generator.list_all_tools())} tools available!")


def main():
    """Main entry point."""
    try:
        agent = BlueprintRawAgent()
        agent.run_interactive()
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()