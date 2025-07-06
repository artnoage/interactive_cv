#!/usr/bin/env python3
"""
Test Utilities

Utility functions for working with test files.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def load_test_file(filename: str = "qa_extended_test_set.json") -> Dict:
    """Load a test file and return the data."""
    test_file = Path("tests") / filename
    with open(test_file, 'r') as f:
        return json.load(f)

def get_questions_by_category(test_data: Dict, category: str) -> List[Dict]:
    """Get all questions of a specific category."""
    return [case for case in test_data['test_cases'] if case['category'] == category]

def get_questions_by_difficulty(test_data: Dict, difficulty: str) -> List[Dict]:
    """Get all questions of a specific difficulty."""
    return [case for case in test_data['test_cases'] if case['difficulty'] == difficulty]

def get_questions_by_source(test_data: Dict, source: str) -> List[Dict]:
    """Get all questions from a specific source."""
    return [case for case in test_data['test_cases'] if case.get('source') == source]

def get_random_questions(test_data: Dict, n: int = 5, seed: Optional[int] = None) -> List[Dict]:
    """Get n random questions from the test set."""
    if seed is not None:
        random.seed(seed)
    return random.sample(test_data['test_cases'], min(n, len(test_data['test_cases'])))

def get_questions_by_id_range(test_data: Dict, start_id: int, end_id: int) -> List[Dict]:
    """Get questions within a specific ID range (inclusive)."""
    return [case for case in test_data['test_cases'] 
            if start_id <= case['id'] <= end_id]

def print_test_summary(test_data: Dict):
    """Print a summary of the test data."""
    test_cases = test_data['test_cases']
    
    print(f"Total questions: {len(test_cases)}")
    print(f"ID range: {min(case['id'] for case in test_cases)} to {max(case['id'] for case in test_cases)}")
    
    # Category breakdown
    categories = {}
    for case in test_cases:
        cat = case['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    # Difficulty breakdown
    difficulties = {}
    for case in test_cases:
        diff = case['difficulty']
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print("\nDifficulties:")
    for diff, count in sorted(difficulties.items()):
        print(f"  {diff}: {count}")
    
    # Source breakdown
    sources = {}
    for case in test_cases:
        src = case.get('source', 'unknown')
        sources[src] = sources.get(src, 0) + 1
    
    print("\nSources:")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count}")

def create_filtered_test_set(test_data: Dict, 
                           categories: Optional[List[str]] = None,
                           difficulties: Optional[List[str]] = None,
                           sources: Optional[List[str]] = None,
                           output_file: Optional[str] = None) -> Dict:
    """Create a filtered test set based on criteria."""
    filtered_cases = []
    
    for case in test_data['test_cases']:
        # Check category filter
        if categories and case['category'] not in categories:
            continue
            
        # Check difficulty filter
        if difficulties and case['difficulty'] not in difficulties:
            continue
            
        # Check source filter
        if sources and case.get('source') not in sources:
            continue
        
        filtered_cases.append(case)
    
    # Create filtered test data
    filtered_data = {
        "test_cases": filtered_cases,
        "metadata": {
            "created_date": "2025-07-06",
            "total_questions": len(filtered_cases),
            "filter_criteria": {
                "categories": categories,
                "difficulties": difficulties,
                "sources": sources
            },
            "original_total": len(test_data['test_cases']),
            "notes": f"Filtered from {len(test_data['test_cases'])} questions"
        }
    }
    
    # Save if output file specified
    if output_file:
        with open(f"tests/{output_file}", 'w') as f:
            json.dump(filtered_data, f, indent=2)
        print(f"Filtered test set saved to tests/{output_file}")
    
    return filtered_data

def compare_test_files(file1: str, file2: str) -> Tuple[List[int], List[int], List[int]]:
    """Compare two test files and return differences."""
    data1 = load_test_file(file1)
    data2 = load_test_file(file2)
    
    ids1 = {case['id'] for case in data1['test_cases']}
    ids2 = {case['id'] for case in data2['test_cases']}
    
    only_in_file1 = sorted(ids1 - ids2)
    only_in_file2 = sorted(ids2 - ids1)
    common = sorted(ids1 & ids2)
    
    return only_in_file1, only_in_file2, common

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test file utilities")
    parser.add_argument("--file", default="qa_extended_test_set.json", 
                       help="Test file to use")
    parser.add_argument("--summary", action="store_true",
                       help="Print test summary")
    parser.add_argument("--random", type=int, metavar="N",
                       help="Get N random questions")
    parser.add_argument("--category", 
                       help="Filter by category")
    parser.add_argument("--difficulty",
                       help="Filter by difficulty")
    parser.add_argument("--source",
                       help="Filter by source")
    parser.add_argument("--id-range", nargs=2, type=int, metavar=("START", "END"),
                       help="Get questions in ID range")
    parser.add_argument("--output", 
                       help="Output file for filtered results")
    
    args = parser.parse_args()
    
    # Load test data
    test_data = load_test_file(args.file)
    
    if args.summary:
        print_test_summary(test_data)
        return
    
    # Apply filters
    filtered_cases = test_data['test_cases']
    
    if args.category:
        filtered_cases = [case for case in filtered_cases if case['category'] == args.category]
    
    if args.difficulty:
        filtered_cases = [case for case in filtered_cases if case['difficulty'] == args.difficulty]
    
    if args.source:
        filtered_cases = [case for case in filtered_cases if case.get('source') == args.source]
    
    if args.id_range:
        start, end = args.id_range
        filtered_cases = [case for case in filtered_cases if start <= case['id'] <= end]
    
    if args.random:
        filtered_cases = random.sample(filtered_cases, min(args.random, len(filtered_cases)))
    
    # Output results
    if args.output:
        output_data = {
            "test_cases": filtered_cases,
            "metadata": {
                "created_date": "2025-07-06",
                "total_questions": len(filtered_cases),
                "source_file": args.file,
                "filters_applied": {
                    "category": args.category,
                    "difficulty": args.difficulty,
                    "source": args.source,
                    "id_range": args.id_range,
                    "random_count": args.random
                }
            }
        }
        
        with open(f"tests/{args.output}", 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Results saved to tests/{args.output}")
    else:
        # Print to console
        for case in filtered_cases:
            print(f"Q{case['id']}: {case['question']}")
            print(f"Expected: {case['expected_answer']}")
            print(f"Category: {case['category']}, Difficulty: {case['difficulty']}")
            if 'source' in case:
                print(f"Source: {case['source']}")
            print()

if __name__ == "__main__":
    main()