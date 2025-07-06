#!/usr/bin/env python3
"""
Sequential Reasoning Agent

A specialized agent that uses MCP Sequential Thinking to provide structured,
step-by-step reasoning for complex queries. This agent is designed to be called
by the main interactive agent when deep analytical thinking is needed.
"""

import os
import sys
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Add MCP subfolder to path
mcp_path = project_root / "mcp_subfolder"
sys.path.append(str(mcp_path))

from client.mcp_client import SequentialThinkingClient


class SequentialReasoningAgent:
    """Agent that provides structured reasoning using MCP Sequential Thinking."""
    
    def __init__(self):
        self.client = None
        self.server_command = ["python", str(mcp_path / "server" / "sequential_thinking_server.py")]
        self.is_running = False
    
    async def start(self):
        """Start the MCP sequential thinking server."""
        if self.is_running:
            return
        
        try:
            self.client = SequentialThinkingClient(self.server_command)
            await self.client.start()
            self.is_running = True
        except Exception as e:
            raise RuntimeError(f"Failed to start sequential thinking server: {e}")
    
    async def stop(self):
        """Stop the MCP sequential thinking server."""
        if self.client and self.is_running:
            await self.client.stop()
            self.is_running = False
    
    async def reason_sequentially(self, 
                                problem: str, 
                                domain: str = "general",
                                max_steps: int = 7) -> str:
        """
        Perform sequential reasoning on a complex problem.
        
        Args:
            problem: The problem or question to analyze
            domain: Domain context (general, technical, mathematical, research)
            max_steps: Maximum number of reasoning steps
            
        Returns:
            Structured reasoning result with step-by-step analysis
        """
        if not self.is_running:
            await self.start()
        
        try:
            # Step 1: Initial problem analysis  
            result = await self.client.think(
                f"Analyzing the {domain} problem: {problem}",
                next_thought_needed=True,
                total_thoughts=max_steps
            )
            
            thoughts = [result]
            
            # Continue sequential thinking until completion
            for step in range(2, max_steps + 1):
                if not result.get("next_thought_needed", False):
                    break
                
                # Generate next thought based on previous analysis
                next_thought = self._generate_next_thought(thoughts, problem, domain, step)
                
                result = await self.client.think(
                    next_thought,
                    next_thought_needed=(step < max_steps),
                    total_thoughts=max_steps
                )
                
                thoughts.append(result)
            
            # Format the complete reasoning chain
            return self._format_reasoning_result(thoughts, problem)
            
        except Exception as e:
            return f"Error in sequential reasoning: {str(e)}"
    
    def _generate_next_thought(self, 
                             previous_thoughts: List[Dict],
                             problem: str,
                             domain: str,
                             step: int) -> str:
        """Generate the next thought in the reasoning chain."""
        
        if step == 2:
            return f"Breaking down the key components and relationships in this {domain} problem"
        elif step == 3:
            return "Identifying the core concepts and connections that need to be analyzed"
        elif step == 4:
            return "Evaluating the available information and identifying any gaps"
        elif step == 5:
            return "Developing a structured approach to address the problem"
        elif step == 6:
            return "Synthesizing insights and drawing connections"
        else:
            return "Finalizing the analysis and providing a comprehensive conclusion"
    
    def _format_reasoning_result(self, 
                               thoughts: List[Dict],
                               problem: str) -> str:
        """Format the complete reasoning chain into a readable result."""
        
        result = [f"Sequential Reasoning Analysis for: {problem}"]
        result.append("=" * 60)
        result.append("")
        
        for i, thought in enumerate(thoughts, 1):
            # Extract content from MCP response format
            if isinstance(thought, dict) and 'content' in thought:
                # Handle list of content blocks
                if isinstance(thought['content'], list):
                    content_text = ""
                    for block in thought['content']:
                        if isinstance(block, dict) and 'text' in block:
                            content_text += block['text']
                        elif isinstance(block, str):
                            content_text += block
                    result.append(f"Step {i}: {content_text}")
                else:
                    result.append(f"Step {i}: {thought['content']}")
            else:
                result.append(f"Step {i}: {str(thought)}")
            
            result.append("")
        
        # Add summary if available
        if thoughts:
            last_thought = thoughts[-1]
            if last_thought.get('is_complete'):
                result.append("Summary:")
                result.append(f"The sequential reasoning process completed with {len(thoughts)} steps.")
                result.append("Key insights and conclusions have been integrated above.")
        
        return "\n".join(result)
    
    async def reason_with_alternatives(self, 
                                     problem: str,
                                     domain: str = "general") -> str:
        """
        Perform reasoning with alternative approaches exploration.
        
        Args:
            problem: The problem to analyze
            domain: Domain context
            
        Returns:
            Reasoning result with alternative approaches
        """
        if not self.is_running:
            await self.start()
        
        try:
            # Main reasoning path
            main_result = await self.client.think(
                f"Primary approach to analyzing: {problem}",
                next_thought_needed=True,
                total_thoughts=5,
                domain=domain
            )
            
            # Continue main path
            main_thoughts = [main_result]
            for step in range(2, 4):
                next_thought = f"Continuing primary analysis - step {step}"
                result = await self.client.think(
                    next_thought,
                    next_thought_needed=(step < 3),
                    total_thoughts=5,
                    domain=domain
                )
                main_thoughts.append(result)
            
            # Branch to explore alternative
            alt_result = await self.client.think(
                f"Alternative approach to analyzing: {problem}",
                branch_from_thought=1,
                branch_id="alternative_1",
                total_thoughts=3,
                domain=domain
            )
            
            alt_thoughts = [alt_result]
            
            # Continue alternative path
            for step in range(2, 4):
                next_thought = f"Continuing alternative analysis - step {step}"
                result = await self.client.think(
                    next_thought,
                    branch_id="alternative_1", 
                    next_thought_needed=(step < 3),
                    total_thoughts=3
                )
                alt_thoughts.append(result)
            
            # Format results
            return self._format_alternative_result(main_thoughts, alt_thoughts, problem)
            
        except Exception as e:
            return f"Error in alternative reasoning: {str(e)}"
    
    def _format_alternative_result(self, 
                                 main_thoughts: List[Dict],
                                 alt_thoughts: List[Dict],
                                 problem: str) -> str:
        """Format reasoning result with alternatives."""
        
        result = [f"Multi-Path Reasoning Analysis for: {problem}"]
        result.append("=" * 60)
        result.append("")
        
        result.append("PRIMARY APPROACH:")
        result.append("-" * 20)
        for i, thought in enumerate(main_thoughts, 1):
            result.append(f"Step {i}: {thought.get('content', 'No content')}")
        
        result.append("")
        result.append("ALTERNATIVE APPROACH:")
        result.append("-" * 20)
        for i, thought in enumerate(alt_thoughts, 1):
            result.append(f"Alt {i}: {thought.get('content', 'No content')}")
        
        result.append("")
        result.append("SYNTHESIS:")
        result.append("Both approaches provide complementary insights for a comprehensive understanding.")
        
        return "\n".join(result)


