#!/usr/bin/env python3
"""
Demo Runner for MCP Sequential Thinking Experiment

Run this script to test the MCP client/server implementation.
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

from client.mcp_client import SequentialThinkingClient
from examples.thinking_agent import ThinkingAgent


async def test_basic_client():
    """Test basic MCP client functionality"""
    
    print("🧪 Testing Basic MCP Client")
    print("=" * 50)
    
    server_command = [
        "python", 
        os.path.join(os.path.dirname(__file__), "server", "sequential_thinking_server.py")
    ]
    
    client = SequentialThinkingClient(server_command)
    
    try:
        await client.start()
        
        # Test a simple thinking sequence
        problem = "How to make a good cup of coffee"
        
        print(f"Problem: {problem}")
        print("-" * 30)
        
        # Step 1
        result = await client.think(
            "First, I need to consider the quality of coffee beans",
            next_thought_needed=True,
            total_thoughts=4
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Step 2
        result = await client.think(
            "Next, I should think about the brewing method and water temperature",
            next_thought_needed=True,
            total_thoughts=4
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Step 3
        result = await client.think(
            "I also need to consider the grind size and brewing time",
            next_thought_needed=True,
            total_thoughts=4
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Final step
        result = await client.think(
            "Finally, I should think about the coffee-to-water ratio for optimal taste",
            next_thought_needed=False,
            total_thoughts=4
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        print("\n✅ Basic client test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in basic client test: {e}")
        return False
    
    finally:
        await client.stop()
    
    return True


async def test_branching():
    """Test branching functionality"""
    
    print("\n🌿 Testing Branching Functionality")
    print("=" * 50)
    
    server_command = [
        "python", 
        os.path.join(os.path.dirname(__file__), "server", "sequential_thinking_server.py")
    ]
    
    client = SequentialThinkingClient(server_command)
    
    try:
        await client.start()
        
        # Main thinking sequence
        result = await client.think(
            "I need to choose between two career paths",
            next_thought_needed=True,
            total_thoughts=3
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        result = await client.think(
            "Option A: Continue in academia with research focus",
            next_thought_needed=True,
            total_thoughts=3
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Branch to explore alternative
        result = await client.think(
            "Let me explore the industry option instead",
            next_thought_needed=True,
            total_thoughts=2,
            branch_from_thought=2,
            branch_id="industry_path"
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        result = await client.think(
            "Industry offers faster career progression and higher compensation",
            next_thought_needed=False,
            total_thoughts=2,
            branch_id="industry_path"
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        print("\n✅ Branching test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in branching test: {e}")
        return False
    
    finally:
        await client.stop()
    
    return True


async def test_revision():
    """Test revision functionality"""
    
    print("\n✏️ Testing Revision Functionality")
    print("=" * 50)
    
    server_command = [
        "python", 
        os.path.join(os.path.dirname(__file__), "server", "sequential_thinking_server.py")
    ]
    
    client = SequentialThinkingClient(server_command)
    
    try:
        await client.start()
        
        # Initial thoughts
        result = await client.think(
            "I think the solution is to use a simple linear approach",
            next_thought_needed=True,
            total_thoughts=3
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        result = await client.think(
            "This approach should work for most cases",
            next_thought_needed=True,
            total_thoughts=3
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        # Revise the first thought
        result = await client.think(
            "Actually, upon reflection, a more sophisticated algorithm would be better",
            next_thought_needed=False,
            total_thoughts=3,
            is_revision=True,
            revises_thought=1
        )
        print(result.get("content", [{}])[0].get("text", ""))
        
        print("\n✅ Revision test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in revision test: {e}")
        return False
    
    finally:
        await client.stop()
    
    return True


async def test_thinking_agent():
    """Test the thinking agent"""
    
    print("\n🤖 Testing Thinking Agent")
    print("=" * 50)
    
    server_command = [
        "python", 
        os.path.join(os.path.dirname(__file__), "server", "sequential_thinking_server.py")
    ]
    
    agent = ThinkingAgent(server_command)
    
    try:
        await agent.start()
        
        # Test with a simple problem
        await agent.solve_problem(
            "Design a simple mobile app for task management",
            max_thoughts=5
        )
        
        print("\n✅ Thinking agent test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in thinking agent test: {e}")
        return False
    
    finally:
        await agent.stop()
    
    return True


async def main():
    """Run all tests"""
    
    print("🚀 MCP Sequential Thinking Experiment Demo")
    print("=" * 60)
    
    tests = [
        ("Basic Client", test_basic_client),
        ("Branching", test_branching),
        ("Revision", test_revision),
        ("Thinking Agent", test_thinking_agent)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test")
        print("=" * 30)
        
        try:
            success = await test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! MCP implementation is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    asyncio.run(main())