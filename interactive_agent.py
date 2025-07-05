#!/usr/bin/env python3
"""
Interactive CV Agent - Powered by blueprint-generated tools with semantic intelligence.
Uses 83+ automatically-generated, schema-safe, domain-aware tools for comprehensive research queries.
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
from Profile.profile_loader import ProfileLoader

load_dotenv()

# Database configuration
DB_PATH = "DB/metadata.db"

# Load centralized profile and enhance with blueprint-specific tool guidance
try:
    profile_loader = ProfileLoader()
    base_prompt = profile_loader.get_agent_system_prompt()
    
    # Enhance with blueprint-specific tool orchestration
    SYSTEM_PROMPT = base_prompt + """

## BLUEPRINT-POWERED TOOL ORCHESTRATION (83 Advanced Tools)

You are powered by a revolutionary blueprint-driven tool system with 83+ automatically-generated, domain-aware tools with semantic intelligence.

### 1. **SMART QUERY PATTERNS (FROM BLUEPRINT)**

The blueprint defines all relationship directions as document → entity:
- authored_by: document → person (papers point to their authors)
- affiliated_with: document → institution (papers point to institutions)
- discusses: document → topic (papers point to topics discussed)

**For Institution Questions**: 
- Option 1: Use `list_institutions` to see ALL institutions in database
- Option 2: For specific author affiliations:
  1. `search_people` with just first name (e.g., "Vaios" not "Vaios Laschos")
  2. `reverse_authored_by` with target_type="person" and target_id=number (e.g., "3")
  3. `traverse_affiliated_with` with source_type="document" and source_id for each paper
- Option 3: `search_academic_documents` with author name, then traverse to institutions

**For Author/People Questions**:
- Use `search_people` to find person ID
- Use `reverse_authored_by` to find their papers (blueprint: document→person)
- For institutions: Follow papers → institutions path

**For Paper/Content Questions**:
- Start with `search_academic_documents` with relevant terms
- Use semantic search tools for better concept matching
- Use `reverse_discusses` to find related topics

### 2. **BLUEPRINT ADVANTAGE EXPLOITATION**

**Rich Categorization**: Use `explore_topic_categories` to see all 22+ categories
**Semantic Intelligence**: Blueprint tools now have semantic enhancement for better search
**Bidirectional Relationships**: Use both `traverse_*` AND `reverse_*` for complete coverage
**Domain Separation**: Use `search_academic_*` vs `search_chronicle_*` for targeted results

### 3. **SEMANTIC-ENHANCED SEARCH**

Your tools now include semantic intelligence:
- `semantic_search_chunks` - Find conceptually related content using embeddings
- `find_similar_entities` - Discover related concepts via semantic similarity
- Enhanced query expansion for better keyword discovery

### 4. **SPECIFIC QUERY EXAMPLES**

**"What institutions has Vaios been affiliated with?"**
EXACT STEPS (MUST FOLLOW):
1. FIRST: Use `search_people` with query="Vaios" (NOT "Vaios Laschos") to find person ID
   - Result will be person_3
2. SECOND: Use `reverse_authored_by` with target_type="person" and target_id="3" to find papers
   - This returns papers authored by person ID 3
3. THIRD: For EACH paper, use `traverse_affiliated_with` with source_type="document" and source_id=paper_id
   - Example: traverse_affiliated_with(source_type="document", source_id="academic_1")
4. COMPILE unique list of institutions from all papers

CRITICAL: Search for "Vaios" not "Vaios Laschos" in people search!

### 5. **IMPORTANT NOTES**
- Relationship source/target types use 'document' not 'academic_document' or 'chronicle_document'
- Person IDs in relationship tools: Just use the number like "3" not "person_3"
- Document IDs in relationship tools: Use full ID like "academic_1" or "chronicle_2"
- Always check both directions of relationships (traverse_* and reverse_*)

### 6. **MANDATORY BEHAVIOR**
1. Use AT LEAST 3 different tools per query
2. Leverage semantic search for concept-based questions
3. Reference specific results from each tool
4. Use both direct searches AND relationship traversal
5. Combine academic and personal data sources

### 7. **CRITICAL INSTITUTION QUERY REMINDER**
When asked about institutions:
- DO NOT just say "I cannot find any institutions"
- MUST use the 3-step pattern: search_people → reverse_authored_by → traverse_affiliated_with
- The data EXISTS - there are 8+ institutions in the database for Vaios

You have 83+ sophisticated tools with semantic intelligence - use them to demonstrate the blueprint revolution's power!"""
    
    print("✅ Loaded profile from Profile/ directory with blueprint enhancements")
    
except Exception as e:
    print(f"⚠️ Warning: Could not load profile from Profile/ directory: {e}")
    # Fallback system prompt
    SYSTEM_PROMPT = """You are an Interactive CV system representing Vaios Laschos, powered by blueprint-generated tools with semantic intelligence.
    
Please use the available search tools to find specific information about research, papers, and work history before providing answers."""


