# Test Files Documentation

This directory contains comprehensive test files for the Interactive CV system, organized into different formats for flexibility and ease of use.

## File Structure

### Main Test Files
- **`qa_test_set.json`** - Original test set with 35 questions (IDs 1-35)
- **`qa_extended_test_set.json`** - Extended test set with 40 questions (IDs 1-40)
- **`additional_questions.json`** - Only the 5 additional questions (IDs 36-40)

### Chunk Files (8 sets of 5 questions each)
- **`questions_chunk_1.json` to `questions_chunk_8.json`** - Questions split into chunks
- **`answers_chunk_1.json` to `answers_chunk_8.json`** - Corresponding answers

## Test Set Overview

### Original Test Set (35 questions)
The `qa_test_set.json` file contains 35 carefully crafted questions that test various aspects of the Interactive CV system:

**Categories:**
- `single_paper` (15 questions) - Questions about specific research papers
- `personal_notes` (14 questions) - Questions about personal work and achievements  
- `cross_paper` (1 question) - Questions requiring knowledge across multiple papers
- `cross_domain` (5 questions) - Questions connecting academic work with practical projects

**Difficulty Levels:**
- `easy` (8 questions) - Simple factual questions
- `medium` (17 questions) - Moderate complexity questions
- `hard` (6 questions) - Complex analytical questions
- `very_hard` (4 questions) - Multi-step reasoning questions

### Extended Test Set (40 questions)
The `qa_extended_test_set.json` includes all 35 original questions plus 5 additional profile-related questions:

**Additional Categories:**
- `profile_research_fit` (5 questions) - Questions about research expertise and qualifications

**Total Distribution:**
- `single_paper` (12 questions)
- `personal_notes` (15 questions)
- `cross_paper` (3 questions)
- `cross_domain` (5 questions)
- `profile_research_fit` (5 questions)

## Usage Examples

### Using the Test Files in Python

```python
import json

# Load the main test set
with open('tests/qa_test_set.json', 'r') as f:
    main_tests = json.load(f)

print(f"Total questions: {len(main_tests['test_cases'])}")

# Load the extended test set  
with open('tests/qa_extended_test_set.json', 'r') as f:
    extended_tests = json.load(f)

print(f"Extended questions: {len(extended_tests['test_cases'])}")

# Access individual questions
for test_case in main_tests['test_cases']:
    print(f"Q{test_case['id']}: {test_case['question']}")
    print(f"Expected: {test_case['expected_answer']}")
    print(f"Category: {test_case['category']}, Difficulty: {test_case['difficulty']}")
    print()
```

### Running Tests with Different Models

```bash
# Test with the original 35 questions
python test_agent_comprehensive.py

# Test with the extended 40 questions  
python test_agent_comprehensive.py --test-file qa_extended_test_set.json

# Test only the additional profile questions
python test_agent_comprehensive.py --test-file additional_questions.json
```

## Question Types and Examples

### Single Paper Questions
Test understanding of specific research papers:
- "What is UNOT and who developed it?"
- "How does the Assignment Method for training GANs differ from traditional WGANs?"

### Personal Notes Questions  
Test knowledge of personal work and achievements:
- "What game development work did Vaios do in late June 2025?"
- "What specific UI improvements did Vaios make to the Collapsi game?"

### Cross Paper Questions
Test ability to connect information across multiple papers:
- "What computational complexity challenges are shared between UNOT and the Assignment Method for GANs?"

### Cross Domain Questions
Test ability to connect academic work with practical implementations:
- "How does Vaios's work demonstrate the evolution from pure mathematics to practical AI applications?"

### Profile Research Fit Questions (Extended Set Only)
Test understanding of research expertise and qualifications:
- "How does Vaios's theoretical work on Wasserstein gradient flows directly relate to modern diffusion models?"
- "What mathematical foundations does Vaios possess that make him ideal for advancing diffusion model theory?"

## Chunk File Format

Each chunk file contains 5 questions or answers with the following structure:

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is UNOT and who developed it?",
      "category": "single_paper",
      "difficulty": "easy",
      "source": "original"
    }
  ]
}
```

## Creating New Test Files

Use the `combine_test_files.py` script to manage test files:

```bash
# Run complete analysis and create combined files
python tests/combine_test_files.py

