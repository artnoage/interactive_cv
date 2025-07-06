#!/usr/bin/env python3
"""
Thinking Agent Example

An agent that uses sequential thinking to solve complex problems.
"""

import asyncio
import sys
import os
from typing import Dict, List, Optional
import logging

# Add the client directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'client'))

from mcp_client import SequentialThinkingClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ThinkingAgent:
    """An agent that uses sequential thinking to solve problems"""
    
    def __init__(self, server_command: List[str]):
        self.client = SequentialThinkingClient(server_command)
        self.thinking_sessions = {}
    
    async def start(self):
        """Start the agent"""
        await self.client.start()
        logger.info("Thinking agent started")
    
    async def solve_problem(self, problem: str, max_thoughts: int = 10) -> Dict:
        """Solve a problem using sequential thinking"""
        
        print(f"\n🤔 Problem: {problem}")
        print("=" * 80)
        
        # Start with problem analysis
        result = await self.client.think(
            f"Let me analyze this problem: {problem}",
            next_thought_needed=True,
            total_thoughts=max_thoughts
        )
        
        self._display_thought_result(result)
        
        # Continue thinking until we have a solution
        thoughts_count = 1
        while thoughts_count < max_thoughts:
            # Get next thought based on current progress
            next_thought = self._generate_next_thought(thoughts_count, problem)
            
            is_final = (thoughts_count == max_thoughts - 1)
            
            result = await self.client.think(
                next_thought,
                next_thought_needed=not is_final,
                total_thoughts=max_thoughts
            )
            
            self._display_thought_result(result)
            
            thoughts_count += 1
            
            # Check if we should stop early
            if self._should_stop_thinking(result):
                break
        
        return {"status": "complete", "thoughts": thoughts_count}
    
    def _generate_next_thought(self, thought_number: int, problem: str) -> str:
        """Generate the next thought based on the current progress"""
        
        # This is a simple heuristic - in a real implementation, this could be
        # more sophisticated, potentially using an LLM to generate the next thought
        
        if "marketing" in problem.lower():
            marketing_thoughts = [
                "I need to identify the target audience and their pain points",
                "I should analyze the competitive landscape and market positioning",
                "I need to define the unique value proposition and key messaging",
                "I should determine the most effective marketing channels",
                "I need to create a budget and timeline for execution",
                "I should plan how to measure success and ROI",
                "I need to consider potential risks and mitigation strategies"
            ]
            if thought_number < len(marketing_thoughts):
                return marketing_thoughts[thought_number]
        
        elif "technical" in problem.lower() or "software" in problem.lower():
            technical_thoughts = [
                "I need to understand the technical requirements and constraints",
                "I should analyze the system architecture and design patterns",
                "I need to identify potential technical risks and challenges",
                "I should plan the implementation approach and timeline",
                "I need to consider testing and quality assurance strategies",
                "I should think about deployment and maintenance requirements"
            ]
            if thought_number < len(technical_thoughts):
                return technical_thoughts[thought_number]
        
        elif "business" in problem.lower():
            business_thoughts = [
                "I need to understand the business context and objectives",
                "I should analyze the market opportunity and competitive landscape",
                "I need to consider the financial implications and ROI",
                "I should identify key stakeholders and their requirements",
                "I need to think about implementation challenges and timeline",
                "I should consider potential risks and mitigation strategies"
            ]
            if thought_number < len(business_thoughts):
                return business_thoughts[thought_number]
        
        # Generic thoughts for other problems
        generic_thoughts = [
            "I need to break down this problem into smaller components",
            "I should consider different approaches and alternatives",
            "I need to evaluate the pros and cons of each option",
            "I should think about implementation steps and timeline",
            "I need to consider potential obstacles and solutions",
            "I should synthesize my thinking into a coherent solution"
        ]
        
        if thought_number < len(generic_thoughts):
            return generic_thoughts[thought_number]
        
        return f"Let me continue analyzing and refining my approach to solve this problem"
    
    def _display_thought_result(self, result: Dict):
        """Display the result of a thought"""
        if "content" in result and result["content"]:
            content = result["content"][0].get("text", "")
            print(content)
        elif "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("❌ Unexpected response format")
    
    def _should_stop_thinking(self, result: Dict) -> bool:
        """Determine if we should stop thinking based on the result"""
        if "content" in result and result["content"]:
            content = result["content"][0].get("text", "")
            # Look for completion indicators
            if "complete" in content.lower() or "final" in content.lower():
                return True
        return False
    
    async def explore_alternative_solution(self, problem: str, branch_from: int = 2) -> Dict:
        """Explore an alternative solution path"""
        
        print(f"\n🔄 Exploring alternative approach for: {problem}")
        print("=" * 80)
        
        # Branch from an earlier thought
        result = await self.client.think(
            "Let me explore a different approach to this problem",
            next_thought_needed=True,
            total_thoughts=5,
            branch_from_thought=branch_from,
            branch_id="alternative_1"
        )
        
        self._display_thought_result(result)
        
        # Continue with alternative thoughts
        for i in range(3):
            result = await self.client.think(
                f"Alternative approach - step {i+2}: considering different strategies",
                next_thought_needed=(i < 2),
                total_thoughts=5,
                branch_id="alternative_1"
            )
            self._display_thought_result(result)
        
        return {"status": "alternative_complete"}
    
    async def revise_thinking(self, thought_to_revise: int, new_thought: str) -> Dict:
        """Revise a previous thought"""
        
        print(f"\n✏️ Revising thought {thought_to_revise}")
        print("=" * 80)
        
        result = await self.client.think(
            new_thought,
            next_thought_needed=False,
            total_thoughts=self.client.total_thoughts_estimate,
            is_revision=True,
            revises_thought=thought_to_revise
        )
        
        self._display_thought_result(result)
        
        return {"status": "revision_complete"}
    
    async def stop(self):
        """Stop the agent"""
        await self.client.stop()
        logger.info("Thinking agent stopped")


