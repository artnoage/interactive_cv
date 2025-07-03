#!/usr/bin/env python3
"""
Test the academic paper pipeline on a single paper first.
This helps verify everything is working before processing all papers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from DB.process_paper_pipeline import AcademicPaperPipeline
from dotenv import load_dotenv

load_dotenv()

def main():
    """Test the pipeline on one paper"""
    # Check for API keys
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY and OPENAI_API_KEY in your .env file")
        exit(1)
    
    # Test with the third paper (Exit_time_risk_sensitive_control)
    test_paper = Path("raw_data/academic/Transcript_MDs/Exit_time_risk_sensitive_control.md")
    
    if not test_paper.exists():
        print(f"Error: Test paper not found at {test_paper}")
        return
    
    print("Testing academic pipeline on single paper...")
    print(f"Paper: {test_paper.name}")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = AcademicPaperPipeline(use_pro_model=True)
    
    # Process the paper
    try:
        results = pipeline.process_paper(test_paper)
        print("\n✅ Pipeline test successful!")
        print("\nYou can now run scripts/process_all_papers.py to process all papers.")
    except Exception as e:
        print(f"\n❌ Pipeline test failed: {e}")
        print("\nPlease fix the error before running the full pipeline.")
        raise

if __name__ == "__main__":
    main()