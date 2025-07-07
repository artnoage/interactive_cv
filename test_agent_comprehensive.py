#!/usr/bin/env python3
"""
Comprehensive test of Interactive CV Agent using the full QA test set.
Uses the embedding-first agent with 6 unified tools + MCP integration.
Includes baseline evaluation, model comparison, and detailed performance analysis.
"""

import json
import random
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import argparse
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from interactive_agent import InteractiveCVAgent
from agents.judge_agent import JudgeAgent, AnswerQuality


class ComprehensiveAgentEvaluator:
    """Evaluates the Interactive CV Agent using the comprehensive QA test set."""
    
    def __init__(self):
        """Initialize the evaluator with agent and judge."""
        print("🚀 Initializing Comprehensive Agent Evaluator...")
        
        print("🎯 Using Embedding-First Agent (3 unified tools with semantic search)")
        self.agent_name = "Embedding-First Agent"
        
        self.agent = InteractiveCVAgent()
        
        self.judge = JudgeAgent()
        
        # Load comprehensive test set
        with open("tests/qa_test_set.json") as f:
            self.test_data = json.load(f)
            self.questions = self.test_data["test_cases"]
            self.metadata = self.test_data["metadata"]
        
        print(f"📊 Loaded {self.metadata['total_questions']} questions")
        print(f"   Categories: {self.metadata['categories']}")
        print(f"   Difficulty: {self.metadata['difficulty_distribution']}")
        print(f"🤖 Testing with: {self.agent_name}")
    
    def get_agent_answer(self, question: str) -> str:
        """Get answer from the agent for a question."""
        try:
            # Use a unique thread ID for each question to avoid context pollution
            thread_id = f"test_{hash(question)}"
            return self.agent.chat(question, thread_id)
        except Exception as e:
            return f"Error getting answer: {str(e)}"
    
    def evaluate_single_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single question."""
        question_id = question_data["id"]
        question_text = question_data["question"]
        expected_answer = question_data["expected_answer"]
        
        print(f"\n{'='*80}")
        print(f"📝 Question {question_id}: {question_text}")
        print(f"   Category: {question_data['category']}, Difficulty: {question_data['difficulty']}")
        if "source" in question_data:
            print(f"   Source: {question_data['source']}")
        print("="*80)
        
        # Get agent's answer
        print("\n🤖 Getting agent's answer...")
        start_time = time.time()
        agent_answer = self.get_agent_answer(question_text)
        answer_time = time.time() - start_time
        
        print(f"\n📊 Agent answered in {answer_time:.2f} seconds")
        print("\n--- Agent's Answer ---")
        print(agent_answer[:500] + "..." if len(agent_answer) > 500 else agent_answer)
        
        # Judge the answer
        print("\n⚖️ Judging the answer...")
        judgment = self.judge.evaluate_answer(
            question_text,
            expected_answer,
            agent_answer
        )
        
        # Display judgment
        print(f"\n🏆 Score: {judgment.score}/100 ({judgment.quality.value})")
        print(f"📋 Reasoning: {judgment.reasoning}")
        
        if judgment.key_points_covered:
            print(f"✅ Key points covered: {', '.join(judgment.key_points_covered[:3])}")
        
        if judgment.missing_points:
            print(f"❌ Missing points: {', '.join(judgment.missing_points[:3])}")
        
        if judgment.has_hallucination:
            print("⚠️ WARNING: Potential hallucination detected!")
        
        return {
            "question_id": question_id,
            "question": question_text,
            "category": question_data["category"],
            "difficulty": question_data["difficulty"],
            "source": question_data.get("source", "original"),
            "agent_answer": agent_answer,
            "expected_answer": expected_answer,
            "judgment": {
                "score": judgment.score,
                "quality": judgment.quality.value,
                "reasoning": judgment.reasoning,
                "key_points_covered": judgment.key_points_covered,
                "missing_points": judgment.missing_points,
                "has_hallucination": judgment.has_hallucination
            },
            "answer_time": answer_time
        }
    
    def evaluate_all_questions(self) -> List[Dict[str, Any]]:
        """Evaluate all test questions."""
        results = []
        
        print(f"\n🎯 Evaluating {len(self.questions)} questions...")
        
        for i, question in enumerate(self.questions, 1):
            print(f"\n[{i}/{len(self.questions)}]", end="")
            result = self.evaluate_single_question(question)
            results.append(result)
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        return results
    
    def evaluate_random_questions(self, count: int = 5) -> List[Dict[str, Any]]:
        """Evaluate random questions."""
        selected = random.sample(self.questions, min(count, len(self.questions)))
        results = []
        
        print(f"\n🎲 Evaluating {len(selected)} random questions...")
        
        for i, question in enumerate(selected, 1):
            print(f"\n[{i}/{len(selected)}]", end="")
            result = self.evaluate_single_question(question)
            results.append(result)
            
            time.sleep(1)
        
        return results
    
    def evaluate_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Evaluate questions from a specific category."""
        category_questions = [q for q in self.questions if q["category"] == category]
        
        if not category_questions:
            print(f"❌ No questions found for category: {category}")
            return []
        
        results = []
        print(f"\n📂 Evaluating {len(category_questions)} questions from category '{category}'...")
        
        for i, question in enumerate(category_questions, 1):
            print(f"\n[{i}/{len(category_questions)}]", end="")
            result = self.evaluate_single_question(question)
            results.append(result)
            
            time.sleep(1)
        
        return results
    
    def evaluate_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Evaluate questions of a specific difficulty."""
        difficulty_questions = [q for q in self.questions if q["difficulty"] == difficulty]
        
        if not difficulty_questions:
            print(f"❌ No questions found for difficulty: {difficulty}")
            return []
        
        results = []
        print(f"\n🎯 Evaluating {len(difficulty_questions)} '{difficulty}' questions...")
        
        for i, question in enumerate(difficulty_questions, 1):
            print(f"\n[{i}/{len(difficulty_questions)}]", end="")
            result = self.evaluate_single_question(question)
            results.append(result)
            
            time.sleep(1)
        
        return results
    
    def evaluate_subset(self, indices: List[int]) -> List[Dict[str, Any]]:
        """Evaluate a subset of questions by indices."""
        results = []
        
        for idx in indices:
            if 1 <= idx <= len(self.questions):
                question = self.questions[idx - 1]  # Convert to 0-based
                result = self.evaluate_single_question(question)
                results.append(result)
            else:
                print(f"⚠️ Invalid question index: {idx} (valid range: 1-{len(self.questions)})")
        
        return results
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print comprehensive summary statistics."""
        print("\n" + "="*80)
        print(f"📊 COMPREHENSIVE EVALUATION SUMMARY - {self.agent_name}")
        print("="*80)
        
        if not results:
            print("No results to summarize.")
            return
        
        # Basic statistics
        total_questions = len(results)
        total_score = sum(r["judgment"]["score"] for r in results)
        avg_score = total_score / total_questions
        total_time = sum(r["answer_time"] for r in results)
        
        print(f"\n📈 Overall Performance:")
        print(f"   - Questions Evaluated: {total_questions}")
        print(f"   - Average Score: {avg_score:.1f}/100")
        print(f"   - Total Time: {total_time:.1f}s ({total_time/total_questions:.1f}s per question)")
        
        # Quality distribution
        quality_counts = {}
        for r in results:
            quality = r["judgment"]["quality"]
            quality_counts[quality] = quality_counts.get(quality, 0) + 1
        
        print(f"\n🎯 Quality Distribution:")
        for quality in ["excellent", "good", "satisfactory", "poor", "incorrect"]:
            count = quality_counts.get(quality, 0)
            percentage = (count / total_questions * 100) if total_questions > 0 else 0
            print(f"   - {quality.capitalize():12}: {count:2d} ({percentage:4.1f}%)")
        
        # Category breakdown
        category_scores = {}
        for r in results:
            cat = r["category"]
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(r["judgment"]["score"])
        
        print(f"\n📊 Performance by Category:")
        for cat, scores in sorted(category_scores.items()):
            avg = sum(scores) / len(scores)
            count = len(scores)
            print(f"   - {cat:15}: {avg:5.1f}/100 (n={count})")
        
        # Difficulty breakdown
        difficulty_scores = {}
        for r in results:
            diff = r["difficulty"]
            if diff not in difficulty_scores:
                difficulty_scores[diff] = []
            difficulty_scores[diff].append(r["judgment"]["score"])
        
        print(f"\n🎯 Performance by Difficulty:")
        difficulty_order = ["easy", "medium", "hard", "very_hard"]
        for diff in difficulty_order:
            if diff in difficulty_scores:
                scores = difficulty_scores[diff]
                avg = sum(scores) / len(scores)
                count = len(scores)
                print(f"   - {diff.capitalize():10}: {avg:5.1f}/100 (n={count})")
        
        # Source breakdown (if available)
        source_scores = {}
        for r in results:
            source = r.get("source", "original")
            if source not in source_scores:
                source_scores[source] = []
            source_scores[source].append(r["judgment"]["score"])
        
        if len(source_scores) > 1:
            print(f"\n📝 Performance by Source:")
            for source, scores in sorted(source_scores.items()):
                avg = sum(scores) / len(scores)
                count = len(scores)
                print(f"   - {source:15}: {avg:5.1f}/100 (n={count})")
        
        # Best and worst performances
        if results:
            sorted_results = sorted(results, key=lambda r: r["judgment"]["score"], reverse=True)
            
            print(f"\n🏆 Top 3 Performances:")
            for i, result in enumerate(sorted_results[:3], 1):
                print(f"   {i}. Q{result['question_id']:2d} ({result['judgment']['score']:3d}/100): {result['question'][:50]}...")
            
            print(f"\n😞 Bottom 3 Performances:")
            for i, result in enumerate(sorted_results[-3:], 1):
                print(f"   {i}. Q{result['question_id']:2d} ({result['judgment']['score']:3d}/100): {result['question'][:50]}...")
        
        # Hallucination analysis
        hallucinations = [r for r in results if r["judgment"]["has_hallucination"]]
        if hallucinations:
            print(f"\n⚠️ Hallucinations Detected: {len(hallucinations)}")
            for h in hallucinations:
                print(f"   - Q{h['question_id']}: {h['question'][:40]}...")
    
    def save_results(self, results: List[Dict[str, Any]], filename: str = None):
        """Save evaluation results to file."""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_{timestamp}.json"
        
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "agent_name": self.agent_name,
            "test_set_metadata": self.metadata,
            "summary": {
                "total_questions": len(results),
                "average_score": sum(r["judgment"]["score"] for r in results) / len(results) if results else 0,
                "total_time": sum(r["answer_time"] for r in results)
            },
            "results": results
        }
        
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 Results saved to {filename}")
    
    def run_baseline_evaluation(self, model_name: str = "flash") -> List[Dict[str, Any]]:
        """Run comprehensive baseline evaluation with enhanced reporting."""
        print(f"\n🚀 INTERACTIVE CV AGENT - BASELINE EVALUATION")
        print("="*80)
        print(f"🎯 Testing agent with 6 unified tools + MCP integration:")
        print("   1. semantic_search - Unified embedding search across all entities")
        print("   2. navigate_relationships - Graph traversal (forward/reverse)")
        print("   3. get_entity_details - Get full entity information")
        print("   4. list_available_papers - Paper catalog access")
        print("   5. consult_manuscript - Deep document analysis (META TOOL)")
        print("   6. sequential_reasoning - Structured analysis (META TOOL)")
        print("="*80)
        
        start_time = time.time()
        results = self.evaluate_all_questions()
        total_time = time.time() - start_time
        
        if results:
            self.print_baseline_analysis(results, total_time, model_name)
        
        return results
    
    def print_baseline_analysis(self, results: List[Dict[str, Any]], total_time: float, model_name: str):
        """Print detailed baseline analysis."""
        print("\n" + "="*80)
        print("🎯 BASELINE PERFORMANCE REPORT")
        print("="*80)
        
        total_questions = len(results)
        total_score = sum(r["judgment"]["score"] for r in results)
        avg_score = total_score / total_questions
        
        print(f"\n📊 OVERALL BASELINE METRICS:")
        print(f"   • Total Questions: {total_questions}")
        print(f"   • Average Score: {avg_score:.1f}/100")
        print(f"   • Total Time: {total_time:.1f}s ({total_time/total_questions:.1f}s per question)")
        print(f"   • Model Used: {model_name}")
        
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
        
        # Top and bottom performers
        sorted_results = sorted(results, key=lambda r: r["judgment"]["score"])
        print(f"\n❌ WORST PERFORMING QUESTIONS (optimization focus):")
        for i, result in enumerate(sorted_results[:5], 1):
            score = result["judgment"]["score"]
            question = result["question"][:60] + "..." if len(result["question"]) > 60 else result["question"]
            print(f"   {i}. Q{result['question_id']:2d} ({score:3d}/100): {question}")
        
        print(f"\n✅ BEST PERFORMING QUESTIONS:")
        for i, result in enumerate(sorted_results[-5:], 1):
            score = result["judgment"]["score"]
            question = result["question"][:60] + "..." if len(result["question"]) > 60 else result["question"]
            print(f"   {i}. Q{result['question_id']:2d} ({score:3d}/100): {question}")
        
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
    
    def compare_models(self, question_count: int = 5) -> Dict[str, float]:
        """Compare Flash vs Pro vs Claude model performance."""
        print(f"\n🔄 FLASH vs PRO vs CLAUDE MODEL COMPARISON")
        print("="*50)
        
        results = {}
        
        # Test Flash model
        print(f"\n⚡ Testing with Flash model ({question_count} questions)...")
        os.environ["AGENT_MODEL"] = "flash"
        os.environ["JUDGE_MODEL"] = "flash"
        
        flash_results = self.evaluate_random_questions(question_count)
        results["flash"] = sum(r["judgment"]["score"] for r in flash_results) / len(flash_results)
        flash_questions = [r["question_id"] for r in flash_results]
        
        # Test Pro model with same questions
        print(f"\n🧠 Testing with Pro model (same questions)...")
        os.environ["AGENT_MODEL"] = "pro"
        os.environ["JUDGE_MODEL"] = "pro"
        
        pro_results = self.evaluate_subset(flash_questions)
        results["pro"] = sum(r["judgment"]["score"] for r in pro_results) / len(pro_results)
        
        # Test Claude model with same questions
        print(f"\n🤖 Testing with Claude model (same questions)...")
        os.environ["AGENT_MODEL"] = "claude"
        os.environ["JUDGE_MODEL"] = "claude"
        
        claude_results = self.evaluate_subset(flash_questions)
        results["claude"] = sum(r["judgment"]["score"] for r in claude_results) / len(claude_results)
        
        # Print comparison
        print(f"\n📊 MODEL COMPARISON RESULTS:")
        print(f"   • Flash Model:  {results['flash']:.1f}/100")
        print(f"   • Pro Model:    {results['pro']:.1f}/100")
        print(f"   • Claude Model: {results['claude']:.1f}/100")
        
        best_model = max(results, key=results.get)
        print(f"\n   🏆 Best: {best_model.capitalize()} ({results[best_model]:.1f}/100)")
        
        return results
    
    def save_baseline_report(self, results: List[Dict[str, Any]], model_name: str, filename: str = None):
        """Save comprehensive baseline report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"baseline_evaluation_{model_name}_{timestamp}.json"
        
        # Calculate category performance
        category_scores = {}
        for r in results:
            cat = r["category"]
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(r["judgment"]["score"])
        
        # Performance breakdown
        total_questions = len(results)
        excellent = len([r for r in results if r["judgment"]["score"] >= 90])
        good = len([r for r in results if 70 <= r["judgment"]["score"] < 90])
        satisfactory = len([r for r in results if 50 <= r["judgment"]["score"] < 70])
        poor = len([r for r in results if 20 <= r["judgment"]["score"] < 50])
        incorrect = len([r for r in results if r["judgment"]["score"] < 20])
        
        baseline_report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_used": model_name,
            "evaluation_type": "comprehensive_baseline",
            "agent_description": "6 unified tools + MCP integration",
            "summary": {
                "total_questions": total_questions,
                "average_score": sum(r["judgment"]["score"] for r in results) / total_questions,
                "total_time": sum(r["answer_time"] for r in results),
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
        return filename


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Evaluation of Interactive CV Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_agent_comprehensive.py --all --baseline --claude --save
  python test_agent_comprehensive.py --random 10 --pro --verbose
  python test_agent_comprehensive.py --category cross_domain --baseline
  python test_agent_comprehensive.py --compare-models --questions 5
  python test_agent_comprehensive.py --quick --flash
        """
    )
    
    # Evaluation scope
    eval_group = parser.add_mutually_exclusive_group()
    eval_group.add_argument("--all", action="store_true", help="Evaluate all 35 questions")
    eval_group.add_argument("--random", type=int, default=5, help="Evaluate N random questions (default: 5)")
    eval_group.add_argument("--quick", action="store_true", help="Quick test with 3 random questions")
    eval_group.add_argument("--category", choices=["single_paper", "personal_notes", "cross_paper", "cross_domain"], 
                           help="Evaluate questions from specific category")
    eval_group.add_argument("--difficulty", choices=["easy", "medium", "hard", "very_hard"], 
                           help="Evaluate questions of specific difficulty")
    eval_group.add_argument("--questions", nargs="+", type=int, help="Question IDs to evaluate (1-35)")
    eval_group.add_argument("--compare-models", action="store_true", help="Compare Flash vs Pro vs Claude models")
    
    # Model selection
    model_group = parser.add_mutually_exclusive_group()
    model_group.add_argument("--flash", action="store_true", help="Use Flash model (default, fastest)")
    model_group.add_argument("--pro", action="store_true", help="Use Pro model (better performance)")
    model_group.add_argument("--claude", action="store_true", help="Use Claude model (best instruction following)")
    
    # Reporting options
    parser.add_argument("--baseline", action="store_true", help="Run baseline evaluation with enhanced reporting")
    parser.add_argument("--save", action="store_true", help="Save results to file")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to file")
    parser.add_argument("--output-file", type=str, help="Specify output filename")
    parser.add_argument("--verbose", action="store_true", help="Verbose output with detailed analysis")
    parser.add_argument("--summary-only", action="store_true", help="Show only summary, skip individual question details")
    
    args = parser.parse_args()
    
    # Set model environment variables
    model_name = "flash"  # default
    if args.claude:
        os.environ["AGENT_MODEL"] = "claude"
        os.environ["JUDGE_MODEL"] = "claude"
        model_name = "claude"
        print("🤖 Using Claude models (best instruction following)")
    elif args.pro:
        os.environ["AGENT_MODEL"] = "pro"
        os.environ["JUDGE_MODEL"] = "pro"
        model_name = "pro"
        print("🧠 Using Pro models (better performance)")
    elif args.flash:
        os.environ["AGENT_MODEL"] = "flash"
        os.environ["JUDGE_MODEL"] = "flash"
        model_name = "flash"
        print("⚡ Using Flash models (fastest)")
    
    # Initialize evaluator
    evaluator = ComprehensiveAgentEvaluator()
    
    # Handle model comparison
    if args.compare_models:
        question_count = args.questions[0] if args.questions else 5
        evaluator.compare_models(question_count)
        return
    
    # Run evaluation based on arguments
    results = []
    
    if args.all:
        if args.baseline:
            results = evaluator.run_baseline_evaluation(model_name)
        else:
            print("\n🎯 Evaluating ALL 35 questions...")
            results = evaluator.evaluate_all_questions()
    elif args.category:
        print(f"\n📂 Evaluating {args.category} questions...")
        results = evaluator.evaluate_by_category(args.category)
    elif args.difficulty:
        print(f"\n🎯 Evaluating {args.difficulty} difficulty questions...")
        results = evaluator.evaluate_by_difficulty(args.difficulty)
    elif args.questions:
        print(f"\n📋 Evaluating questions: {args.questions}")
        results = evaluator.evaluate_subset(args.questions)
    elif args.quick:
        print("\n⚡ Quick test with 3 random questions...")
        results = evaluator.evaluate_random_questions(3)
    else:
        # Default: random questions
        count = args.random
        print(f"\n🎲 Evaluating {count} random questions...")
        results = evaluator.evaluate_random_questions(count)
    
    # Print summary (unless summary-only and baseline was already run)
    if not (args.baseline and args.all):
        if args.baseline and results:
            # Print baseline analysis for non-full evaluations
            total_time = sum(r["answer_time"] for r in results)
            evaluator.print_baseline_analysis(results, total_time, model_name)
        elif not args.summary_only:
            evaluator.print_summary(results)
        else:
            # Summary only
            if results:
                avg_score = sum(r["judgment"]["score"] for r in results) / len(results)
                print(f"\n📊 SUMMARY: {len(results)} questions, Average: {avg_score:.1f}/100")
    
    # Save results
    save_results = args.save or (not args.no_save and (args.baseline or args.all))
    
    if save_results and results:
        if args.baseline:
            evaluator.save_baseline_report(results, model_name, args.output_file)
        else:
            if args.output_file:
                evaluator.save_results(results, args.output_file)
            else:
                evaluator.save_results(results)
    
    print("\n✅ Comprehensive evaluation complete!")


if __name__ == "__main__":
    main()