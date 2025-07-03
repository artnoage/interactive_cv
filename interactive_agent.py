#!/usr/bin/env python3
"""
Interactive CV Agent - A conversational agent for exploring Vaios Laschos' research
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import metadata system components
from KG.graph_enhanced_query import GraphEnhancedQuery
from DB.embeddings import EmbeddingGenerator

load_dotenv()


# Database query tools
@tool
def search_academic_papers(
    query: str,
    topic: Optional[str] = None,
    limit: int = 5
) -> str:
    """Search academic papers by query or topic.
    
    Args:
        query: Text to search for in paper titles and content
        topic: Optional specific topic to filter by
        limit: Maximum number of results to return
    """
    db_path = "DB/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if topic:
            cursor.execute("""
                SELECT DISTINCT d.id, d.title, d.date, d.metadata
                FROM documents d
                JOIN document_topics dt ON d.id = dt.document_id
                JOIN topics t ON dt.topic_id = t.id
                WHERE d.doc_type = 'academic' 
                AND (d.title LIKE ? OR t.name LIKE ?)
                ORDER BY d.date DESC
                LIMIT ?
            """, (f'%{query}%', f'%{topic}%', limit))
        else:
            cursor.execute("""
                SELECT d.id, d.title, d.date, d.metadata
                FROM documents d
                WHERE d.doc_type = 'academic' 
                AND d.title LIKE ?
                ORDER BY d.date DESC
                LIMIT ?
            """, (f'%{query}%', limit))
        
        results = cursor.fetchall()
        
        if not results:
            return "No academic papers found matching your query."
        
        papers = []
        for doc_id, title, date, metadata_json in results:
            metadata = json.loads(metadata_json) if metadata_json else {}
            paper_info = f"**{title}**"
            if date and date != "not specified":
                paper_info += f" ({date})"
            
            if metadata.get('core_contributions'):
                contributions = metadata['core_contributions']
                if isinstance(contributions, list):
                    paper_info += f"\n- Key contributions: {', '.join(contributions[:2])}"
                else:
                    paper_info += f"\n- Key contribution: {contributions}"
            
            papers.append(paper_info)
        
        return f"Found {len(papers)} academic papers:\n\n" + "\n\n".join(papers)
        
    finally:
        conn.close()


@tool
def get_paper_details(paper_title: str) -> str:
    """Get detailed information about a specific paper including abstract and key findings.
    
    Args:
        paper_title: Title or partial title of the paper
    """
    db_path = "DB/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT d.id, d.title, d.metadata
            FROM documents d
            WHERE d.doc_type = 'academic' AND d.title LIKE ?
            LIMIT 1
        """, (f'%{paper_title}%',))
        
        result = cursor.fetchone()
        if not result:
            return f"No paper found matching: {paper_title}"
        
        doc_id, title, metadata_json = result
        metadata = json.loads(metadata_json) if metadata_json else {}
        
        details = [f"**{title}**\n"]
        
        if metadata.get('core_contributions'):
            contrib = metadata['core_contributions']
            if isinstance(contrib, list):
                details.append("**Key Contributions:**")
                for c in contrib[:3]:
                    details.append(f"- {c}")
            else:
                details.append(f"**Key Contribution:** {contrib}")
        
        if metadata.get('mathematical_concepts'):
            concepts = metadata['mathematical_concepts']
            if isinstance(concepts, list) and concepts:
                details.append(f"\n**Mathematical Concepts:** {', '.join(concepts[:5])}")
        
        if metadata.get('applications'):
            apps = metadata['applications']
            if isinstance(apps, list) and apps:
                details.append(f"\n**Applications:** {', '.join(apps[:3])}")
        
        cursor.execute("""
            SELECT t.name
            FROM topics t
            JOIN document_topics dt ON t.id = dt.topic_id
            WHERE dt.document_id = ?
            LIMIT 10
        """, (doc_id,))
        
        topics = [row[0] for row in cursor.fetchall()]
        if topics:
            details.append(f"\n**Related Topics:** {', '.join(topics)}")
        
        return "\n".join(details)
        
    finally:
        conn.close()


