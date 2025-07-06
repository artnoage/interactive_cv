#!/usr/bin/env python3
"""
Simple Demo of MCP Sequential Thinking

A minimal example showing how to use the MCP client/server.
"""

import asyncio
import os
import sys

# Add the client directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'client'))

from mcp_client import SequentialThinkingClient


async def main():
    """Simple demo of sequential thinking"""
    
    # Configure server command
    server_command = [
        "python", 
        os.path.join(os.path.dirname(__file__), "server", "sequential_thinking_server.py")
    ]
    
    # Create client
    client = SequentialThinkingClient(server_command)
    
    try:
        # Start the client
        await client.start()
        print("🚀 Sequential Thinking MCP Demo")
        print("=" * 40)
        
        # Problem to solve
        problem = "How to learn a new programming language effectively"
        print(f"Problem: {problem}\n")
        
        # Sequential thinking process
        thoughts = [
            "First, I need to identify my learning goals and current skill level",
            "Next, I should choose appropriate learning resources and materials",
            "Then, I need to create a structured learning plan with milestones",
            "I should practice with hands-on projects and exercises",
            "Finally, I need to seek feedback and continuously improve"
        ]
        
        for i, thought in enumerate(thoughts, 1):
            is_last = (i == len(thoughts))
            
            result = await client.think(
                thought,
                next_thought_needed=not is_last,
                total_thoughts=len(thoughts)
            )
            
            # Display the result
            if "content" in result:
                print(result["content"][0]["text"])
            else:
                print(f"Error: {result}")
        
        print("\n🎉 Sequential thinking complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())