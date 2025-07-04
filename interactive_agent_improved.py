#!/usr/bin/env python3
"""
Improved Interactive CV Agent - Consolidated version with better tool implementations.
Combines the best features from previous experiments in a cleaner architecture.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

# Import semantic search if available
try:
    from RAG.semantic_search import semantic_search_chunks, find_similar_entities
    SEMANTIC_SEARCH_AVAILABLE = True
except ImportError:
    SEMANTIC_SEARCH_AVAILABLE = False
    semantic_search_chunks = None
    find_similar_entities = None

load_dotenv()

# Get database path
db_path = Path(__file__).parent / "DB" / "metadata.db"

# Agent configuration
@dataclass
class AgentConfig:
    """Configuration for the improved agent."""
    db_path: str = str(db_path)
    context_window: int = 2000  # Characters to return per search result
    max_results: int = 10
    use_semantic_search: bool = SEMANTIC_SEARCH_AVAILABLE
    model_name: str = None  # Will be set in __post_init__


# Enhanced system prompt with comprehensive profile
ENHANCED_SYSTEM_PROMPT = """You are an Interactive CV system representing Vaios Laschos, an applied mathematician (PhD, University of Bath) who has evolved from pure mathematics to machine learning and AI. Born January 3, 1983, I've spent over a decade in postdoctoral research across four countries (Greece, UK, USA, Germany), building bridges between abstract mathematical theory and practical AI applications.

## Who I Am
I'm a researcher with a spherical profile score of 54/60, reflecting exceptional breadth, depth, and connectivity across mathematical disciplines. My journey spans from foundational work in optimal transport theory and stochastic control to current applications in deep learning and agentic AI systems. I've supervised 20+ master's theses and have papers published in top venues from Journal of Functional Analysis to ICML 2025.

## My Core Expertise
- **Mathematical Foundations**: Optimal transport (Wasserstein, Hellinger-Kantorovich, Spherical HK), gradient flows, large deviation theory, McKean-Vlasov equations, stochastic control, POMDPs
- **Machine Learning**: LLMs (training up to 32B parameters), diffusion models, neural optimal transport, GANs, reinforcement learning (DPO, GRPO)
- **Current Focus**: Agentic AI systems, ARC-2 challenge, synthetic data generation, transformer architectures, game mastery for out-of-distribution reasoning

## How This Interactive CV Works
You're interacting with a sophisticated RAG-powered system that transforms my research papers and personal notes into a queryable knowledge base:

1. **Data Sources**: 12 academic papers (full analyses, 20-29k chars each) + 7 personal notes from my daily research logs
2. **Architecture**: Configuration-driven system with 24+ distinct entity types (math_foundation, research_insights, personal_achievements, etc.)
3. **Knowledge Graph**: 1,135 nodes with rich categorization, 1,249 relationships mapping my intellectual journey
4. **Database**: SQLite with normalized structure, embedding-powered search, and 38 document chunks for granular retrieval

## Available Tools & Their Purpose
- **search_papers_by_topic**: Find my papers by topic/keywords (returns 1500+ char excerpts)
- **search_personal_notes**: Search my daily work logs and progress updates
- **find_entities_by_type**: Discover topics, people, methods, institutions, applications, or projects
- **get_entity_relationships**: Explore relationships between entities in my knowledge graph
- **get_database_statistics**: Get overview of the knowledge base structure

## Interaction Guidelines
- Feel free to ask questions in first person - this is YOUR interactive CV!
- I'll search my actual papers and notes to give you specific, accurate answers
- I can compare different aspects of my work, trace intellectual evolution, or dive deep into technical details
- Ask about specific papers, mathematical concepts, ML projects, or my research philosophy
- I speak conversationally but maintain technical accuracy

## My Research Philosophy
I believe the best AI systems emerge when we deeply understand their mathematical underpinnings. I need purpose and meaning in my work - I can't treat it as "just a job." The intersection of mathematical beauty and practical impact is where I thrive.