# Synchronous wrapper for use in non-async contexts
class SequentialReasoningSync:
    """Synchronous wrapper for SequentialReasoningAgent."""
    
    def __init__(self):
        self.agent = SequentialReasoningAgent()
        self.loop = None
    
    def reason(self, problem: str, domain: str = "general", max_steps: int = 7) -> str:
        """Synchronous reasoning interface."""
        return self._run_async(self.agent.reason_sequentially(problem, domain, max_steps))
    
    def reason_alternatives(self, problem: str, domain: str = "general") -> str:
        """Synchronous alternative reasoning interface."""
        return self._run_async(self.agent.reason_with_alternatives(problem, domain))
    
    def _run_async(self, coro):
        """Run async coroutine in sync context."""
        try:
            # Always use asyncio.run for clean subprocess management
            return asyncio.run(self._run_with_cleanup(coro))
        except Exception as e:
            return f"Error in async execution: {str(e)}"
    
    async def _run_with_cleanup(self, coro):
        """Run coroutine with proper cleanup."""
        try:
            result = await coro
            return result
        finally:
            # Ensure cleanup happens
            if self.agent.is_running:
                try:
                    await self.agent.stop()
                except:
                    pass
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        # Don't try to run async cleanup in __del__ as it can cause loop issues
        pass


def main():
    """Test the sequential reasoning agent."""
    print("Sequential Reasoning Agent - Testing")
    print("=" * 40)
    
    agent = SequentialReasoningSync()
    
    # Test basic reasoning
    problem = "How does theoretical mathematics connect to practical game development?"
    print(f"Problem: {problem}\n")
    
    result = agent.reason(problem, domain="research", max_steps=5)
    print(result)
    
    print("\n" + "=" * 40)
    print("Testing alternative approaches:")
    
    alt_result = agent.reason_alternatives(problem, domain="research")
    print(alt_result)


if __name__ == "__main__":
    main()