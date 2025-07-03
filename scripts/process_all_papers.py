#!/usr/bin/env python3
"""
Process all academic papers through the complete pipeline.
This will analyze, extract metadata, store in database, chunk, and generate embeddings.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from DB.process_paper_pipeline import AcademicPaperPipeline
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

def main():
    """Process all academic papers"""
    # Check for API keys
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY and OPENAI_API_KEY in your .env file")
        exit(1)
    
    # Get all papers
    papers_dir = Path("raw_data/academic/Transcript_MDs")
    if not papers_dir.exists():
        print(f"Error: Papers directory not found at {papers_dir}")
        return
    
    papers = list(papers_dir.glob("*.md"))
    if not papers:
        print("No papers found to process!")
        return
    
    print(f"Found {len(papers)} papers to process")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = AcademicPaperPipeline(use_pro_model=True)
    
    # Process each paper
    results = {
        'start_time': datetime.now().isoformat(),
        'papers': [],
        'summary': {
            'total': len(papers),
            'successful': 0,
            'failed': 0
        }
    }
    
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] Processing: {paper.name}")
        print("-" * 80)
        
        try:
            paper_results = pipeline.process_paper(paper)
            results['papers'].append(paper_results)
            results['summary']['successful'] += 1
        except Exception as e:
            print(f"❌ Failed to process {paper.name}: {e}")
            results['papers'].append({
                'paper': paper.name,
                'status': 'failed',
                'error': str(e)
            })
            results['summary']['failed'] += 1
            # Continue with next paper
            continue
    
    results['end_time'] = datetime.now().isoformat()
    
    # Save results summary
    output_path = Path("academic_processing_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Total papers: {results['summary']['total']}")
    print(f"Successful: {results['summary']['successful']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"\nResults saved to: {output_path}")
    
    if results['summary']['successful'] > 0:
        print("\n✅ Academic database populated successfully!")
        print("\nNext steps:")
        print("1. View database: ./view_database.sh")
        print("2. Generate knowledge graph: python KG/knowledge_graph.py")
        print("3. Query the database: python DB/query_comprehensive.py")

if __name__ == "__main__":
    main()