@tool
def search_chronicle_notes(
    query: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 10
) -> str:
    """Search chronicle notes for daily work and insights.
    
    Args:
        query: Text to search for in notes
        date_from: Optional start date (YYYY-MM-DD)
        date_to: Optional end date (YYYY-MM-DD)
        limit: Maximum number of results
    """
    db_path = "DB/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        sql = """
            SELECT d.title, d.date, d.metadata
            FROM documents d
            WHERE d.doc_type = 'chronicle'
            AND (d.title LIKE ? OR d.metadata LIKE ?)
        """
        params = [f'%{query}%', f'%{query}%']
        
        if date_from:
            sql += " AND d.date >= ?"
            params.append(date_from)
        if date_to:
            sql += " AND d.date <= ?"
            params.append(date_to)
        
        sql += " ORDER BY d.date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        if not results:
            return "No chronicle notes found matching your query."
        
        notes = []
        for title, date, metadata_json in results:
            metadata = json.loads(metadata_json) if metadata_json else {}
            note_info = f"**{title}** ({date})"
            
            if metadata.get('daily_summary') or metadata.get('day_summary'):
                summary = metadata.get('daily_summary') or metadata.get('day_summary')
                note_info += f"\n- Summary: {summary}"
            
            notes.append(note_info)
        
        return f"Found {len(notes)} chronicle notes:\n\n" + "\n\n".join(notes)
        
    finally:
        conn.close()


@tool
def search_chronicle_by_date(
    date: str,
    keyword: Optional[str] = None
) -> str:
    """Search chronicle notes for a specific date.
    
    Args:
        date: Date in YYYY-MM-DD format
        keyword: Optional keyword to search within that day's notes
    """
    db_path = "DB/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if keyword:
            cursor.execute("""
                SELECT d.title, d.metadata
                FROM documents d
                WHERE d.doc_type = 'chronicle' 
                AND d.date = ?
                AND (d.title LIKE ? OR d.metadata LIKE ?)
            """, (date, f'%{keyword}%', f'%{keyword}%'))
        else:
            cursor.execute("""
                SELECT d.title, d.metadata
                FROM documents d
                WHERE d.doc_type = 'chronicle' AND d.date = ?
            """, (date,))
        
        result = cursor.fetchone()
        if not result:
            return f"No chronicle notes found for {date}"
        
        title, metadata_json = result
        metadata = json.loads(metadata_json) if metadata_json else {}
        
        output = [f"**{title}**\n"]
        
        summary = metadata.get('daily_summary') or metadata.get('day_summary')
        if summary:
            output.append(f"**Summary:** {summary}\n")
        
        if metadata.get('project_updates'):
            output.append("**Project Updates:**")
            for proj in metadata['project_updates']:
                if isinstance(proj, dict):
                    name = proj.get('project_name', 'Unknown')
                    work = proj.get('work_completed', 'No details')
                    output.append(f"- **{name}**: {work}")
        
        return "\n".join(output)
        
    finally:
        conn.close()


@tool
def find_research_topics(
    area: Optional[str] = None,
    limit: int = 20
) -> str:
    """Find research topics and areas of expertise.
    
    Args:
        area: Optional area to focus on (e.g., 'optimal transport', 'machine learning')
        limit: Maximum number of topics to return
    """
    db_path = "DB/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if area:
            cursor.execute("""
                SELECT t.name, COUNT(DISTINCT d.id) as doc_count
                FROM topics t
                JOIN document_topics dt ON t.id = dt.topic_id
                JOIN documents d ON dt.document_id = d.id
                WHERE t.name LIKE ?
                GROUP BY t.id
                ORDER BY doc_count DESC
                LIMIT ?
            """, (f'%{area}%', limit))
        else:
            cursor.execute("""
                SELECT t.name, COUNT(DISTINCT d.id) as doc_count
                FROM topics t
                JOIN document_topics dt ON t.id = dt.topic_id
                JOIN documents d ON dt.document_id = d.id
                GROUP BY t.id
                ORDER BY doc_count DESC
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        
        if not results:
            return "No research topics found."
        
        topics_by_count = {}
        for topic, count in results:
            if count not in topics_by_count:
                topics_by_count[count] = []
            topics_by_count[count].append(topic)
        
        output = "Research topics by frequency:\n"
        for count in sorted(topics_by_count.keys(), reverse=True):
            output += f"\n**{count} documents**: {', '.join(topics_by_count[count])}"
        
        return output
        
    finally:
        conn.close()