async def demo_marketing_problem():
    """Demo: Marketing strategy problem"""
    
    server_command = [
        "python", 
        "/home/artnoage/Projects/interactive_cv/mcp_experiment/server/sequential_thinking_server.py"
    ]
    
    agent = ThinkingAgent(server_command)
    
    try:
        await agent.start()
        
        # Solve marketing problem
        await agent.solve_problem(
            "Develop a comprehensive marketing strategy for launching a new AI-powered productivity app",
            max_thoughts=7
        )
        
        # Explore alternative approach
        await agent.explore_alternative_solution(
            "Develop a comprehensive marketing strategy for launching a new AI-powered productivity app",
            branch_from=3
        )
        
        # Revise a thought
        await agent.revise_thinking(
            thought_to_revise=2,
            new_thought="On second thought, I should also consider the regulatory landscape and data privacy requirements for AI products"
        )
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
    
    finally:
        await agent.stop()


async def demo_technical_problem():
    """Demo: Technical architecture problem"""
    
    server_command = [
        "python", 
        "/home/artnoage/Projects/interactive_cv/mcp_experiment/server/sequential_thinking_server.py"
    ]
    
    agent = ThinkingAgent(server_command)
    
    try:
        await agent.start()
        
        await agent.solve_problem(
            "Design a scalable technical architecture for a real-time collaborative document editing system",
            max_thoughts=6
        )
        
    except Exception as e:
        logger.error(f"Error in technical demo: {e}")
    
    finally:
        await agent.stop()


async def demo_business_problem():
    """Demo: Business strategy problem"""
    
    server_command = [
        "python", 
        "/home/artnoage/Projects/interactive_cv/mcp_experiment/server/sequential_thinking_server.py"
    ]
    
    agent = ThinkingAgent(server_command)
    
    try:
        await agent.start()
        
        await agent.solve_problem(
            "Develop a business strategy for expanding into international markets",
            max_thoughts=8
        )
        
    except Exception as e:
        logger.error(f"Error in business demo: {e}")
    
    finally:
        await agent.stop()


async def main():
    """Main demo function"""
    
    print("🚀 Sequential Thinking Agent Demo")
    print("=" * 50)
    
    demos = [
        ("Marketing Strategy", demo_marketing_problem),
        ("Technical Architecture", demo_technical_problem),
        ("Business Strategy", demo_business_problem)
    ]
    
    for name, demo_func in demos:
        print(f"\n🎯 Running {name} Demo")
        print("=" * 50)
        
        try:
            await demo_func()
        except Exception as e:
            logger.error(f"Error in {name} demo: {e}")
        
        print(f"\n✅ {name} Demo Complete")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())