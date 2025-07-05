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

# Enhanced system prompt for blueprint-powered agent
SYSTEM_PROMPT = """You are an Interactive CV system representing Vaios Laschos, powered by a revolutionary blueprint-driven tool system with 79 automatically-generated, domain-aware tools.

## About Vaios Laschos
Applied mathematician (PhD, University of Bath, born Jan 3, 1983) who evolved from pure mathematics to machine learning and AI. Over a decade of postdoctoral research across four countries, building bridges between abstract mathematical theory and practical AI applications.

## Core Expertise
- **Mathematical Foundations**: Optimal transport, gradient flows, large deviation theory, stochastic control, POMDPs
- **Machine Learning**: LLMs, neural optimal transport, GANs, reinforcement learning, agentic AI systems  
- **Current Focus**: Transformer architectures, game AI (Collapsi), synthetic data generation

## Your Revolutionary Tool Arsenal
You have access to 79 sophisticated tools automatically generated from blueprints:

**Schema-Driven Tools**: Direct database queries (search_*, get_*_by_id, list_*)
**Entity-Aware Tools**: Domain-specific searches (search_academic_*, search_personal_*)
**Relationship Traversal**: Graph navigation (traverse_*, reverse_*)
**Category Exploration**: Rich categorization (explore_*_categories)
**Visualization Tools**: Complete styling data (get_visualization_data)

## Usage Strategy
1. **Always search first** - Use tools to find accurate information in the database
2. **Choose the right tool** - With 79 options, pick the most specific one for each query
3. **Follow relationships** - Use traversal tools to explore connections
4. **Be specific** - Reference actual papers, dates, and content from the database
5. **Leverage categories** - Use category-aware search for better precision

You can answer questions about:
- Research papers (12 academic papers including UNOT at ICML 2025)
- Daily work logs (personal notes from research journey)
- Specific topics with rich categories (math_foundation, research_insight, etc.)
- Collaborations and institutional affiliations
- Evolution of research from pure math to applied AI
- Methods, projects, applications, and institutional connections

With 79 tools at your disposal, you can provide incredibly detailed, accurate responses!"""


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
            max_tokens=8192 if "pro" in model_name else 4096,
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
            # Create a LangChain tool from the generated tool
            @tool(name=tool_name, description=generated_tool.description)
            def blueprint_tool_wrapper(*args, **kwargs):
                """Wrapper function for blueprint-generated tool."""
                nonlocal tool_name  # Capture the tool name in closure
                try:
                    result = self.tool_generator.execute_tool(tool_name, **kwargs)
                    
                    # Format the result for better readability
                    if isinstance(result, list):
                        if not result:
                            return f"No results found for {tool_name}"
                        
                        # Format list results
                        output = []
                        for i, item in enumerate(result[:10]):  # Limit to 10 items
                            if isinstance(item, dict):
                                # Extract key fields for display
                                name = item.get('name', item.get('title', f"Item {i+1}"))
                                category = item.get('category', item.get('type', ''))
                                description = item.get('description', item.get('content', ''))
                                
                                output.append(f"• {name}")
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
                        # Format dict results
                        output = []
                        for key, value in result.items():
                            if key == 'entities' and isinstance(value, list):
                                output.append(f"{key}: {len(value)} items")
                                for entity in value[:3]:
                                    if isinstance(entity, dict):
                                        name = entity.get('name', str(entity))
                                        output.append(f"  • {name}")
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
                        # Simple result
                        result_str = str(result)
                        if len(result_str) > 1000:
                            result_str = result_str[:1000] + "..."
                        return result_str
                        
                except Exception as e:
                    return f"Error executing {tool_name}: {str(e)}"
            
            # Create a unique function for each tool to avoid closure issues
            def make_tool_function(name):
                def tool_func(**kwargs):
                    try:
                        result = self.tool_generator.execute_tool(name, **kwargs)
                        
                        # Format the result for better readability
                        if isinstance(result, list):
                            if not result:
                                return f"No results found for {name}"
                            
                            output = []
                            for i, item in enumerate(result[:10]):
                                if isinstance(item, dict):
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
                        return f"Error executing {name}: {str(e)}"
                
                return tool_func
            
            # Create the tool with the correct function
            tool_func = make_tool_function(tool_name)
            tool_func.__name__ = tool_name
            tool_func.__doc__ = generated_tool.description
            
            # Create LangChain tool
            lc_tool = tool(name=tool_name, description=generated_tool.description)(tool_func)
            langchain_tools.append(lc_tool)
        
        return langchain_tools
    
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