#!/usr/bin/env python3
"""
Process chronicle notes (daily, weekly, monthly) through the extraction pipeline.
Uses the chronicle extractor to extract metadata and populate the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from datetime import datetime
import json
import sqlite3
import hashlib
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Import the chronicle extractor
from DB.extractors.chronicle import ChronicleExtractor

load_dotenv()


class ChronicleProcessor:
    """Processes chronicle notes and stores them in the database"""
    
    def __init__(self, db_path: str = "DB/metadata.db"):
        self.db_path = db_path
        self.extractor = ChronicleExtractor(db_path)
        
    def process_chronicle_notes(self, chronicle_base_path: Path) -> Dict:
        """Process all chronicle notes in the given path"""
        results = {
            'start_time': datetime.now().isoformat(),
            'notes_processed': {
                'daily': [],
                'weekly': [],
                'monthly': []
            },
            'summary': {
                'total': 0,
                'successful': 0,
                'failed': 0
            }
        }
        
        # Process daily notes
        daily_path = chronicle_base_path / "Daily Notes"
        if daily_path.exists():
            daily_notes = list(daily_path.glob("*.md"))
            print(f"\nFound {len(daily_notes)} daily notes")
            for note in daily_notes:
                result = self._process_single_note(note, 'daily')
                results['notes_processed']['daily'].append(result)
                results['summary']['total'] += 1
                if result['status'] == 'success':
                    results['summary']['successful'] += 1
                else:
                    results['summary']['failed'] += 1
        
        # Process weekly notes
        weekly_path = chronicle_base_path / "Weekly Notes"
        if weekly_path.exists():
            weekly_notes = list(weekly_path.glob("*.md"))
            print(f"\nFound {len(weekly_notes)} weekly notes")
            for note in weekly_notes:
                result = self._process_single_note(note, 'weekly')
                results['notes_processed']['weekly'].append(result)
                results['summary']['total'] += 1
                if result['status'] == 'success':
                    results['summary']['successful'] += 1
                else:
                    results['summary']['failed'] += 1
        
        # Process monthly notes
        monthly_path = chronicle_base_path / "Monthly Notes"
        if monthly_path.exists():
            monthly_notes = list(monthly_path.glob("*.md"))
            print(f"\nFound {len(monthly_notes)} monthly notes")
            for note in monthly_notes:
                result = self._process_single_note(note, 'monthly')
                results['notes_processed']['monthly'].append(result)
                results['summary']['total'] += 1
                if result['status'] == 'success':
                    results['summary']['successful'] += 1
                else:
                    results['summary']['failed'] += 1
        
        results['end_time'] = datetime.now().isoformat()
        return results
    
    def _process_single_note(self, note_path: Path, note_type: str) -> Dict:
        """Process a single chronicle note"""
        print(f"\nProcessing {note_type} note: {note_path.name}")
        
        try:
            # Process the file using the extractor
            print(f"  → Processing with extractor...")
            doc_id = self.extractor.process_file(note_path)
            
            if doc_id:
                print(f"  ✓ Stored with ID: {doc_id}")
                
                # Get entity counts from database
                conn = sqlite3.connect(self.db_path)
                entity_counts = self._get_entity_counts_for_document(conn, doc_id)
                conn.close()
                
                print(f"    - Topics: {entity_counts['topics']}")
                print(f"    - Projects: {entity_counts['projects']}")
                print(f"    - People: {entity_counts['people']}")
                
                return {
                    'file': note_path.name,
                    'status': 'success',
                    'document_id': doc_id,
                    'entities_extracted': entity_counts
                }
            else:
                print(f"  → Skipped (unchanged or already processed)")
                return {
                    'file': note_path.name,
                    'status': 'skipped',
                    'reason': 'unchanged'
                }
            
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            return {
                'file': note_path.name,
                'status': 'failed',
                'error': str(e)
            }
    
    def _get_entity_counts_for_document(self, conn: sqlite3.Connection, doc_id: int) -> Dict[str, int]:
        """Get entity counts for a document from the database"""
        counts = {}
        
        # Count topics
        cursor = conn.execute("""
            SELECT COUNT(DISTINCT target_id) 
            FROM relationships 
            WHERE source_type = 'document' 
            AND source_id = ? 
            AND target_type = 'topic'
        """, (f'chronicle_{doc_id}',))
        counts['topics'] = cursor.fetchone()[0]
        
        # Count projects
        cursor = conn.execute("""
            SELECT COUNT(DISTINCT target_id) 
            FROM relationships 
            WHERE source_type = 'document' 
            AND source_id = ? 
            AND target_type = 'project'
        """, (f'chronicle_{doc_id}',))
        counts['projects'] = cursor.fetchone()[0]
        
        # Count people
        cursor = conn.execute("""
            SELECT COUNT(DISTINCT target_id) 
            FROM relationships 
            WHERE source_type = 'document' 
            AND source_id = ? 
            AND target_type = 'person'
        """, (f'chronicle_{doc_id}',))
        counts['people'] = cursor.fetchone()[0]
        
        return counts


def main():
    """Main function to process chronicle notes"""
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY in your .env file")
        exit(1)
    
    # Set up paths
    chronicle_path = Path("raw_data/chronicle")
    
    if not chronicle_path.exists():
        print(f"Error: Chronicle path not found: {chronicle_path}")
        exit(1)
    
    print("Chronicle Note Processing Pipeline")
    print("=" * 80)
    
    # Initialize processor
    processor = ChronicleProcessor()
    
    # Process all notes
    results = processor.process_chronicle_notes(chronicle_path)
    
    # Save results
    output_path = Path("chronicle_processing_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"Total notes: {results['summary']['total']}")
    print(f"Successful: {results['summary']['successful']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"\nResults saved to: {output_path}")
    
    if results['summary']['successful'] > 0:
        print("\n✅ Chronicle notes processed successfully!")
        print("\nNext steps:")
        print("1. Generate embeddings: python DB/embeddings.py")
        print("2. View database: ./view_database.sh")
        print("3. Generate knowledge graph: python KG/knowledge_graph.py DB/metadata.db")
        print("4. Query with interactive agent: python interactive_agent.py")


if __name__ == "__main__":
    main()