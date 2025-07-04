#!/usr/bin/env python3
"""
Test script to verify the interactive agent works.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key exists
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: OPENROUTER_API_KEY not found in .env file")
    print("Please add your API key to .env file")
    exit(1)
else:
    print(f"✓ API key found (length: {len(api_key)})")

# Try to import and initialize the agent
try:
    from interactive_agent import InteractiveCVAgent
    print("✓ Interactive agent module imported successfully")
    
    print("\nInitializing agent...")
    agent = InteractiveCVAgent()
    print("✓ Agent initialized successfully")
    
    # Test a simple query
    print("\nTesting agent with a simple query...")
    response = agent.chat("Hello, can you tell me about Vaios's research?", "test-session")
    print(f"\n✓ Agent response received (length: {len(response)} chars)")
    print(f"First 200 chars: {response[:200]}...")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()