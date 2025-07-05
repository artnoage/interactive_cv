# Comprehensive Testing Guide for Interactive CV Agent

This guide explains how to test the Interactive CV Agent using the comprehensive QA test set with 35 questions.

## Overview

We now use the **comprehensive QA test set** (`tests/qa_test_set.json`) with 35 carefully crafted questions instead of the limited 5-question chunk. This provides:

- **35 questions** across 4 categories and 4 difficulty levels
- **Comprehensive coverage** of academic papers, personal notes, and cross-domain topics
- **Pre-written expected answers** for accurate evaluation
- **Multiple sources** including original questions and generated pairs

## Test Set Breakdown

### Categories (35 questions total)
- **single_paper** (15): Questions about specific academic papers
- **personal_notes** (14): Questions about daily work logs and chronicles  
- **cross_paper** (1): Questions spanning multiple papers
- **cross_domain** (5): Questions connecting theory and practice

### Difficulty Levels
- **easy** (8): Basic factual questions
- **medium** (17): Moderate complexity requiring understanding
- **hard** (6): Complex questions requiring synthesis
- **very_hard** (4): Advanced questions requiring deep analysis

### Question Examples
- Q1: "What is UNOT and who developed it?" (single_paper, easy)
- Q11: "What connection exists between theoretical work and game development?" (cross_domain, very_hard)
- Q20: "How does work demonstrate evolution from pure math to AI?" (cross_domain, very_hard)

## Testing Scripts

### 1. **quick_test_comprehensive.py** - Quick Validation
Tests one random question from the comprehensive set.

```bash
python quick_test_comprehensive.py
```

Perfect for:
- Verifying the system works
- Quick smoke tests
- Debugging setup issues

### 2. **test_agent_comprehensive.py** - Full Evaluation System
Comprehensive evaluation with multiple options.

```bash
# Quick test (3 random questions)
python test_agent_comprehensive.py --quick

# Test all 35 questions
python test_agent_comprehensive.py --all

# Test random subset
python test_agent_comprehensive.py --random 10

# Test by category
python test_agent_comprehensive.py --category single_paper
python test_agent_comprehensive.py --category personal_notes
python test_agent_comprehensive.py --category cross_domain

# Test by difficulty
python test_agent_comprehensive.py --difficulty easy
python test_agent_comprehensive.py --difficulty very_hard

# Test specific questions (1-35)
python test_agent_comprehensive.py --questions 1 5 10 15 20

# Save detailed results
python test_agent_comprehensive.py --all --save
```

### 3. **Legacy Scripts** (for compatibility)
- `quick_test_judge.py` - Original 5-question test
- `batch_test_questions.py` - Simple batch test

## Model Configuration

Configure models for different quality/speed trade-offs:

```bash
# High-quality evaluation (slower)
AGENT_MODEL=pro JUDGE_MODEL=pro python test_agent_comprehensive.py --all

# Fast evaluation (default)
AGENT_MODEL=flash JUDGE_MODEL=flash python test_agent_comprehensive.py --quick

# Mixed configuration
AGENT_MODEL=pro python test_agent_comprehensive.py --category cross_domain
```

## Understanding Results

### Performance Tiers
- **90-100**: Excellent - Comprehensive, accurate, all key points
- **70-89**: Good - Most points covered, minor gaps
- **50-69**: Satisfactory - Basic understanding, some missing points
- **30-49**: Poor - Limited understanding, significant gaps
- **0-29**: Incorrect - Wrong or irrelevant information

### Detailed Metrics
- **Overall average**: Should target >70 for good performance
- **Category performance**: May vary (personal_notes often easier than cross_domain)
- **Difficulty progression**: Expect scores to decrease with difficulty
- **Time per question**: Typically 2-5 seconds per response

### Quality Indicators
✅ **Good Signs**:
- Consistent scores across categories
- High performance on easy/medium questions
- Specific details from actual papers/notes
- No hallucination warnings

❌ **Warning Signs**:
- Low scores on basic factual questions
- Consistent "I don't know" responses
- Hallucination detections
- Generic answers not grounded in data

## Usage Scenarios

