#!/usr/bin/env python3
"""
Extract metadata from academic paper analyses
Uses the modular academic extractors to generate JSON files
"""

import sys
from pathlib import Path
import argparse

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.academic_analyzer import AcademicAnalyzer
from agents.academic_metadata_extractor import AcademicExtractor


def main():
    parser = argparse.ArgumentParser(description='Extract metadata from academic papers')
    parser.add_argument('--input', type=Path, 
                       default=Path("raw_data/academic/Transcript_MDs"),
                       help='Input directory with paper transcripts')
    parser.add_argument('--analyses', type=Path,
                       default=Path("raw_data/academic/generated_analyses"),
                       help='Directory with/for paper analyses')
    parser.add_argument('--output', type=Path, 
                       default=Path("raw_data/academic/extracted_metadata"),
                       help='Output directory for metadata JSON files')
    parser.add_argument('--use-pro', action='store_true',
                       help='Use pro model instead of flash')
    parser.add_argument('--skip-analysis', action='store_true',
                       help='Skip analysis phase (use existing analyses)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without extracting')
    
    args = parser.parse_args()
    
    print(f"Academic Metadata Extraction")
    print(f"{'='*60}")
    print(f"Input directory: {args.input}")
    print(f"Analyses directory: {args.analyses}")
    print(f"Output directory: {args.output}")
    print(f"Model: {'pro' if args.use_pro else 'flash'}")
    
    # Ensure output directories exist
    args.analyses.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Find all papers
    papers = list(args.input.glob("*.md"))
    print(f"\nFound {len(papers)} papers to process")
    
    if args.dry_run:
        print("\nDRY RUN - Files that would be processed:")
        for paper in sorted(papers):
            print(f"  - {paper.name}")
        return
    
    # Initialize components
    if not args.skip_analysis:
        analyzer = AcademicAnalyzer(use_pro_model=args.use_pro)
    extractor = AcademicExtractor(use_pro_model=args.use_pro)
    
    successful = 0
    failed = 0
    
    for i, paper_path in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] Processing {paper_path.name}")
        
        try:
            # Step 1: Analyze paper (unless skipped)
            analysis_path = args.analyses / f"{paper_path.stem}_analysis.md"
            
            if not args.skip_analysis:
                print("  Analyzing paper...")
                analysis = analyzer.analyze_file(paper_path)
                analyzer.save_analysis(analysis, str(analysis_path))
                print(f"  ✓ Analysis saved to {analysis_path.name}")
            elif not analysis_path.exists():
                print(f"  ⚠️  Analysis not found at {analysis_path}, skipping")
                failed += 1
                continue
            
            # Step 2: Extract metadata from analysis
            print("  Extracting metadata...")
            output_path = extractor.process_file(analysis_path, args.output)
            
            if output_path:
                print(f"  ✓ Metadata saved to {output_path.name}")
                successful += 1
            else:
                print("  ✗ Metadata extraction failed")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Total papers: {len(papers)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\nNext step: Build database with:")
        print(f"  cd DB && python build_database.py")


if __name__ == "__main__":
    main()