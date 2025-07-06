#!/usr/bin/env python3
"""
Comprehensive Baseline Testing Script for Interactive CV Agent

This script tests the simplified embedding-first agent against the test dataset.
The agent uses only 3 tools, relying on semantic search across all entities.
"""

import os
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
import sys
sys.path.append(str(Path(__file__).parent))

from test_agent_comprehensive import ComprehensiveAgentEvaluator


def run_full_baseline(save_results=True, use_pro_model=False, use_claude_model=False):
    """Run comprehensive baseline evaluation on all questions."""
    
    print("🚀 INTERACTIVE CV AGENT - TESTING NEW EMBEDDING-FIRST VERSION")
    print("="*80)
    print("🎯 This tests the NEW simplified agent with only 3 tools:")
    print("   1. semantic_search - Unified embedding search across all entities")
    print("   2. navigate_relationships - Graph traversal (forward/reverse)")
    print("   3. get_entity_details - Get full entity information")
    print("="*80)
    
    # Set model if requested
    if use_claude_model:
        os.environ["AGENT_MODEL"] = "claude"
        os.environ["JUDGE_MODEL"] = "claude"
        print("🤖 Using Claude models (Claude Sonnet 4) for superior instruction following")
    elif use_pro_model:
        os.environ["AGENT_MODEL"] = "pro"
        os.environ["JUDGE_MODEL"] = "pro"
        print("🧠 Using Pro models (Gemini 2.5 Pro) for better performance")
    else:
        print("⚡ Using Flash models (Gemini 2.5 Flash) for faster evaluation")
    
    # Initialize evaluator
    print("\n🔧 Initializing NEW embedding-first agent...")
    evaluator = ComprehensiveAgentEvaluator()
    
    # Run comprehensive evaluation
    print("\n🎯 Running FULL evaluation on all 35 questions...")
    print("This will test if 3 semantic tools can replace 83 specific tools...")
    
    start_time = time.time()
    results = evaluator.evaluate_all_questions()
    total_time = time.time() - start_time
    
    # Print detailed summary
    print("\n" + "="*80)
    print("🎯 BASELINE PERFORMANCE REPORT")
    print("="*80)
    
    if results:
        # Overall metrics
        total_questions = len(results)
        total_score = sum(r["judgment"]["score"] for r in results)
        avg_score = total_score / total_questions
        
        print(f"\n📊 OVERALL BASELINE METRICS:")
        print(f"   • Total Questions: {total_questions}")
        print(f"   • Average Score: {avg_score:.1f}/100")
        print(f"   • Total Time: {total_time:.1f}s ({total_time/total_questions:.1f}s per question)")
        print(f"   • Model Used: {os.environ.get('AGENT_MODEL', 'flash')}")
        
        # Performance categorization
        excellent = len([r for r in results if r["judgment"]["score"] >= 90])
        good = len([r for r in results if 70 <= r["judgment"]["score"] < 90])
        satisfactory = len([r for r in results if 50 <= r["judgment"]["score"] < 70])
        poor = len([r for r in results if 20 <= r["judgment"]["score"] < 50])
        incorrect = len([r for r in results if r["judgment"]["score"] < 20])
        
        print(f"\n🎯 PERFORMANCE BREAKDOWN:")
        print(f"   • Excellent (90-100): {excellent:2d} ({excellent/total_questions*100:4.1f}%)")
        print(f"   • Good (70-89):       {good:2d} ({good/total_questions*100:4.1f}%)")
        print(f"   • Satisfactory (50-69): {satisfactory:2d} ({satisfactory/total_questions*100:4.1f}%)")
        print(f"   • Poor (20-49):       {poor:2d} ({poor/total_questions*100:4.1f}%)")
        print(f"   • Incorrect (0-19):   {incorrect:2d} ({incorrect/total_questions*100:4.1f}%)")
        
        # Top failures for analysis
        sorted_results = sorted(results, key=lambda r: r["judgment"]["score"])
        print(f"\n❌ WORST PERFORMING QUESTIONS (for optimization focus):")
        for i, result in enumerate(sorted_results[:5], 1):
            score = result["judgment"]["score"]
            question = result["question"][:60] + "..." if len(result["question"]) > 60 else result["question"]
            print(f"   {i}. Q{result['question_id']:2d} ({score:3d}/100): {question}")
        
        # Best performances
        print(f"\n✅ BEST PERFORMING QUESTIONS:")
        for i, result in enumerate(sorted_results[-5:], 1):
            score = result["judgment"]["score"]
            question = result["question"][:60] + "..." if len(result["question"]) > 60 else result["question"]
            print(f"   {i}. Q{result['question_id']:2d} ({score:3d}/100): {question}")
        
        # Category analysis
        category_scores = {}
        for r in results:
            cat = r["category"]
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(r["judgment"]["score"])
        
        print(f"\n📂 PERFORMANCE BY CATEGORY:")
        for cat, scores in sorted(category_scores.items()):
            avg = sum(scores) / len(scores)
            count = len(scores)
            print(f"   • {cat:15}: {avg:5.1f}/100 (n={count})")
        
        # Optimization recommendations
        print(f"\n🔧 OPTIMIZATION RECOMMENDATIONS:")
        if avg_score < 30:
            print("   🚨 CRITICAL: Agent performance is very poor (<30/100)")
            print("   • Check if tools are accessing the right data")
            print("   • Verify semantic search is working correctly")
            print("   • Review agent prompting and tool guidance")
        elif avg_score < 50:
            print("   ⚠️  NEEDS IMPROVEMENT: Agent performance is below acceptable (30-50/100)")
            print("   • Optimize tool selection strategies")
            print("   • Improve semantic search thresholds")
            print("   • Enhance system prompting")
        elif avg_score < 70:
            print("   📈 MODERATE: Agent performance is acceptable (50-70/100)")
            print("   • Fine-tune semantic search parameters")
            print("   • Optimize tool orchestration")
            print("   • Consider using Pro model for better reasoning")
        else:
            print("   ✅ GOOD: Agent performance is solid (>70/100)")
            print("   • Fine-tune edge cases")
            print("   • Optimize response time")
        
        # Save results
        if save_results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if use_claude_model:
                model_suffix = "claude"
            elif use_pro_model:
                model_suffix = "pro"
            else:
                model_suffix = "flash"
            filename = f"embedding_agent_evaluation_{model_suffix}_{timestamp}.json"
            
            baseline_report = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model_used": os.environ.get('AGENT_MODEL', 'flash'),
                "evaluation_type": "comprehensive_baseline",
                "summary": {
                    "total_questions": total_questions,
                    "average_score": avg_score,
                    "total_time": total_time,
                    "performance_breakdown": {
                        "excellent": excellent,
                        "good": good,
                        "satisfactory": satisfactory,
                        "poor": poor,
                        "incorrect": incorrect
                    },
                    "category_performance": {cat: sum(scores)/len(scores) for cat, scores in category_scores.items()}
                },
                "detailed_results": results
            }
            
            with open(filename, 'w') as f:
                json.dump(baseline_report, f, indent=2)
            
            print(f"\n💾 Baseline report saved to: {filename}")
    
    else:
        print("❌ No results obtained!")
    
    print("\n" + "="*80)
    print("🎯 BASELINE EVALUATION COMPLETE")
    print("="*80)
    
    return results