@tool
def get_research_evolution(topic: str) -> str:
    """Track how research on a specific topic evolved over time.
    
    Args:
        topic: The topic to track (e.g., 'optimal transport', 'reinforcement learning')
    """
    enhancer = GraphEnhancedQuery()
    evolution = enhancer.find_research_evolution(topic)
    
    if not evolution:
        return f"No research evolution found for topic: {topic}"
    
    output = f"Research evolution for '{topic}':\n\n"
    for item in evolution:
        output += f"**{item['date']}** - {item['title']} ({item['type']})\n"
        if item.get('context'):
            context = item['context']
            if isinstance(context, str) and len(context) > 200:
                context = context[:200] + "..."
            output += f"   Context: {context}\n"
        output += "\n"
    
    return output


@tool
def find_project_connections(project_name: str) -> str:
    """Find all connections for a specific project.
    
    Args:
        project_name: Name of the project (e.g., 'Interactive CV', 'Collapsi RL')
    """
    enhancer = GraphEnhancedQuery()
    connections = enhancer.find_project_connections(project_name)
    
    if not connections or all(not v for v in connections.values()):
        return f"No connections found for project: {project_name}"
    
    output = f"Connections for project '{project_name}':\n"
    
    if connections.get('topics'):
        output += f"\n**Topics**: {', '.join(connections['topics'][:10])}"
    if connections.get('people'):
        output += f"\n**Collaborators**: {', '.join(connections['people'])}"
    if connections.get('documents'):
        output += f"\n**Related documents**: {len(connections['documents'])} documents"
    
    return output


@tool
def get_collaborations() -> str:
    """Get information about collaborations and people worked with."""
    enhancer = GraphEnhancedQuery()
    patterns = enhancer.find_collaboration_patterns()
    
    if not patterns:
        return "No collaboration information found."
    
    output = "Collaboration patterns:\n"
    for person, info in patterns.items():
        output += f"\n**{person}**:"
        output += f"\n- Documents: {info['documents']}"
        if info['topics']:
            output += f"\n- Topics: {', '.join(info['topics'][:5])}"
        if info['projects']:
            output += f"\n- Projects: {', '.join(info['projects'])}"
    
    return output


def create_agent():
    """Create the interactive CV agent"""
    
    # Initialize LLM
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")
    
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="google/gemini-2.5-flash",
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Interactive CV Agent",
        },
        temperature=0.1,
    )
    
    # Define tools
    tools = [
        search_academic_papers,
        get_paper_details,
        search_chronicle_notes,
        search_chronicle_by_date,
        find_research_topics,
        get_research_evolution,
        find_project_connections,
        get_collaborations
    ]
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an intelligent assistant helping to explore Vaios Laschos' research and professional journey.

You have access to tools for:
- Searching academic papers and getting their details
- Finding daily chronicle notes and project progress
- Tracking research evolution and connections
- Finding collaborations and research topics

When answering questions:
1. Use the most specific tool for the query
2. For paper topics: use get_paper_details for specific papers
3. For daily work: use search_chronicle_by_date for specific dates
4. Always provide specific information from the tools

Be concise but thorough in your responses."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor


def interactive_chat():
    """Run interactive chat interface"""
    agent = create_agent()
    
    print("=== Interactive CV Agent ===")
    print("Ask questions about Vaios' research and professional journey.")
    print("Type 'exit' to quit.\n")
    
    chat_history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif not user_input:
                continue
            
            # Invoke agent
            result = agent.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            print(f"\nAssistant: {result['output']}")
            
            # Update chat history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=result['output']))
            
            # Keep only last 10 messages
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]
                
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"\nError: {str(e)}")


def test_agent():
    """Test the agent with sample questions"""
    agent = create_agent()
    
    test_questions = [
        "What are Vaios' main research areas?",
        "What papers has he written about optimal transport?",
        "What was accomplished on June 28, 2025?",
        "Tell me about the Interactive CV project"
    ]
    
    print("=== Testing Interactive CV Agent ===\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQ{i}: {question}")
        print("="*80)
        
        try:
            result = agent.invoke({
                "input": question,
                "chat_history": []
            })
            
            print(f"\nAnswer: {result['output']}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\n" + "-"*80)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_agent()
    else:
        interactive_chat()