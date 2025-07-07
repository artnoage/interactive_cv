#!/usr/bin/env python3
"""
Judge Agent for evaluating answer correctness using LLM.
Uses Gemini Flash 2.5 to compare agent responses against expected answers.
"""

import os
from typing import Optional
from dataclasses import dataclass
from enum import Enum
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()


class AnswerQuality(Enum):
    """Quality levels for answer evaluation."""
    EXCELLENT = "excellent"      # 90-100 points
    GOOD = "good"               # 70-89 points
    SATISFACTORY = "satisfactory" # 50-69 points
    POOR = "poor"               # 30-49 points
    INCORRECT = "incorrect"      # 0-29 points


@dataclass
class JudgmentResult:
    """Result of judge evaluation."""
    score: int  # 0-100
    quality: AnswerQuality
    reasoning: str
    key_points_covered: list
    missing_points: list
    accuracy_assessment: str
    has_hallucination: bool


class JudgeAgent:
    """LLM-based judge for evaluating answer correctness."""
    
    # Model configuration
    MODELS = {
        "flash": "google/gemini-2.5-flash",
        "pro": "google/gemini-2.5-pro",
        "claude": "anthropic/claude-sonnet-4",
        "mistral": "mistralai/mistral-small-3.2-24b-instruct",
        "lmstudio": "google/gemma-3-12b"
    }
    
    MODEL_CONFIGS = {
        "google/gemini-2.5-flash": {
            "temperature": 0.1,
            "max_tokens": 4096
        },
        "google/gemini-2.5-pro": {
            "temperature": 0.1,
            "max_tokens": 8192
        },
        "anthropic/claude-sonnet-4": {
            "temperature": 0.1,
            "max_tokens": 4096
        },
        "mistralai/mistral-small-3.2-24b-instruct": {
            "temperature": 0.1,
            "max_tokens": 4096
        },
        "google/gemma-3-12b": {
            "temperature": 0.1,
            "max_tokens": 2048
        }
    }
    
    def __init__(self, model: Optional[str] = None):
        """Initialize judge with specified or configured model."""
        # Always use Gemini Flash for judge, regardless of agent model
        if model is None:
            model_key = "flash"  # Force Flash for judge
            model = self.MODELS["flash"]
        else:
            model_key = "flash"  # Force Flash for judge
        
        # Check API key only for non-local models
        if model_key != "lmstudio":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not found in .env file")
        else:
            api_key = "lm-studio"  # Dummy key for LM Studio
        
        model_config = self.MODEL_CONFIGS.get(model, self.MODEL_CONFIGS["google/gemini-2.5-flash"])
        
        # Get max tokens from config
        max_tokens = model_config.get("max_tokens", 4096)
        
        # Check if using LM Studio
        model_key = os.getenv("JUDGE_MODEL", "flash")
        if model_key == "lmstudio":
            self.llm = ChatOpenAI(
                base_url="http://localhost:1234/v1",
                api_key="lm-studio",  # LM Studio doesn't require real key
                model=model,
                temperature=model_config.get("temperature", 0.1),
                model_kwargs={"max_tokens": max_tokens}
            )
        else:
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=SecretStr(api_key),
                model=model,
                temperature=model_config.get("temperature", 0.1),
                default_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Interactive CV Judge Agent",
                },
                model_kwargs={"max_tokens": max_tokens}
            )
        
        print(f"⚖️ Judge using model: {model}")
        
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the judge."""
        return """You are an expert judge evaluating the quality and correctness of answers about academic research.

Your task is to compare a given answer against an expected/correct answer and provide a detailed evaluation.

Evaluation Criteria:
1. **Factual Accuracy** (40 points): Are the facts, concepts, and relationships correct?
2. **Completeness** (30 points): Does it cover the key points from the expected answer?
3. **Clarity** (20 points): Is the answer clear and well-structured?
4. **Evidence** (10 points): Does it provide citations or specific examples?

Important Guidelines:
- Focus on content accuracy, not writing style
- Accept paraphrasing and different ways of explaining the same concept
- Give partial credit for partially correct answers
- If the agent says "I don't have this information", score it as 0
- If the agent provides some relevant information but incomplete, give partial credit
- Identify any hallucinations or incorrect statements
- Be fair but rigorous in your assessment

Output your evaluation in this JSON format:
{
    "score": <0-100>,
    "quality": "<excellent|good|satisfactory|poor|incorrect>",
    "reasoning": "<brief explanation of score>",
    "key_points_covered": ["<point1>", "<point2>", ...],
    "missing_points": ["<point1>", "<point2>", ...],
    "accuracy_assessment": "<assessment of factual accuracy>",
    "has_hallucination": <true|false>
}"""
    
    def evaluate_answer(self, question: str, expected_answer: str, 
                       given_answer: str) -> JudgmentResult:
        """Evaluate a given answer against the expected answer."""
        
        # Create evaluation prompt
        evaluation_prompt = f"""Question: {question}