def compare_models():
    """Compare Flash vs Pro vs Claude model performance on a subset."""
    print("🔄 FLASH vs PRO vs CLAUDE MODEL COMPARISON")
    print("="*50)
    
    # Test Flash model first
    print("\n⚡ Testing with Flash model (5 random questions)...")
    os.environ["AGENT_MODEL"] = "flash"
    os.environ["JUDGE_MODEL"] = "flash"
    
    evaluator_flash = ComprehensiveAgentEvaluator()
    results_flash = evaluator_flash.evaluate_random_questions(5)
    flash_avg = sum(r["judgment"]["score"] for r in results_flash) / len(results_flash)
    
    # Test Pro model with same questions
    print("\n🧠 Testing with Pro model (same questions)...")
    os.environ["AGENT_MODEL"] = "pro"
    os.environ["JUDGE_MODEL"] = "pro"
    
    evaluator_pro = ComprehensiveAgentEvaluator()
    same_questions = [r["question_id"] for r in results_flash]
    results_pro = evaluator_pro.evaluate_subset(same_questions)
    pro_avg = sum(r["judgment"]["score"] for r in results_pro) / len(results_pro)
    
    # Test Claude model with same questions
    print("\n🤖 Testing with Claude model (same questions)...")
    os.environ["AGENT_MODEL"] = "claude"
    os.environ["JUDGE_MODEL"] = "claude"
    
    evaluator_claude = ComprehensiveAgentEvaluator()
    results_claude = evaluator_claude.evaluate_subset(same_questions)
    claude_avg = sum(r["judgment"]["score"] for r in results_claude) / len(results_claude)
    
    # Comparison
    print(f"\n📊 MODEL COMPARISON RESULTS:")
    print(f"   • Flash Model:  {flash_avg:.1f}/100")
    print(f"   • Pro Model:    {pro_avg:.1f}/100")
    print(f"   • Claude Model: {claude_avg:.1f}/100")
    
    # Find best model
    models = [("Flash", flash_avg), ("Pro", pro_avg), ("Claude", claude_avg)]
    best_model, best_score = max(models, key=lambda x: x[1])
    
    print(f"\n   🏆 Best: {best_model} ({best_score:.1f}/100)")
    
    if claude_avg > pro_avg and claude_avg > flash_avg:
        print("   ✅ Claude model shows best performance - recommend for complex queries")
    elif pro_avg > flash_avg + 10:
        print("   ✅ Pro model shows significant improvement over Flash")
    else:
        print("   ⚡ Flash model performs adequately - use for speed")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Comprehensive Baseline Testing for Interactive CV Agent")
    parser.add_argument("--full", action="store_true", help="Run full baseline on all 35 questions")
    parser.add_argument("--compare-models", action="store_true", help="Compare Flash vs Pro model performance")
    parser.add_argument("--pro", action="store_true", help="Use Pro model for evaluation")
    parser.add_argument("--claude", action="store_true", help="Use Claude model for superior instruction following")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to file")
    parser.add_argument("--quick", action="store_true", help="Quick baseline with 10 random questions")
    
    args = parser.parse_args()
    
    if args.compare_models:
        compare_models()
    elif args.full:
        run_full_baseline(save_results=not args.no_save, use_pro_model=args.pro, use_claude_model=args.claude)
    elif args.quick:
        print("⚡ QUICK BASELINE EVALUATION (10 questions)")
        print("="*50)
        
        if args.claude:
            os.environ["AGENT_MODEL"] = "claude"
            os.environ["JUDGE_MODEL"] = "claude"
        elif args.pro:
            os.environ["AGENT_MODEL"] = "pro"
            os.environ["JUDGE_MODEL"] = "pro"
        
        evaluator = ComprehensiveAgentEvaluator()
        results = evaluator.evaluate_random_questions(10)
        avg_score = sum(r["judgment"]["score"] for r in results) / len(results)
        
        print(f"\n📊 Quick Baseline: {avg_score:.1f}/100")
        
        if not args.no_save:
            evaluator.save_results(results, f"quick_baseline_{time.strftime('%Y%m%d_%H%M%S')}.json")
    else:
        print("🎯 Interactive CV Agent Baseline Testing")
        print("\nOptions:")
        print("  --full           Run comprehensive baseline (all 35 questions)")
        print("  --quick          Quick baseline (10 questions)")
        print("  --compare-models Compare Flash vs Pro model performance")
        print("  --pro            Use Pro model for better performance")
        print("  --claude         Use Claude model for superior instruction following")
        print("  --no-save        Don't save results to file")
        print("\nExample: python run_comprehensive_baseline.py --full --claude")


if __name__ == "__main__":
    main()