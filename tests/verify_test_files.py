#!/usr/bin/env python3
"""
Test File Verification Script

Verifies the integrity and consistency of all test files.
"""

import json
from pathlib import Path

def verify_test_files():
    """Verify all test files for consistency and integrity."""
    test_dir = Path("tests")
    
    print("=== Test File Verification ===\n")
    
    # Load all files
    try:
        with open(test_dir / "qa_test_set.json", 'r') as f:
            main_data = json.load(f)
        
        with open(test_dir / "qa_extended_test_set.json", 'r') as f:
            extended_data = json.load(f)
        
        with open(test_dir / "additional_questions.json", 'r') as f:
            additional_data = json.load(f)
        
        print("✅ All main test files loaded successfully")
    except Exception as e:
        print(f"❌ Error loading main test files: {e}")
        return False
    
    # Verify main test file
    main_cases = {case['id']: case for case in main_data['test_cases']}
    print(f"✅ Main test file: {len(main_cases)} questions (IDs {min(main_cases.keys())}-{max(main_cases.keys())})")
    
    # Verify extended test file
    extended_cases = {case['id']: case for case in extended_data['test_cases']}
    print(f"✅ Extended test file: {len(extended_cases)} questions (IDs {min(extended_cases.keys())}-{max(extended_cases.keys())})")
    
    # Verify additional questions
    additional_cases = {case['id']: case for case in additional_data['test_cases']}
    print(f"✅ Additional questions: {len(additional_cases)} questions (IDs {min(additional_cases.keys())}-{max(additional_cases.keys())})")
    
    # Check that extended contains all main questions
    missing_in_extended = set(main_cases.keys()) - set(extended_cases.keys())
    if missing_in_extended:
        print(f"❌ Extended test file missing questions: {missing_in_extended}")
        return False
    else:
        print("✅ Extended test file contains all main questions")
    
    # Check that additional questions are in extended
    missing_additional = set(additional_cases.keys()) - set(extended_cases.keys())
    if missing_additional:
        print(f"❌ Extended test file missing additional questions: {missing_additional}")
        return False
    else:
        print("✅ Extended test file contains all additional questions")
    
    # Verify chunk files
    print("\n=== Chunk File Verification ===")
    
    all_chunk_questions = {}
    all_chunk_answers = {}
    
    for i in range(1, 9):
        try:
            with open(test_dir / f"questions_chunk_{i}.json", 'r') as f:
                q_data = json.load(f)
            
            with open(test_dir / f"answers_chunk_{i}.json", 'r') as f:
                a_data = json.load(f)
            
            q_ids = [q['id'] for q in q_data['questions']]
            a_ids = [a['id'] for a in a_data['answers']]
            
            print(f"✅ Chunk {i}: {len(q_ids)} questions, {len(a_ids)} answers (IDs {min(q_ids)}-{max(q_ids)})")
            
            # Check that question and answer IDs match
            if set(q_ids) != set(a_ids):
                print(f"❌ Chunk {i}: Question and answer IDs don't match")
                return False
            
            # Collect all questions and answers
            for q in q_data['questions']:
                all_chunk_questions[q['id']] = q
            for a in a_data['answers']:
                all_chunk_answers[a['id']] = a
        
        except Exception as e:
            print(f"❌ Error loading chunk {i}: {e}")
            return False
    
    print(f"✅ All chunk files loaded: {len(all_chunk_questions)} questions, {len(all_chunk_answers)} answers")
    
    # Verify that chunk questions match extended questions
    chunk_ids = set(all_chunk_questions.keys())
    extended_ids = set(extended_cases.keys())
    
    if chunk_ids != extended_ids:
        print(f"❌ Chunk questions don't match extended questions")
        print(f"   Missing in chunks: {extended_ids - chunk_ids}")
        print(f"   Extra in chunks: {chunk_ids - extended_ids}")
        return False
    else:
        print("✅ Chunk questions match extended questions perfectly")
    
    # Verify question content consistency
    print("\n=== Content Consistency Verification ===")
    
    inconsistent_questions = []
    for q_id in extended_ids:
        extended_q = extended_cases[q_id]['question']
        chunk_q = all_chunk_questions[q_id]['question']
        
        if extended_q != chunk_q:
            inconsistent_questions.append(q_id)
    
    if inconsistent_questions:
        print(f"❌ Inconsistent question content for IDs: {inconsistent_questions}")
        return False
    else:
        print("✅ All question content is consistent across files")
    
    # Verify answer consistency
    inconsistent_answers = []
    for q_id in extended_ids:
        extended_a = extended_cases[q_id]['expected_answer']
        chunk_a = all_chunk_answers[q_id]['expected_answer']
        
        if extended_a != chunk_a:
            inconsistent_answers.append(q_id)
    
    if inconsistent_answers:
        print(f"❌ Inconsistent answer content for IDs: {inconsistent_answers}")
        return False
    else:
        print("✅ All answer content is consistent across files")
    
    # Summary statistics
    print("\n=== Summary Statistics ===")
    
    categories = {}
    difficulties = {}
    sources = {}
    
    for case in extended_cases.values():
        cat = case['category']
        categories[cat] = categories.get(cat, 0) + 1
        
        diff = case['difficulty']
        difficulties[diff] = difficulties.get(diff, 0) + 1
        
        src = case.get('source', 'unknown')
        sources[src] = sources.get(src, 0) + 1
    
    print(f"Categories: {dict(sorted(categories.items()))}")
    print(f"Difficulties: {dict(sorted(difficulties.items()))}")
    print(f"Sources: {dict(sorted(sources.items()))}")
    
    print("\n✅ All verification checks passed!")
    return True

if __name__ == "__main__":
    success = verify_test_files()
    exit(0 if success else 1)