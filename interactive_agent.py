#!/usr/bin/env python3
"""
Interactive CV Agent - A conversational interface for querying academic research and personal notes.
Uses LangGraph for agent orchestration and OpenRouter for LLM access.
"""

import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# LangChain and LangGraph imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from typing import Any, Dict
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import SecretStr

# Local imports
from RAG.graph_enhanced_query import GraphEnhancedQuery

# Load environment variables
load_dotenv()

# Database path
DB_PATH = "DB/metadata.db"
GRAPH_PATH = "KG/knowledge_graph.json"


class InteractiveCVAgent:
    """Main agent class for interactive CV queries."""
    
    def __init__(self):
        """Initialize the agent with tools and LangGraph configuration."""
        # Don't create connection here due to threading issues
        self.db_path = DB_PATH
        self.graph_query = GraphEnhancedQuery(DB_PATH, GRAPH_PATH)
        
        # Initialize OpenRouter LLM with configurable model
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        
        # Get model configuration
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
                "X-Title": "Interactive CV Agent",
            }
        )
        
        # Print model being used
        print(f"🤖 Agent using model: {model_name}")
        
        # Create tools
        self.tools = self._create_tools()
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Build the agent graph
        self.agent = self._build_agent()
        
    def _create_tools(self):
        """Create all tools for the agent."""
        
        # Capture paths in closure
        db_path = self.db_path
        graph_query = self.graph_query
        
        @tool
        def search_academic_papers(query: str, context_length: int = 1500) -> str:
            """Search for academic papers by topic or keywords. Returns detailed content."""
            conn = None
            try:
                # Create connection in the tool to avoid threading issues
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT d.id, d.title, d.date, d.content
                    FROM academic_documents d
                    LEFT JOIN relationships r ON (d.id = r.source_id AND r.source_type = 'academic_document')
                    LEFT JOIN topics t ON (r.target_id = t.id AND r.target_type = 'topic')
                    WHERE t.name LIKE ? OR d.title LIKE ? OR d.content LIKE ?
                    ORDER BY d.date DESC
                    LIMIT 5
                """, (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = []
                for row in cursor.fetchall():
                    doc_id, title, date, content = row
                    content = content if content else ""
                    
                    # Find the most relevant section containing the query
                    if query.lower() in content.lower():
                        # Find position of query
                        pos = content.lower().find(query.lower())
                        # Extract context around the match
                        start = max(0, pos - context_length//2)
                        end = min(len(content), pos + context_length//2)
                        excerpt = content[start:end]
                    else:
                        # If not found in content, take beginning
                        excerpt = content[:context_length]
                    
                    results.append({
                        'id': doc_id,
                        'title': title,
                        'date': date,
                        'excerpt': excerpt
                    })
                
                if not results:
                    return f"No papers found for query: {query}"
                
                response = f"Found {len(results)} papers related to '{query}':\n\n"
                for i, paper in enumerate(results, 1):
                    response += f"{i}. **{paper['title']}** ({paper['date']})\n"
                    response += f"Relevant excerpt:\n{paper['excerpt']}\n\n"
                    response += "-" * 80 + "\n\n"
                
                conn.close()
                return response
            except Exception as e:
                return f"Error searching academic papers: {str(e)}"
            finally:
                if conn is not None:
                    conn.close()
        
        @tool
        def search_chronicle_notes(query: str, context_length: int = 1000) -> str:
            """Search daily work notes and progress updates."""
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT d.title, d.date, d.content
                    FROM chronicle_documents d
                    WHERE d.content LIKE ? OR d.title LIKE ?
                    ORDER BY d.date DESC
                    LIMIT 10
                """, (f'%{query}%', f'%{query}%'))
                
                results = []
                for row in cursor.fetchall():
                    title, date, content = row
                    content = content if content else ""
                    
                    # Find relevant section
                    if query.lower() in content.lower():
                        pos = content.lower().find(query.lower())
                        start = max(0, pos - context_length//2)
                        end = min(len(content), pos + context_length//2)
                        excerpt = content[start:end]
                    else:
                        excerpt = content[:context_length]
                    
                    results.append({
                        'title': title,
                        'date': date,
                        'excerpt': excerpt
                    })
                
                if not results:
                    return f"No notes found for query: {query}"
                
                response = f"Found {len(results)} notes related to '{query}':\n\n"
                for i, note in enumerate(results, 1):
                    response += f"{i}. **{note['title']}** ({note['date']})\n"
                    response += f"{note['excerpt']}\n\n"
                    response += "-" * 60 + "\n\n"
                
                conn.close()
                return response
            except Exception as e:
                return f"Error searching chronicle notes: {str(e)}"
            finally:
                if conn is not None:
                    conn.close()
        
        @tool
        def find_research_topics(area: str) -> str:
            """Find research topics and expertise areas."""
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT t.name, t.category, COUNT(DISTINCT r.source_id) as doc_count
                    FROM topics t
                    LEFT JOIN relationships r ON (t.id = r.target_id AND r.target_type = 'topic')
                    WHERE t.name LIKE ? OR t.category LIKE ?
                    GROUP BY t.id, t.name, t.category
                    ORDER BY doc_count DESC
                    LIMIT 15
                """, (f'%{area}%', f'%{area}%'))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'topic': row[0],
                        'category': row[1] if row[1] else 'general',
                        'document_count': row[2]
                    })
                
                if not results:
                    return f"No research topics found for area: {area}"
                
                response = f"Found {len(results)} research topics in '{area}':\n\n"
                for topic in results:
                    response += f"• {topic['topic']} ({topic['category']})"
                    response += f" - mentioned in {topic['document_count']} documents\n"
                
                conn.close()
                return response
            except Exception as e:
                return f"Error finding research topics: {str(e)}"
            finally:
                if conn is not None:
                    conn.close()
        
        @tool
        def get_research_evolution(topic: str) -> str:
            """Track how research on a topic evolved over time."""
            evolution = graph_query.find_research_evolution(topic)
            
            if not evolution:
                return f"No research evolution found for topic: {topic}"
            
            response = f"Research evolution for '{topic}':\n\n"
            for entry in evolution[:10]:
                response += f"• {entry['date']}: {entry['title']} ({entry['type']})\n"
                if entry['context']:
                    response += f"  Context: {entry['context'][:150]}...\n"
                response += "\n"
            
            return response
        
        @tool
        def find_project_connections(project_name: str) -> str:
            """Find all connections for a given project."""
            connections = graph_query.find_project_connections(project_name)
            
            if not connections or all(not v for v in connections.values()):
                return f"No connections found for project: {project_name}"
            
            response = f"Connections for project '{project_name}':\n\n"
            
            if connections['topics']:
                response += f"Topics: {', '.join(connections['topics'][:10])}\n"
            if connections['people']:
                response += f"People: {', '.join(connections['people'][:5])}\n"
            if connections['documents']:
                response += f"Documents: {', '.join(connections['documents'][:5])}\n"
            if connections['related_projects']:
                response += f"Related Projects: {', '.join(connections['related_projects'])}\n"
            
            return response
        
        @tool
        def semantic_search_chunks(query: str, top_k: int = 5) -> str:
            """Search through document chunks for detailed content matching the query."""
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Search in document chunks for more complete content
                cursor.execute("""
                    SELECT c.id, c.content, c.document_id, c.document_type,
                           CASE 
                               WHEN c.document_type = 'academic' THEN a.title
                               WHEN c.document_type = 'chronicle' THEN ch.title
                               ELSE 'Unknown'
                           END as title
                    FROM document_chunks c
                    LEFT JOIN academic_documents a ON (c.document_id = a.id AND c.document_type = 'academic')
                    LEFT JOIN chronicle_documents ch ON (c.document_id = ch.id AND c.document_type = 'chronicle')
                    WHERE c.content LIKE ?
                    ORDER BY LENGTH(c.content) DESC
                    LIMIT ?
                """, (f'%{query}%', top_k))
                
                results = []
                for row in cursor.fetchall():
                    chunk_id, content, _, doc_type, title = row
                    results.append({
                        'chunk_id': chunk_id,
                        'content': content if content else '',
                        'document': title,
                        'doc_type': doc_type
                    })
                
                if not results:
                    return f"No relevant content found for: {query}"
                
                response = f"Found {len(results)} relevant passages for '{query}':\n\n"
                for i, result in enumerate(results, 1):
                    response += f"{i}. From **{result['document']}** ({result['doc_type']}):\n\n"
                    response += f"{result['content']}\n\n"
                    response += "=" * 80 + "\n\n"
                
                conn.close()
                return response
            except Exception as e:
                return f"Error in semantic search: {str(e)}"
            finally:
                if conn is not None:
                    conn.close()
        
        @tool
        def get_collaborations() -> str:
            """Find collaboration patterns and key people."""
            patterns = graph_query.find_collaboration_patterns()
            
            if not patterns:
                return "No collaboration patterns found."
            
            response = "Collaboration patterns:\n\n"
            for person, info in sorted(patterns.items(), 
                                     key=lambda x: x[1]['documents'], 
                                     reverse=True)[:10]:
                response += f"• {person}: {info['documents']} documents\n"
                if info['topics']:
                    response += f"  Topics: {', '.join(info['topics'][:5])}\n"
                if info['projects']:
                    response += f"  Projects: {', '.join(info['projects'])}\n"
                response += "\n"
            
            return response
        
        @tool
        def get_paper_content(paper_title: str, section_query: str = "") -> str:
            """Get full or partial content of a specific paper by title."""
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT content 
                    FROM academic_documents 
                    WHERE title LIKE ?
                    LIMIT 1
                """, (f'%{paper_title}%',))
                
                result = cursor.fetchone()
                if not result:
                    return f"No paper found with title containing: {paper_title}"
                
                content = result[0]
                
                if section_query and section_query.strip():
                    # Find section containing the query
                    lines = content.split('\n')
                    relevant_lines = []
                    
                    for i, line in enumerate(lines):
                        if section_query.lower() in line.lower():
                            # Start capturing from 10 lines before
                            start = max(0, i - 10)
                            end = min(len(lines), i + 50)
                            relevant_lines = lines[start:end]
                            break
                    
                    if relevant_lines:
                        return '\n'.join(relevant_lines)
                    else:
                        return f"Section '{section_query}' not found in paper. Returning first 2000 chars:\n\n{content[:2000]}"
                else:
                    # Return first significant portion
                    return content[:3000]
                    
            except Exception as e:
                return f"Error getting paper content: {str(e)}"
            finally:
                if conn is not None:
                    conn.close()
        
        return [
            search_academic_papers,
            get_paper_content,
            search_chronicle_notes,
            find_research_topics,
            get_research_evolution,
            find_project_connections,
            semantic_search_chunks,
            get_collaborations
        ]
    
    def _build_agent(self):
        """Build the LangGraph agent."""
        # Create state graph
        builder = StateGraph(MessagesState)
        
        # Define the agent node
        def agent_node(state: MessagesState):
            """Process messages and decide on tool usage."""
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # Add nodes
        builder.add_node("agent", agent_node)
        tool_node = ToolNode(self.tools)
        builder.add_node("tools", tool_node)
        
        # Add edges
        builder.add_edge(START, "agent")
        builder.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "tools", END: END}
        )
        builder.add_edge("tools", "agent")
        
        # Compile with memory
        memory = InMemorySaver()
        return builder.compile(checkpointer=memory)
    
    def chat(self, user_input: str, thread_id: str = "default"):
        """Process a user message and return response."""
        config: Dict[str, Any] = {"configurable": {"thread_id": thread_id}, "recursion_limit": 32}
        
        # Create system message for context
        system_msg = SystemMessage(content="""You are an Interactive CV system representing Vaios Laschos, an applied mathematician (PhD, University of Bath) who has evolved from pure mathematics to machine learning and AI. Born January 3, 1983, I've spent over a decade in postdoctoral research across four countries (Greece, UK, USA, Germany), building bridges between abstract mathematical theory and practical AI applications.

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
- **search_academic_papers**: Find my papers by topic/keywords (returns 1500+ char excerpts)
- **get_paper_content**: Retrieve full/partial content of specific papers
- **search_chronicle_notes**: Search my daily work logs and progress updates
- **find_research_topics**: Discover research areas with mathematical categorization
- **get_research_evolution**: Track how my work evolved from pure math to AI
- **find_project_connections**: Explore relationships between projects
- **semantic_search_chunks**: Deep content search across all documents
- **get_collaborations**: Find my collaboration patterns and co-authors

## Interaction Guidelines
- Feel free to ask questions in first person - this is YOUR interactive CV!
- I'll search my actual papers and notes to give you specific, accurate answers
- I can compare different aspects of my work, trace intellectual evolution, or dive deep into technical details
- Ask about specific papers, mathematical concepts, ML projects, or my research philosophy
- I speak conversationally but maintain technical accuracy

## My Research Philosophy
I believe the best AI systems emerge when we deeply understand their mathematical underpinnings. I need purpose and meaning in my work - I can't treat it as "just a job." The intersection of mathematical beauty and practical impact is where I thrive.

IMPORTANT: I will ALWAYS search my database first before answering - my responses are grounded in actual data from my papers and notes, not general knowledge.""")
        
        # Process the message
        messages = [system_msg, HumanMessage(content=user_input)]
        
        # Stream the response
        response_content = ""
        for event in self.agent.stream({"messages": messages}, config):  # type: ignore
            if "agent" in event:
                last_message = event["agent"]["messages"][-1]
                if hasattr(last_message, 'content') and last_message.content:
                    response_content = last_message.content
        
        return response_content
    
    def __del__(self):
        """Clean up resources."""
        pass  # No connection to close anymore


def main():
    """Main interactive loop."""
    print("=== Interactive CV Agent ===")
    print("Chat with Vaios's research profile. Type 'exit' to quit.\n")
    
    agent = InteractiveCVAgent()
    thread_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAssistant: ", end="", flush=True)
            response = agent.chat(user_input, thread_id)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()