# This creates:
# - qa_extended_test_set.json (40 questions)
# - additional_questions.json (5 profile questions)
```

## Test File Maintenance

### Adding New Questions
1. Add questions to appropriate chunk files (maintaining ID sequence)
2. Add corresponding answers to answer chunk files
3. Run `combine_test_files.py` to update combined files
4. Update this README with new question counts and categories

### Modifying Existing Questions
1. Edit the question/answer in the appropriate chunk file
2. Run `combine_test_files.py` to regenerate combined files
3. Verify changes in generated files

## Integration with Test Scripts

The test files are designed to work with various test scripts:

- **`test_agent_comprehensive.py`** - Comprehensive agent testing
- **`run_comprehensive_baseline.py`** - Baseline performance measurement
- **`test_agent_with_judge.py`** - Judge-evaluated testing

All scripts can accept different test files via command-line arguments for flexibility.

## Test Utilities

### `test_utils.py` - Test File Helper Functions

Utility library providing common functions for working with test files across the testing framework.

**Key Functions:**
- `load_test_file(filename)`: Load any test file with error handling
- `get_questions_by_category(test_data, category)`: Filter questions by category
- `get_questions_by_difficulty(test_data, difficulty)`: Filter questions by difficulty level
- `get_random_questions(test_data, count)`: Get random sample of questions
- `validate_test_structure(test_data)`: Verify test file format and required fields

**Usage:**
```python
from tests.test_utils import load_test_file, get_questions_by_category

# Load test data
test_data = load_test_file("qa_extended_test_set.json")

# Get specific categories
single_paper_questions = get_questions_by_category(test_data, "single_paper")
cross_domain_questions = get_questions_by_category(test_data, "cross_domain")

# Get random sample for quick testing
random_questions = get_random_questions(test_data, 5)
```

### `verify_test_files.py` - Test File Integrity Checker

Comprehensive verification script that checks consistency and integrity across all test files in the testing framework.

**Verification Checks:**
- **File Consistency**: Ensures all chunk files combine correctly into complete sets
- **ID Continuity**: Verifies question IDs are sequential and complete
- **JSON Validation**: Checks all files are valid JSON with required fields
- **Category Validation**: Ensures categories match expected values
- **Difficulty Validation**: Verifies difficulty levels are consistent
- **Cross-File Consistency**: Checks that combined files match individual chunks

**Usage:**
```bash
# Run comprehensive verification
python tests/verify_test_files.py

# Example output:
# === Test File Verification ===
# 
# ✓ Main test set loaded: 35 questions
# ✓ Extended test set loaded: 40 questions  
# ✓ All chunk files loaded successfully
# ✓ ID sequence is complete (1-40)
# ✓ Categories are consistent
# ✓ Combined files match individual chunks
```

**Integration:**
This script is useful for:
- CI/CD pipeline testing validation
- Pre-commit hooks to ensure test file integrity
- Debugging test file issues during development
- Validating test file modifications

## Best Practices

1. **Use Extended Set for Complete Testing** - The 40-question extended set provides comprehensive coverage
2. **Profile Questions for Specific Use Cases** - Use the profile questions when testing research-fit scenarios
3. **Chunk Files for Parallel Processing** - Use individual chunk files when running tests in parallel
4. **Maintain ID Consistency** - Keep question IDs consistent across all files
5. **Update Documentation** - Always update this README when modifying test files

## File Relationships

```
qa_test_set.json (35 questions, IDs 1-35)
├── Source of truth for original questions
└── Fully contained in chunks 1-7

qa_extended_test_set.json (40 questions, IDs 1-40)  
├── Includes all questions from qa_test_set.json
├── Adds 5 profile questions from chunk 8
└── Recommended for comprehensive testing

Chunk files (IDs 1-40)
├── questions_chunk_1.json + answers_chunk_1.json (IDs 1-5)
├── questions_chunk_2.json + answers_chunk_2.json (IDs 6-10)
├── ...
├── questions_chunk_7.json + answers_chunk_7.json (IDs 31-35)
└── questions_chunk_8.json + answers_chunk_8.json (IDs 36-40)
```

This structure provides maximum flexibility while maintaining consistency and avoiding duplication.