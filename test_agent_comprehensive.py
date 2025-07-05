#!/usr/bin/env python3
"""
Comprehensive test of Interactive CV Agent using the full QA test set.
Supports both manual-tool agent and blueprint-raw agent for comparison.
Uses the complete qa_test_set.json with 35 questions instead of the limited chunk.
"""

import json
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import argparse

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from interactive_agent_final import InteractiveCVAgent
from interactive_agent_blueprint_raw import BlueprintRawAgent
from agents.judge_agent import JudgeAgent, AnswerQuality


class ComprehensiveAgentEvaluator:
    """Evaluates the Interactive CV Agent using the comprehensive QA test set."""
    
    def __init__(self, agent_type: str = "manual"):
        """Initialize the evaluator with agent and judge.
        
        Args:
            agent_type: "manual" for InteractiveCVAgent or "blueprint" for BlueprintRawAgent
        """
        print("🚀 Initializing Comprehensive Agent Evaluator...")
        
        if agent_type == "blueprint":
            print("🔧 Using Blueprint Raw Agent (79 auto-generated tools)")
            self.agent = BlueprintRawAgent()
            self.agent_name = "Blueprint Raw Agent"
        else:
            print("🛠️ Using Manual Tool Agent (10 hand-coded tools)")
            self.agent = InteractiveCVAgent()
            self.agent_name = "Manual Tool Agent"
        
        self.agent_type = agent_type
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
            filename = f"evaluation_{self.agent_type}_{timestamp}.json"
        
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "agent_type": self.agent_type,
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


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Comprehensive Evaluation of Interactive CV Agent")
    parser.add_argument("--agent", choices=["manual", "blueprint"], default="manual", 
                       help="Agent type: 'manual' for 10 hand-coded tools, 'blueprint' for 79 auto-generated tools")
    parser.add_argument("--all", action="store_true", help="Evaluate all 35 questions")
    parser.add_argument("--random", type=int, default=5, help="Evaluate N random questions (default: 5)")
    parser.add_argument("--category", choices=["single_paper", "personal_notes", "cross_paper", "cross_domain"], 
                       help="Evaluate questions from specific category")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard", "very_hard"], 
                       help="Evaluate questions of specific difficulty")
    parser.add_argument("--questions", nargs="+", type=int, help="Question IDs to evaluate (1-35)")
    parser.add_argument("--save", action="store_true", help="Save results to file")
    parser.add_argument("--quick", action="store_true", help="Quick test with 3 random questions")
    parser.add_argument("--compare", action="store_true", help="Run both agents and compare results")
    
    args = parser.parse_args()
    
    # Handle comparison mode
    if args.compare:
        print("🔄 COMPARISON MODE: Testing both agents...")
        
        # Test manual agent
        print("\n" + "="*50)
        print("🛠️ TESTING MANUAL TOOL AGENT")
        print("="*50)
        evaluator_manual = ComprehensiveAgentEvaluator("manual")
        
        if args.quick:
            results_manual = evaluator_manual.evaluate_random_questions(3)
        elif args.random and not args.all:
            results_manual = evaluator_manual.evaluate_random_questions(args.random)
        else:
            results_manual = evaluator_manual.evaluate_random_questions(5)
        
        # Test blueprint agent
        print("\n" + "="*50)
        print("🔧 TESTING BLUEPRINT RAW AGENT")
        print("="*50)
        evaluator_blueprint = ComprehensiveAgentEvaluator("blueprint")
        
        # Use same questions for fair comparison
        same_questions = [r["question_id"] for r in results_manual]
        results_blueprint = evaluator_blueprint.evaluate_subset(same_questions)
        
        # Print comparison
        print("\n" + "="*80)
        print("📊 AGENT COMPARISON RESULTS")
        print("="*80)
        
        manual_avg = sum(r["judgment"]["score"] for r in results_manual) / len(results_manual)
        blueprint_avg = sum(r["judgment"]["score"] for r in results_blueprint) / len(results_blueprint)
        
        print(f"Manual Tool Agent (10 tools):    {manual_avg:.1f}/100")
        print(f"Blueprint Raw Agent (79 tools):  {blueprint_avg:.1f}/100")
        print(f"Difference:                      {blueprint_avg - manual_avg:+.1f} points")
        
        if args.save:
            evaluator_manual.save_results(results_manual, f"comparison_manual_{time.strftime('%Y%m%d_%H%M%S')}.json")
            evaluator_blueprint.save_results(results_blueprint, f"comparison_blueprint_{time.strftime('%Y%m%d_%H%M%S')}.json")
        
        return
    
    # Initialize evaluator with selected agent
    evaluator = ComprehensiveAgentEvaluator(args.agent)
    
    # Run evaluation based on arguments
    if args.all:
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
        count = args.random if not args.all else 5
        print(f"\n🎲 Evaluating {count} random questions...")
        results = evaluator.evaluate_random_questions(count)
    
    # Print summary
    evaluator.print_summary(results)
    
    # Save if requested
    if args.save:
        evaluator.save_results(results)
    
    print("\n✅ Comprehensive evaluation complete!")


if __name__ == "__main__":
    main()