### Development Workflow
```bash
# 1. Quick validation during development
python quick_test_comprehensive.py

# 2. Category-focused testing
python test_agent_comprehensive.py --category single_paper --save

# 3. Full evaluation before release
AGENT_MODEL=pro JUDGE_MODEL=pro python test_agent_comprehensive.py --all --save
```

### Performance Analysis
```bash
# Test difficulty progression
python test_agent_comprehensive.py --difficulty easy --save
python test_agent_comprehensive.py --difficulty medium --save
python test_agent_comprehensive.py --difficulty hard --save
python test_agent_comprehensive.py --difficulty very_hard --save

# Compare categories
python test_agent_comprehensive.py --category single_paper --save
python test_agent_comprehensive.py --category cross_domain --save
```

### Debugging Specific Issues
```bash
# Test problematic questions
python test_agent_comprehensive.py --questions 11 17 20  # cross_domain questions

# Test personal notes understanding
python test_agent_comprehensive.py --category personal_notes

# Test complex academic questions
python test_agent_comprehensive.py --questions 6 8 14  # hard cross-paper questions
```

## Sample Questions by Category

### Single Paper (Technical Understanding)
- Q1: What is UNOT and who developed it?
- Q12: What are Fourier Neural Operators and why were they chosen?
- Q18: What are the main limitations of UNOT?

### Personal Notes (Daily Work Understanding)  
- Q3: What game development work in late June 2025?
- Q7: What pathfinding algorithm for Collapsi and why?
- Q19: What software engineering practices demonstrated?

### Cross-Domain (Connecting Theory & Practice)
- Q11: Connection between theoretical work and game development?
- Q14: How do computational trade-offs reflect in implementations?
- Q20: Evolution from pure mathematics to practical AI?

### Cross-Paper (Multi-Paper Synthesis)
- Q6: Computational complexity challenges shared between UNOT and Assignment Method?
- Q8: Key mathematical concepts across multiple papers?

## Expected Performance Targets

### By Category
- **single_paper**: 75-85 (good technical understanding)
- **personal_notes**: 80-90 (should know daily work well)  
- **cross_paper**: 60-75 (synthesis is challenging)
- **cross_domain**: 50-70 (most difficult category)

### By Difficulty
- **easy**: 85-95 (basic facts should be solid)
- **medium**: 70-85 (good understanding)
- **hard**: 55-75 (acceptable for complex questions)
- **very_hard**: 40-65 (challenging even for humans)

## Interpreting Comprehensive Results

### Summary Statistics
The comprehensive evaluation provides:
- **Overall performance** across all dimensions
- **Category breakdowns** showing strengths/weaknesses
- **Difficulty analysis** showing capability limits
- **Source analysis** (original vs generated questions)
- **Top/bottom performers** for targeted improvement

### Key Performance Indicators
1. **Average Score >70**: Generally good performance
2. **No Category <50**: Balanced understanding
3. **Easy Questions >80**: Solid foundations
4. **Low Hallucination Rate**: Trustworthy responses
5. **Consistent Performance**: Reliable across question types

## Next Steps After Testing

### Performance Analysis
1. **Identify weak categories** for targeted improvement
2. **Analyze missing points patterns** to improve tools
3. **Review hallucination cases** for safety
4. **Compare across model configurations** for optimization

### System Improvement
1. **Tool Enhancement**: Fix tools for poorly performing categories
2. **Prompt Optimization**: Improve system prompts for weak areas
3. **Knowledge Gap Filling**: Add missing information sources
4. **Response Quality**: Improve answer formatting and completeness

## Troubleshooting

### Common Issues
1. **Low scores on personal_notes**: Check chronicle search tools
2. **Poor cross_domain performance**: Improve semantic connections
3. **Hallucinations**: Strengthen grounding in actual data
4. **Timeouts**: Use flash model or reduce question complexity

### Debug Commands
```bash
# Test specific problematic areas
python test_agent_comprehensive.py --questions 11 17 20  # hardest questions
python test_agent_comprehensive.py --category cross_domain  # most challenging

# Compare model performance
AGENT_MODEL=flash python test_agent_comprehensive.py --quick
AGENT_MODEL=pro python test_agent_comprehensive.py --quick
```

This comprehensive testing framework provides the tools to thoroughly evaluate and continuously improve the Interactive CV Agent's performance across all dimensions of the knowledge base.