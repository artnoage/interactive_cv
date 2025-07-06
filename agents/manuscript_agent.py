#!/usr/bin/env python3
"""
Manuscript Reading Agent

A specialized agent that can read and analyze original manuscript files
to answer specific questions. This agent is designed to be called by the
main interactive agent when deep manuscript analysis is needed.
"""

import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


@tool
def list_manuscripts() -> str:
    """List all available manuscript files in the academic directory."""
    academic_dir = project_root / "academic"
    transcript_dir = project_root / "raw_data" / "academic" / "Transcript_MDs"
    
    manuscripts = []
    
    # Check academic directory for original manuscripts
    if academic_dir.exists():
        for file_path in academic_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.tex', '.md', '.docx', '.doc', '.txt']:
                manuscripts.append(f"Original: {file_path.relative_to(academic_dir)}")
    
    # Check transcript directory for processed manuscripts
    if transcript_dir.exists():
        for file_path in transcript_dir.rglob("*.md"):
            if file_path.is_file():
                manuscripts.append(f"Transcript: {file_path.name}")
    
    if not manuscripts:
        return "No manuscript files found. Original manuscripts should be placed in 'academic/' directory."
    
    return "Available manuscripts:\n" + "\n".join(manuscripts)


@tool
def read_manuscript(manuscript_name: str) -> str:
    """Read the content of a specific manuscript file."""
    academic_dir = project_root / "academic"
    transcript_dir = project_root / "raw_data" / "academic" / "Transcript_MDs"
    
    # Try to find the manuscript
    manuscript_path = None
    
    # Check if it's a transcript file
    if manuscript_name.startswith("Transcript:"):
        file_name = manuscript_name.replace("Transcript:", "").strip()
        potential_path = transcript_dir / file_name
        if potential_path.exists():
            manuscript_path = potential_path
    
    # Check if it's an original file
    elif manuscript_name.startswith("Original:"):
        file_name = manuscript_name.replace("Original:", "").strip()
        potential_path = academic_dir / file_name
        if potential_path.exists():
            manuscript_path = potential_path
    
    # Try direct file lookup
    else:
        # First try transcript directory
        potential_path = transcript_dir / manuscript_name
        if potential_path.exists():
            manuscript_path = potential_path
        else:
            # Try academic directory
            potential_path = academic_dir / manuscript_name
            if potential_path.exists():
                manuscript_path = potential_path
    
    if not manuscript_path:
        return f"Manuscript '{manuscript_name}' not found. Use list_manuscripts() to see available files."
    
    try:
        with open(manuscript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if too long (keep first 20000 characters)
        if len(content) > 20000:
            content = content[:20000] + "\n\n[Content truncated for length...]"
        
        return f"Content of {manuscript_name}:\n\n{content}"
    
    except Exception as e:
        return f"Error reading manuscript '{manuscript_name}': {str(e)}"


@tool
def search_manuscript_content(manuscript_name: str, search_query: str) -> str:
    """Search for specific content within a manuscript."""
    content = read_manuscript(manuscript_name)
    
    if "Error reading" in content or "not found" in content:
        return content
    
    # Simple keyword search
    lines = content.split('\n')
    matching_lines = []
    
    for i, line in enumerate(lines):
        if search_query.lower() in line.lower():
            # Add context (previous and next lines)
            start_idx = max(0, i-2)
            end_idx = min(len(lines), i+3)
            context = lines[start_idx:end_idx]
            matching_lines.append(f"Line {i+1}: {' '.join(context)}")
    
    if not matching_lines:
        return f"No matches found for '{search_query}' in {manuscript_name}"
    
    return f"Search results for '{search_query}' in {manuscript_name}:\n\n" + "\n\n".join(matching_lines[:10])


class ManuscriptAgent:
    """Agent specialized in reading and analyzing manuscript files."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model = ChatOpenAI(model=model_name, temperature=0)
        self.tools = [list_manuscripts, read_manuscript, search_manuscript_content]
        
        # Create the agent prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a specialized manuscript reading agent. Your role is to:

1. Read and analyze original manuscript files
2. Answer specific questions about manuscript content
3. Search for relevant information within manuscripts
4. Provide detailed, accurate responses based on the manuscript content

Available tools:
- list_manuscripts(): See all available manuscript files
- read_manuscript(name): Read full content of a specific manuscript
- search_manuscript_content(name, query): Search for specific content within a manuscript

When answering questions:
- Be precise and cite specific parts of the manuscript
- If you can't find relevant information, say so clearly
- Focus on the specific question asked
- Provide context from the manuscript when helpful

Remember: You are called by the main agent when deep manuscript analysis is needed."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # Create the agent
        self.agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)
    
    def answer_question(self, question: str) -> str:
        """Answer a specific question about manuscript content."""
        try:
            result = self.agent_executor.invoke({"input": question})
            return result["output"]
        except Exception as e:
            return f"Error processing question: {str(e)}"


def main():
    """Test the manuscript agent directly."""
    agent = ManuscriptAgent()
    
    print("Manuscript Agent - Testing Interface")
    print("=" * 50)
    
    # Test listing manuscripts
    print("Available manuscripts:")
    print(agent.answer_question("What manuscripts are available?"))
    print()
    
    # Interactive mode
    while True:
        question = input("\nEnter a question about the manuscripts (or 'quit' to exit): ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        answer = agent.answer_question(question)
        print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()