#!/usr/bin/env python3
"""
Extract metadata from all personal notes (formerly chronicle notes)
Uses the modular chronicle_metadata_extractor to generate JSON files
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.chronicle_metadata_extractor import ChronicleMetadataExtractor
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description='Extract metadata from personal notes')
    parser.add_argument('--input', type=Path, default=Path("raw_data/personal_notes"),
                       help='Input directory with personal notes')
    parser.add_argument('--output', type=Path, default=Path("raw_data/personal_notes/extracted_metadata"),
                       help='Output directory for metadata JSON files')
    parser.add_argument('--pattern', default="*.md", help='File pattern to match')
    parser.add_argument('--model', default="google/gemini-2.5-flash", 
                       help='Model to use for extraction')
    parser.add_argument('--show-summary', action='store_true', 
                       help='Display detailed summaries')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be processed without extracting')
    
    args = parser.parse_args()
    
    print(f"Personal Notes Metadata Extraction")
    print(f"{'='*60}")
    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")
    print(f"File pattern: {args.pattern}")
    print(f"Model: {args.model}")
    
    # Find all markdown files
    files = list(args.input.rglob(args.pattern))
    print(f"\nFound {len(files)} files to process")
    
    if args.dry_run:
        print("\nDRY RUN - Files that would be processed:")
        for f in sorted(files):
            print(f"  - {f.relative_to(args.input)}")
        return
    
    # Initialize extractor
    extractor = ChronicleMetadataExtractor(model_name=args.model)
    
    # Process files
    processed = []
    errors = []
    
    for i, file_path in enumerate(sorted(files), 1):
        relative_path = file_path.relative_to(args.input)
        print(f"\n[{i}/{len(files)}] Processing {relative_path}...")
        
        try:
            output_path = extractor.process_file(file_path, args.output)
            if output_path:
                processed.append((file_path, output_path))
                
                if args.show_summary:
                    with open(output_path) as f:
                        metadata = json.load(f)
                    extractor.display_summary(metadata)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            errors.append((file_path, str(e)))
    
    # Summary
    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"✓ Successfully processed: {len(processed)} files")
    print(f"✗ Errors: {len(errors)} files")
    
    if errors:
        print("\nErrors encountered:")
        for file_path, error in errors:
            print(f"  - {file_path.name}: {error}")
    
    # Statistics
    if processed:
        print("\nEntity Statistics:")
        total_topics = 0
        total_projects = 0
        total_people = 0
        total_institutions = 0
        
        for _, output_path in processed:
            with open(output_path) as f:
                metadata = json.load(f)
                total_topics += len(metadata.get('topics', []))
                total_projects += len(metadata.get('projects', []))
                total_people += len(metadata.get('people', []))
                total_institutions += len(metadata.get('institutions', []))
        
        print(f"  - Topics: {total_topics}")
        print(f"  - Projects: {total_projects}")
        print(f"  - People: {total_people}")
        print(f"  - Institutions: {total_institutions}")
    
    print(f"\nMetadata files saved to: {args.output}")


if __name__ == "__main__":
    main()