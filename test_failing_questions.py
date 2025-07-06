#!/usr/bin/env python3
"""
Test the failing questions with the interactive agent to diagnose issues.
"""

import asyncio
import json
from interactive_agent import InteractiveCVAgent

def test_question(agent, question_id, question, expected_answer):
    """Test a single question and return the response."""
    print(f"\n{'='*60}")
    print(f"TESTING Q{question_id}: {question}")
    print(f"{'='*60}")
    
    try:
        # Send the question to the agent
        response = agent.chat(question)
        
        print(f"\nAGENT RESPONSE:")
        print("-" * 40)
        print(response)
        
        print(f"\nEXPECTED ANSWER:")
        print("-" * 40)
        print(expected_answer[:500] + "..." if len(expected_answer) > 500 else expected_answer)
        
        return response
        
    except Exception as e:
        error_msg = f"Error testing Q{question_id}: {str(e)}"
        print(error_msg)
        return error_msg

def main():
    """Test the failing questions."""
    
    # Load the test questions
    with open('tests/qa_test_set.json', 'r') as f:
        data = json.load(f)
    
    failing_ids = [4, 6, 9, 11, 14]
    failing_questions = []
    
    for case in data['test_cases']:
        if case['id'] in failing_ids:
            failing_questions.append(case)
    
    # Initialize the agent
    print("Initializing Interactive Agent...")
    agent = InteractiveCVAgent()
    
    # Test each failing question
    for case in failing_questions:
        test_question(
            agent, 
            case['id'], 
            case['question'], 
            case['expected_answer']
        )
        
        print(f"\n{'='*20} END Q{case['id']} {'='*20}\n")

if __name__ == "__main__":
    main()