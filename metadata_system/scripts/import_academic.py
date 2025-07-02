#!/usr/bin/env python3
"""
Import pre-extracted academic metadata from JSON file into the database.
This is a one-time import for academic papers.
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.base import BaseExtractor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AcademicImporter(BaseExtractor):
    """Import academic metadata from JSON file."""
    
    def get_doc_type(self, file_path: Path) -> str:
        """Academic files are always 'academic' type."""
        return "academic"
    
    def extract_metadata(self, file_path: Path, content: str) -> dict:
        """Not used for import - metadata already extracted."""
        pass
    
    def import_paper(self, paper_data: dict) -> int:
        """Import a single paper's metadata."""
        try:
            # Extract file path
            file_path = paper_data['file_path']
            
            # Prepare metadata structure
            metadata = {
                'title': paper_data.get('paper_title', Path(file_path).stem),
                'date': paper_data.get('year'),  # Just year for academic papers
                'authors': paper_data.get('authors', []),
                'venue': paper_data.get('venue', 'Not specified'),
                
                # Core academic content
                'core_contributions': paper_data.get('core_contribution', paper_data.get('core_contributions', [])),
                'problem_solved': paper_data.get('problem_solved'),
                'mathematical_concepts': paper_data.get('mathematical_concepts', []),
                'methods': paper_data.get('methods_and_techniques', paper_data.get('methods', [])),
                'algorithms': paper_data.get('algorithms_introduced', []),
                'theoretical_results': paper_data.get('theoretical_results', []),
                'applications': paper_data.get('applications', []),
                'practical_impact': paper_data.get('practical_impact'),
                
                # Research context
                'research_areas': paper_data.get('research_areas', []),
                'related_concepts': paper_data.get('related_concepts', []),
                'builds_on': paper_data.get('builds_on', []),
                'enables': paper_data.get('enables', []),
                
                # Additional info
                'key_innovations': paper_data.get('key_innovations', []),
                'limitations': paper_data.get('limitations', []),
                'future_directions': paper_data.get('future_directions', []),
                'code_available': paper_data.get('code_available'),
                'datasets_used': paper_data.get('datasets_used', []),
                'key_equations': paper_data.get('key_equations', []),
                
                # For compatibility with chronicle structure
                # Combine research areas and mathematical concepts, removing duplicates
                'topics': list(set(paper_data.get('research_areas', []) + paper_data.get('mathematical_concepts', []))),
                'people': paper_data.get('authors', []),
                'projects': [],  # Academic papers don't have projects
            }
            
            # Generate a content hash (use title + year as proxy)
            content_hash = self.calculate_hash(f"{metadata['title']}_{metadata.get('date', '')}")
            
            # Save to database
            doc_id = self.save_metadata(
                file_path,
                'academic',
                metadata,
                content_hash
            )
            
            return doc_id
            
        except Exception as e:
            logger.error(f"Error importing paper {paper_data.get('title', 'Unknown')}: {e}")
            return None


def import_academic_metadata(json_path: str, db_path: str = "metadata_system/metadata.db"):
    """Import all academic metadata from JSON file."""
    
    # Verify paths
    json_file = Path(json_path)
    if not json_file.exists():
        logger.error(f"JSON file does not exist: {json_file}")
        return 1
    
    db_file = Path(db_path)
    if not db_file.exists():
        logger.error(f"Database does not exist: {db_file}")
        logger.info("Run setup_db.py first to create the database")
        return 1
    
    logger.info("="*60)
    logger.info("Academic Metadata Import Starting")
    logger.info(f"JSON file: {json_file.resolve()}")
    logger.info(f"Database path: {db_file.resolve()}")
    logger.info("="*60)
    
    try:
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            academic_data = json.load(f)
        
        papers = academic_data.get('papers', [])
        logger.info(f"Found {len(papers)} papers to import")
        
        # Create importer
        importer = AcademicImporter(db_path)
        
        # Import each paper
        successful_imports = 0
        for i, paper in enumerate(papers, 1):
            logger.info(f"Importing paper {i}/{len(papers)}: {paper.get('title', 'Unknown')}")
            doc_id = importer.import_paper(paper)
            if doc_id:
                successful_imports += 1
                logger.info(f"  ✓ Imported with ID: {doc_id}")
            else:
                logger.error(f"  ✗ Failed to import")
        
        # Summary statistics
        logger.info("="*60)
        logger.info("Import Summary")
        logger.info(f"Total papers processed: {len(papers)}")
        logger.info(f"Successfully imported: {successful_imports}")
        logger.info(f"Failed: {len(papers) - successful_imports}")
        
        if successful_imports > 0:
            # Get some statistics from database
            conn = importer.get_connection()
            cursor = conn.cursor()
            
            # Count academic documents
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'academic'")
            academic_count = cursor.fetchone()[0]
            
            # Count unique research areas (topics)
            cursor.execute("""
                SELECT COUNT(DISTINCT t.name) 
                FROM topics t
                JOIN document_topics dt ON t.id = dt.topic_id
                JOIN documents d ON dt.document_id = d.id
                WHERE d.doc_type = 'academic'
            """)
            research_area_count = cursor.fetchone()[0]
            
            conn.close()
            
            logger.info(f"Total academic papers in database: {academic_count}")
            logger.info(f"Research areas/topics: {research_area_count}")
        
        logger.info("="*60)
        
        if successful_imports == len(papers):
            logger.info("✅ Academic import completed successfully!")
            return 0
        else:
            logger.warning("⚠️  Academic import completed with some failures")
            return 1
        
    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import academic metadata from JSON file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "json_path",
        help="Path to academic_metadata.json file"
    )
    
    parser.add_argument(
        "--db-path",
        default="metadata_system/metadata.db",
        help="Path to SQLite database"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run import
    exit_code = import_academic_metadata(args.json_path, args.db_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()