Expected/Correct Answer:
{expected_answer}

Given Answer to Evaluate:
{given_answer}

Please evaluate the given answer against the expected answer according to the criteria in your instructions."""
        
        try:
            # Get LLM judgment
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=evaluation_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse JSON response
            try:
                # Extract JSON from response (handle potential markdown formatting)
                response_text = response.content if hasattr(response, 'content') else str(response)
                if isinstance(response_text, list):
                    response_text = str(response_text)
                
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                result_dict = json.loads(response_text.strip())
                
                # Map quality string to enum
                quality_map = {
                    "excellent": AnswerQuality.EXCELLENT,
                    "good": AnswerQuality.GOOD,
                    "satisfactory": AnswerQuality.SATISFACTORY,
                    "poor": AnswerQuality.POOR,
                    "incorrect": AnswerQuality.INCORRECT
                }
                
                return JudgmentResult(
                    score=result_dict.get("score", 0),
                    quality=quality_map.get(result_dict.get("quality", "poor"), AnswerQuality.POOR),
                    reasoning=result_dict.get("reasoning", "No reasoning provided"),
                    key_points_covered=result_dict.get("key_points_covered", []),
                    missing_points=result_dict.get("missing_points", []),
                    accuracy_assessment=result_dict.get("accuracy_assessment", "No assessment"),
                    has_hallucination=result_dict.get("has_hallucination", False)
                )
                
            except json.JSONDecodeError as e:
                # Fallback if JSON parsing fails
                return JudgmentResult(
                    score=0,
                    quality=AnswerQuality.INCORRECT,
                    reasoning=f"Failed to parse judge response: {str(e)}",
                    key_points_covered=[],
                    missing_points=[],
                    accuracy_assessment="Evaluation failed",
                    has_hallucination=False
                )
                
        except Exception as e:
            # Handle any errors
            return JudgmentResult(
                score=0,
                quality=AnswerQuality.INCORRECT,
                reasoning=f"Judge evaluation error: {str(e)}",
                key_points_covered=[],
                missing_points=[],
                accuracy_assessment="Evaluation error",
                has_hallucination=False
            )
    
    def evaluate_batch(self, test_cases: list) -> list:
        """Evaluate a batch of test cases."""
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"🧑‍⚖️ Judging question {i}/{len(test_cases)}...")
            
            judgment = self.evaluate_answer(
                test_case.get("question", ""),
                test_case.get("expected_answer", test_case.get("answer", "")),
                test_case.get("given_answer", "")
            )
            
            results.append({
                "question": test_case.get("question", ""),
                "judgment": judgment,
                "original_score": test_case.get("original_score", None)
            })
        
        return results


def create_judge_tool():
    """Create a LangChain tool for the judge agent."""
    from langchain_core.tools import tool
    
    judge = JudgeAgent()
    
    @tool
    def judge_answer_quality(question: str, expected_answer: str, given_answer: str) -> str:
        """Judge the quality and correctness of an answer using LLM evaluation."""
        try:
            judgment = judge.evaluate_answer(question, expected_answer, given_answer)
            
            response = f"**Answer Quality: {judgment.quality.value.upper()}** (Score: {judgment.score}/100)\n\n"
            response += f"**Assessment**: {judgment.reasoning}\n\n"
            
            if judgment.key_points_covered:
                response += f"**Key Points Covered**: {', '.join(judgment.key_points_covered)}\n"
            
            if judgment.missing_points:
                response += f"**Missing Points**: {', '.join(judgment.missing_points)}\n"
            
            response += f"\n**Accuracy**: {judgment.accuracy_assessment}\n"
            
            if judgment.has_hallucination:
                response += "\n⚠️ **Warning**: Potential hallucination detected"
            
            return response
            
        except Exception as e:
            return f"Error in judge evaluation: {str(e)}"
    
    return judge_answer_quality


def main():
    """Test the judge agent with sample cases."""
    judge = JudgeAgent()
    
    # Test case
    test_question = "What is the difference between Wasserstein and Hellinger-Kantorovich distances?"
    
    test_expected = """The Wasserstein distance is a pure transport metric that measures the cost of moving mass 
    while preserving total mass. The Hellinger-Kantorovich distance combines transport with creation/destruction 
    of mass, making it suitable for measures with different total masses."""
    
    test_given = """The Wasserstein distance is about optimal transport of probability measures, while 
    Hellinger-Kantorovich allows for changes in mass during transport."""
    
    print("🧑‍⚖️ Testing Judge Agent")
    print("=" * 60)
    
    result = judge.evaluate_answer(test_question, test_expected, test_given)
    
    print(f"\nScore: {result.score}/100")
    print(f"Quality: {result.quality.value}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Key Points: {result.key_points_covered}")
    print(f"Missing: {result.missing_points}")
    print(f"Hallucination: {result.has_hallucination}")


if __name__ == "__main__":
    main()