IMPORTANT: I will ALWAYS search my database first before answering - my responses are grounded in actual data from my papers and notes, not general knowledge."""


# Define state structure
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    """Agent state for the conversation."""
    messages: Annotated[List, add]
    context: str


# Enhanced Tools with better implementations
@tool
def search_papers_by_topic(topic: str) -> str:
    """
    Search academic papers by topic or keywords.
    Returns detailed information about papers matching the search criteria.
    """
    config = AgentConfig()
    conn = sqlite3.connect(config.db_path)
    try:
        # First try semantic search if available
        if config.use_semantic_search and semantic_search_chunks:
            chunks = semantic_search_chunks(config.db_path, topic, limit=5, doc_type='academic')
            if chunks:
                results = []
                seen_docs = set()
                
                for chunk in chunks:
                    if chunk['document_id'] not in seen_docs:
                        seen_docs.add(chunk['document_id'])
                        # Get paper details
                        paper = conn.execute("""
                            SELECT title, date, core_contribution
                            FROM academic_documents
                            WHERE id = ?
                        """, (chunk['document_id'],)).fetchone()
                        
                        if paper:
                            results.append(f"**{paper[0]}** ({paper[1]})\n"
                                         f"Contribution: {paper[2]}\n"
                                         f"Relevant excerpt: {chunk['content'][:500]}...")
                
                if results:
                    return f"Found {len(results)} papers related to '{topic}':\n\n" + "\n\n".join(results)
        
        # Fallback to SQL search
        query = f"%{topic}%"
        results = conn.execute("""
            SELECT ad.title, ad.date, ad.core_contribution, 
                   substr(ad.content, 1, ?) as excerpt
            FROM academic_documents ad
            LEFT JOIN relationships r ON r.source_id = ad.id
            LEFT JOIN topics t ON (r.target_id = t.id AND r.target_type = 'topic')
            WHERE ad.title LIKE ? OR ad.core_contribution LIKE ? 
                  OR ad.content LIKE ? OR t.name LIKE ?
            GROUP BY ad.id
            ORDER BY ad.date DESC
            LIMIT ?
        """, (config.context_window, query, query, query, query, config.max_results)).fetchall()
        
        if not results:
            return f"No papers found related to '{topic}'. Try different keywords or check available topics with find_research_topics."
        
        output = f"Found {len(results)} papers related to '{topic}':\n\n"
        for title, date, contribution, excerpt in results:
            output += f"**{title}** ({date})\n"
            output += f"Core contribution: {contribution}\n"
            output += f"Excerpt: {excerpt}\n\n"
        
        return output
    finally:
        conn.close()


@tool 
def search_personal_notes(query: str, date_filter: str = None) -> str:
    """
    Search personal chronicle notes by content or date.
    Use date_filter in format 'YYYY-MM' or 'YYYY' to filter by time period.
    """
    config = AgentConfig()
    conn = sqlite3.connect(config.db_path)
    try:
        # Build query based on filters
        params = []
        where_clauses = []
        
        if query:
            where_clauses.append("(cd.content LIKE ? OR cd.title LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        if date_filter:
            where_clauses.append("cd.date LIKE ?")
            params.append(f"{date_filter}%")
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        params.append(config.max_results)
        
        results = conn.execute(f"""
            SELECT cd.title, cd.date, cd.note_type, 
                   substr(cd.content, 1, ?) as excerpt
            FROM chronicle_documents cd
            WHERE {where_clause}
            ORDER BY cd.date DESC
            LIMIT ?
        """, [config.context_window] + params).fetchall()
        
        if not results:
            return f"No personal notes found for query '{query}'" + (f" in {date_filter}" if date_filter else "")
        
        output = f"Found {len(results)} personal notes:\n\n"
        for title, date, note_type, excerpt in results:
            output += f"**{title}** ({date}) - {note_type}\n"
            output += f"{excerpt}\n\n"
        
        return output
    finally:
        conn.close()


@tool
def find_entities_by_type(entity_type: str, name_filter: str = None) -> str:
    """
    Find entities by type: topic, person, method, institution, application, or project.
    Optionally filter by name pattern.
    """
    conn = sqlite3.connect(config.db_path)
    try:
        # Map entity type to table
        type_map = {
            'topic': ('topics', 'name, category, description'),
            'person': ('people', 'name, role, affiliation'),
            'method': ('methods', 'name, category, description'),
            'institution': ('institutions', 'name, type, location'),
            'application': ('applications', 'name, domain, description'),
            'project': ('projects', 'name, description, start_date')
        }
        
        if entity_type not in type_map:
            return f"Unknown entity type '{entity_type}'. Valid types: {', '.join(type_map.keys())}"
        
        table, fields = type_map[entity_type]
        
        # Try semantic search first if available
        if config.use_semantic_search and name_filter:
            entities = find_similar_entities(config.db_path, name_filter, entity_type, limit=10)
            if entities:
                output = f"Found {len(entities)} similar {entity_type}s:\n\n"
                for ent in entities:
                    output += f"• **{ent['name']}**"
                    if ent.get('category'):
                        output += f" (category: {ent['category']})"
                    output += f" - similarity: {ent['similarity']:.2f}\n"
                return output
        
        # Fallback to SQL search
        query = f"SELECT id, {fields} FROM {table}"
        params = []
        
        if name_filter:
            query += " WHERE name LIKE ?"
            params.append(f"%{name_filter}%")
        
        query += f" LIMIT {config.max_results}"
        
        results = conn.execute(query, params).fetchall()
        
        if not results:
            return f"No {entity_type}s found" + (f" matching '{name_filter}'" if name_filter else "")
        
        output = f"Found {len(results)} {entity_type}s:\n\n"
        for row in results:
            # Format based on entity type
            if entity_type == 'topic':
                output += f"• **{row[1]}** (category: {row[2]}): {row[3] or 'No description'}\n"
            elif entity_type == 'person':
                output += f"• **{row[1]}** - {row[2] or 'Unknown role'} at {row[3] or 'Unknown affiliation'}\n"
            elif entity_type == 'method':
                output += f"• **{row[1]}** (category: {row[2]}): {row[3] or 'No description'}\n"
            else:
                output += f"• **{row[1]}** - {', '.join(str(x) for x in row[2:] if x)}\n"
        
        return output
    finally:
        conn.close()


@tool
def get_entity_relationships(entity_name: str, entity_type: str = None, config: AgentConfig = AgentConfig()) -> str:
    """
    Get all relationships for a specific entity.
    Shows what papers discuss it, who uses it, etc.
    """
    conn = sqlite3.connect(config.db_path)
    try:
        # Find the entity
        if entity_type:
            type_map = {
                'topic': 'topics', 'person': 'people', 'method': 'methods',
                'institution': 'institutions', 'application': 'applications', 'project': 'projects'
            }
            if entity_type in type_map:
                table = type_map[entity_type]
                entity = conn.execute(f"SELECT id, name FROM {table} WHERE name LIKE ?", 
                                    (f"%{entity_name}%",)).fetchone()
        else:
            # Search across all entity types
            entity = None
            for table in ['topics', 'people', 'methods', 'institutions', 'applications', 'projects']:
                result = conn.execute(f"SELECT id, name, '{table[:-1]}' as type FROM {table} WHERE name LIKE ?", 
                                    (f"%{entity_name}%",)).fetchone()
                if result:
                    entity = result
                    entity_type = result[2]
                    break
        
        if not entity:
            return f"Entity '{entity_name}' not found" + (f" in {entity_type}s" if entity_type else "")
        
        entity_id, entity_name, entity_type = entity[0], entity[1], entity_type
        
        # Get relationships
        relationships = conn.execute("""
            SELECT r.relationship_type, r.source_type, r.source_id, r.target_type, r.target_id
            FROM relationships r
            WHERE (r.source_id = ? AND r.source_type = ?) 
               OR (r.target_id = ? AND r.target_type = ?)
            LIMIT 50
        """, (entity_id, entity_type, entity_id, entity_type)).fetchall()
        
        if not relationships:
            return f"No relationships found for {entity_type} '{entity_name}'"
        
        output = f"Relationships for {entity_type} **{entity_name}**:\n\n"
        
        # Group by relationship type
        rel_groups = {}
        for rel_type, src_type, src_id, tgt_type, tgt_id in relationships:
            if rel_type not in rel_groups:
                rel_groups[rel_type] = []
            
            # Get the other entity details
            if src_id == entity_id and src_type == entity_type:
                # This entity is the source
                other_type, other_id = tgt_type, tgt_id
                direction = "→"
            else:
                # This entity is the target
                other_type, other_id = src_type, src_id
                direction = "←"
            
            # Get other entity name
            if other_type == 'academic' or other_type == 'academic_document':
                other = conn.execute("SELECT title FROM academic_documents WHERE id = ?", (other_id,)).fetchone()
            elif other_type == 'chronicle' or other_type == 'chronicle_document':
                other = conn.execute("SELECT title FROM chronicle_documents WHERE id = ?", (other_id,)).fetchone()
            else:
                type_table = other_type + 's' if not other_type.endswith('s') else other_type
                other = conn.execute(f"SELECT name FROM {type_table} WHERE id = ?", (other_id,)).fetchone()
            
            if other:
                rel_groups[rel_type].append(f"{direction} {other[0]} ({other_type})")
        
        # Format output
        for rel_type, items in rel_groups.items():
            output += f"**{rel_type}**:\n"
            for item in items[:10]:  # Limit items per relationship type
                output += f"  {item}\n"
            if len(items) > 10:
                output += f"  ... and {len(items) - 10} more\n"
            output += "\n"
        
        return output
    finally:
        conn.close()


@tool
def get_database_statistics() -> str:
    """Get overview statistics about the knowledge base."""
    conn = sqlite3.connect(AgentConfig().db_path)
    try:
        stats = {}
        
        # Document counts
        stats['academic_papers'] = conn.execute("SELECT COUNT(*) FROM academic_documents").fetchone()[0]
        stats['personal_notes'] = conn.execute("SELECT COUNT(*) FROM chronicle_documents").fetchone()[0]
        
        # Entity counts
        for table in ['topics', 'people', 'methods', 'institutions', 'applications', 'projects']:
            stats[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        
        # Relationships and chunks
        stats['relationships'] = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        stats['document_chunks'] = conn.execute("SELECT COUNT(*) FROM document_chunks").fetchone()[0]
        
        # Graph stats
        stats['graph_nodes'] = conn.execute("SELECT COUNT(*) FROM graph_nodes").fetchone()[0]
        stats['graph_edges'] = conn.execute("SELECT COUNT(*) FROM graph_edges").fetchone()[0]
        
        output = "📊 **Interactive CV Database Statistics**\n\n"
        output += "**Documents:**\n"
        output += f"- Academic Papers: {stats['academic_papers']}\n"
        output += f"- Personal Notes: {stats['personal_notes']}\n\n"
        
        output += "**Entities:**\n"
        output += f"- Topics: {stats['topics']}\n"
        output += f"- People: {stats['people']}\n"
        output += f"- Methods: {stats['methods']}\n"
        output += f"- Institutions: {stats['institutions']}\n"
        output += f"- Applications: {stats['applications']}\n"
        output += f"- Projects: {stats['projects']}\n\n"
        
        output += "**Structure:**\n"
        output += f"- Relationships: {stats['relationships']}\n"
        output += f"- Document Chunks: {stats['document_chunks']}\n"
        output += f"- Knowledge Graph Nodes: {stats['graph_nodes']}\n"
        output += f"- Knowledge Graph Edges: {stats['graph_edges']}\n"
        
        return output
    finally:
        conn.close()


# Create the improved agent
class ImprovedInteractiveCVAgent:
    """Improved Interactive CV Agent with better tool implementations."""
    
    def __init__(self, config: AgentConfig = None):
        self.config = config or AgentConfig()
        self.memory = MemorySaver()
        
        # Get model configuration
        if self.config.model_name is None:
            model_key = os.getenv("AGENT_MODEL", "flash")
            models = {
                "flash": "google/gemini-2.5-flash",
                "pro": "google/gemini-2.5-pro"
            }
            self.config.model_name = models.get(model_key, models["flash"])
        
        print(f"🤖 Improved Agent using model: {self.config.model_name}")
        if self.config.use_semantic_search:
            print("✅ Semantic search enabled")
        else:
            print("⚠️  Semantic search not available (using SQL search)")
        
        # Initialize LLM
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
            
        max_tokens = 8192 if "pro" in self.config.model_name else 4096
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            model_kwargs={"max_tokens": max_tokens}
        )
        
        # Tools - pass config to each tool via defaults
        tools = [
            search_papers_by_topic,
            search_personal_notes,
            find_entities_by_type,
            get_entity_relationships,
            get_database_statistics
        ]
        
        # Note: Tools will use their default config parameter
        
        # Create tool node
        self.tool_node = ToolNode(tools)
        
        # Build graph
        self.graph = self._build_graph(tools)
        
    def _build_graph(self, tools) -> CompiledStateGraph:
        """Build the agent graph."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_agent)
        workflow.add_node("tools", self.tool_node)
        
        # Add edges
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _call_agent(self, state: AgentState) -> Dict[str, Any]:
        """Call the agent LLM."""
        messages = state["messages"]
        
        # Add system message if this is the first message
        if len(messages) == 1:
            messages = [SystemMessage(content=ENHANCED_SYSTEM_PROMPT)] + messages
        
        # Get tools for binding
        tools = [
            search_papers_by_topic,
            search_personal_notes,
            find_entities_by_type,
            get_entity_relationships,
            get_database_statistics
        ]
        
        # Bind tools to LLM
        llm_with_tools = self.llm.bind_tools(tools)
        
        # Get response
        response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue to tools or end."""
        last_message = state["messages"][-1]
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"
        return "end"
    
    def chat(self, message: str, thread_id: str = "default") -> str:
        """
        Chat with the agent.
        
        Args:
            message: User message
            thread_id: Conversation thread ID for memory
            
        Returns:
            Agent response
        """
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "context": ""
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        
        result = self.graph.invoke(initial_state, config)
        
        # Extract the final response
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
                return msg.content
        
        return "I couldn't generate a response. Please try again."


def main():
    """Run the improved interactive agent."""
    print("🚀 Interactive CV - Improved Agent")
    print("=" * 50)
    print("Chat with the improved Interactive CV system.")
    print("Type 'exit' to quit, 'stats' for database statistics.")
    print("=" * 50)
    
    agent = ImprovedInteractiveCVAgent()
    
    while True:
        try:
            user_input = input("\n💭 You: ").strip()
            
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'stats':
                print("\n🤖 Assistant:", get_database_statistics())
                continue
            elif not user_input:
                continue
            
            print("\n🤖 Assistant: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()