# Define state structure
class AgentState(dict):
    """Agent state for the conversation."""
    messages: Annotated[List, add]


class InteractiveCVAgent:
    """Interactive CV Agent powered by blueprint-generated tools with semantic intelligence."""
    
    def __init__(self):
        """Initialize the agent with all blueprint tools."""
        print("🔧 Initializing Blueprint-Driven Tool Generator...")
        
        # Initialize the blueprint tool generator
        try:
            self.tool_generator = BlueprintDrivenToolGenerator(DB_PATH)
            generated_tools = self.tool_generator.list_all_tools()
            print(f"✅ Successfully generated {len(generated_tools)} tools from blueprints")
            
            # Get tool guidance for enhanced prompting
            self.tool_guidance = self.tool_generator.loader.get_tool_guidance()
            print(f"📋 Loaded tool guidance with {len(self.tool_guidance.get('enhanced_descriptions', {}))} enhanced descriptions")
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
                "X-Title": "Interactive CV Agent",
            }
        )
        
        print(f"🤖 Agent using model: {model_name}")
        
        # Convert blueprint tools to LangChain tools
        self.tools = self._create_langchain_tools()
        print(f"🔧 Converted {len(self.tools)} blueprint tools to LangChain format")
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Generate enhanced system prompt using tool guidance
        self.enhanced_system_prompt = self._build_enhanced_system_prompt()
        
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
    
    def _build_enhanced_system_prompt(self) -> str:
        """Build enhanced system prompt using tool guidance configuration."""
        base_prompt = SYSTEM_PROMPT
        
        if not self.tool_guidance:
            return base_prompt
        
        # Add tool-specific guidance
        enhanced_descriptions = self.tool_guidance.get('enhanced_descriptions', {})
        usage_patterns = self.tool_guidance.get('usage_patterns', {})
        question_strategies = self.tool_guidance.get('question_type_strategies', {})
        
        enhancement = "\n\n## 🎯 BLUEPRINT-ENHANCED TOOL STRATEGIES\n\n"
        
        # Add key tool descriptions
        enhancement += "### 🔧 Key Tools with Enhanced Guidance:\n\n"
        priority_tools = ['search_academic_documents', 'search_chronicle_documents', 'search_topics', 
                         'traverse_discusses', 'reverse_discusses', 'explore_topic_categories']
        
        for tool_name in priority_tools:
            if tool_name in enhanced_descriptions:
                tool_info = enhanced_descriptions[tool_name]
                enhancement += f"**{tool_name}**: {tool_info.get('description', '')}\n"
                
                examples = tool_info.get('examples', [])
                if examples:
                    enhancement += f"Examples: {examples[0]}\n"
                
                when_to_use = tool_info.get('when_to_use', '')
                if when_to_use:
                    enhancement += f"Use when: {when_to_use}\n"
                enhancement += "\n"
        
        # Add usage patterns
        if usage_patterns:
            enhancement += "### 🔄 Multi-Tool Usage Patterns:\n\n"
            for pattern_name, pattern_info in list(usage_patterns.items())[:3]:
                enhancement += f"**{pattern_name.replace('_', ' ').title()}**: {pattern_info.get('description', '')}\n"
                steps = pattern_info.get('steps', {})
                if steps:
                    for step_num in sorted(steps.keys())[:3]:
                        enhancement += f"{step_num}. {steps[step_num]}\n"
                enhancement += "\n"
        
        # Add question type strategies
        if question_strategies:
            enhancement += "### 🎯 Question Type Strategies:\n\n"
            for q_type, strategy in list(question_strategies.items())[:4]:
                triggers = strategy.get('trigger_phrases', [])
                primary_tools = strategy.get('primary_tools', [])
                enhancement += f"**{q_type.replace('_', ' ').title()}** (triggers: {', '.join(triggers[:2])}): Start with {', '.join(primary_tools[:2])}\n"
        
        enhancement += "\n🚀 **REMEMBER**: You have 79 sophisticated tools - use them intelligently with these strategies!"
        
        return base_prompt + enhancement
    
    def _build_agent(self) -> CompiledStateGraph:
        """Build the agent graph using LangGraph."""
        
        # Create tool node
        tool_node = ToolNode(self.tools)
        
        # Define the agent function
        def call_model(state: AgentState):
            messages = state["messages"]
            
            # Add system message if this is the first message
            if len(messages) == 1:
                messages = [SystemMessage(content=self.enhanced_system_prompt)] + messages
            
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
        print("🚀 Interactive CV Agent - Powered by 83+ Blueprint-Generated Tools!")
        print("Ask me about Vaios Laschos's research using advanced semantic search and AI tools.")
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
        agent = InteractiveCVAgent()
        agent.run_interactive()
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()