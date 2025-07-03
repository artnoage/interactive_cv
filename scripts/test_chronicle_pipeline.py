#!/usr/bin/env python3
"""
Test the chronicle processing pipeline on a single note first.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from scripts.process_chronicle_notes import ChronicleProcessor
from dotenv import load_dotenv

load_dotenv()


def main():
    """Test the chronicle pipeline on one note"""
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    # Get the first daily note for testing
    daily_notes_path = Path("raw_data/chronicle/Daily Notes")
    if not daily_notes_path.exists():
        print(f"Error: Daily notes path not found: {daily_notes_path}")
        return
    
    notes = list(daily_notes_path.glob("*.md"))
    if not notes:
        print("No daily notes found!")
        return
    
    # Test with the first note
    test_note = notes[0]
    
    print("Testing chronicle pipeline on single note...")
    print(f"Note: {test_note.name}")
    print("=" * 80)
    
    # Initialize processor
    processor = ChronicleProcessor()
    
    # Process the single note
    try:
        result = processor._process_single_note(test_note, 'daily')
        print("\n✅ Pipeline test successful!")
        print(f"\nResult: {result}")
        
        if result['status'] == 'success':
            print("\nYou can now run scripts/process_chronicle_notes.py to process all notes.")
    except Exception as e:
        print(f"\n❌ Pipeline test failed: {e}")
        print("\nPlease fix the error before running the full pipeline.")
        raise


if __name__ == "__main__":
    main()