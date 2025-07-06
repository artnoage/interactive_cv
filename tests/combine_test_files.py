#!/usr/bin/env python3
"""
Test File Integration Script

This script provides utilities to combine, merge, and analyze the test files:
- qa_test_set.json: Main test file with 35 questions (IDs 1-35)
- questions_chunk_*.json: 8 chunk files with 5 questions each (IDs 1-40)
- answers_chunk_*.json: 8 chunk files with 5 answers each (IDs 1-40)

The chunk files contain:
- IDs 1-35: Same questions as main test file
- IDs 36-40: Additional questions from chunk 8 (profile-related)
"""

import json
import os
from pathlib import Path

def load_main_test_file(test_dir="tests"):
    """Load the main qa_test_set.json file."""
    main_file = Path(test_dir) / "qa_test_set.json"
    with open(main_file, 'r') as f:
        return json.load(f)

def load_chunk_files(test_dir="tests"):
    """Load all chunk files and return combined questions and answers."""
    questions = {}
    answers = {}
    
    for i in range(1, 9):
        # Load questions
        q_file = Path(test_dir) / f"questions_chunk_{i}.json"
        with open(q_file, 'r') as f:
            q_data = json.load(f)
        
        for question in q_data['questions']:
            questions[question['id']] = question
        
        # Load answers
        a_file = Path(test_dir) / f"answers_chunk_{i}.json"
        with open(a_file, 'r') as f:
            a_data = json.load(f)
        
        for answer in a_data['answers']:
            answers[answer['id']] = answer
    
    return questions, answers

def create_extended_test_set(output_file="tests/qa_extended_test_set.json"):
    """Create an extended test set that includes all 40 questions."""
    print("Creating extended test set...")
    
    # Load main test file
    main_data = load_main_test_file()
    
    # Load chunk files
    chunk_questions, chunk_answers = load_chunk_files()
    
    # Create extended test cases
    extended_test_cases = []
    
    # Add all questions from chunks (including the additional ones)
    for i in range(1, 41):  # IDs 1-40
        if i in chunk_questions and i in chunk_answers:
            question = chunk_questions[i]
            answer = chunk_answers[i]
            
            test_case = {
                "id": i,
                "question": question['question'],
                "expected_answer": answer['expected_answer'],
                "category": question['category'],
                "difficulty": question['difficulty']
            }
            
            # Add source if available
            if 'source' in question:
                test_case['source'] = question['source']
            
            extended_test_cases.append(test_case)
    
    # Create extended metadata
    categories = {}
    difficulties = {}
    sources = set()
    
    for case in extended_test_cases:
        # Count categories
        cat = case['category']
        categories[cat] = categories.get(cat, 0) + 1
        
        # Count difficulties
        diff = case['difficulty']
        difficulties[diff] = difficulties.get(diff, 0) + 1
        
        # Collect sources
        if 'source' in case:
            sources.add(case['source'])
    
    extended_data = {
        "test_cases": extended_test_cases,
        "metadata": {
            "created_date": "2025-07-06",
            "total_questions": len(extended_test_cases),
            "categories": categories,
            "difficulty_distribution": difficulties,
            "sources": sorted(list(sources)),
            "notes": "Extended test set combining qa_test_set.json (IDs 1-35) with additional questions from chunk 8 (IDs 36-40). Includes profile-related questions for comprehensive testing."
        }
    }
    
    # Save extended test set
    with open(output_file, 'w') as f:
        json.dump(extended_data, f, indent=2)
    
    print(f"Extended test set saved to {output_file}")
    print(f"Total questions: {len(extended_test_cases)}")
    print(f"Categories: {categories}")
    print(f"Difficulties: {difficulties}")
    return extended_data

def analyze_differences():
    """Analyze differences between main test file and chunks."""
    print("Analyzing differences between main test file and chunks...")
    
    # Load main test file
    main_data = load_main_test_file()
    main_cases = {case['id']: case for case in main_data['test_cases']}
    
    # Load chunk files
    chunk_questions, chunk_answers = load_chunk_files()
    
    print(f"Main test file: {len(main_cases)} questions (IDs 1-35)")
    print(f"Chunk files: {len(chunk_questions)} questions (IDs 1-40)")
    
    # Find additional questions in chunks
    additional_questions = []
    for i in range(36, 41):
        if i in chunk_questions and i in chunk_answers:
            additional_questions.append(i)
    
    print(f"Additional questions in chunks: {additional_questions}")
    
    # Check for differences in overlapping questions (1-35)
    differences = []
    for i in range(1, 36):
        if i in main_cases and i in chunk_questions:
            main_q = main_cases[i]['question']
            chunk_q = chunk_questions[i]['question']
            
            if main_q != chunk_q:
                differences.append(i)
    
    if differences:
        print(f"Questions with differences: {differences}")
    else:
        print("No differences found in overlapping questions (IDs 1-35)")
    
    return {
        'main_count': len(main_cases),
        'chunk_count': len(chunk_questions),
        'additional_questions': additional_questions,
        'differences': differences
    }

def extract_additional_questions(output_file="tests/additional_questions.json"):
    """Extract only the additional questions (IDs 36-40) from chunk 8."""
    print("Extracting additional questions from chunk 8...")
    
    # Load chunk files
    chunk_questions, chunk_answers = load_chunk_files()
    
    # Extract additional questions
    additional_test_cases = []
    for i in range(36, 41):
        if i in chunk_questions and i in chunk_answers:
            question = chunk_questions[i]
            answer = chunk_answers[i]
            
            test_case = {
                "id": i,
                "question": question['question'],
                "expected_answer": answer['expected_answer'],
                "category": question['category'],
                "difficulty": question['difficulty']
            }
            
            if 'source' in question:
                test_case['source'] = question['source']
            
            additional_test_cases.append(test_case)
    
    additional_data = {
        "test_cases": additional_test_cases,
        "metadata": {
            "created_date": "2025-07-06",
            "total_questions": len(additional_test_cases),
            "note": "Additional questions from chunk 8 (IDs 36-40) - profile-related questions"
        }
    }
    
    # Save additional questions
    with open(output_file, 'w') as f:
        json.dump(additional_data, f, indent=2)
    
    print(f"Additional questions saved to {output_file}")
    print(f"Total additional questions: {len(additional_test_cases)}")
    return additional_data

def main():
    """Main function to run analysis and create combined files."""
    print("=== Test File Integration Analysis ===\n")
    
    # Analyze differences
    analysis = analyze_differences()
    print()
    
    # Create extended test set
    extended_data = create_extended_test_set()
    print()
    
    # Extract additional questions
    additional_data = extract_additional_questions()
    print()
    
    print("=== Summary ===")
    print(f"Main test file: {analysis['main_count']} questions")
    print(f"Chunk files: {analysis['chunk_count']} questions")
    print(f"Additional questions: {len(analysis['additional_questions'])}")
    print(f"Extended test set: {len(extended_data['test_cases'])} questions")
    
    print("\nFiles created:")
    print("- tests/qa_extended_test_set.json (40 questions)")
    print("- tests/additional_questions.json (5 additional questions)")

if __name__ == "__main__":
    main()