#!/usr/bin/env python3
"""
Import existing chronicle files into the metadata database.
This is a one-time import script for initial population.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extractors.chronicle import ChronicleExtractor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def import_chronicle_files(chronicle_path: str, db_path: str = "metadata_system/metadata.db"):
    """Import all chronicle files into the database."""
    
    # Verify paths
    chronicle_dir = Path(chronicle_path)
    if not chronicle_dir.exists():
        logger.error(f"Chronicle path does not exist: {chronicle_dir}")
        return 1
    
    db_file = Path(db_path)
    if not db_file.exists():
        logger.error(f"Database does not exist: {db_file}")
        logger.info("Run setup_db.py first to create the database")
        return 1
    
    logger.info("="*60)
    logger.info("Chronicle Import Starting")
    logger.info(f"Chronicle path: {chronicle_dir.resolve()}")
    logger.info(f"Database path: {db_file.resolve()}")
    logger.info("="*60)
    
    try:
        # Create extractor
        extractor = ChronicleExtractor(db_path)
        
        # Process all files
        processed_ids = extractor.process_chronicle_folder(str(chronicle_dir))
        
        # Summary statistics
        logger.info("="*60)
        logger.info("Import Summary")
        logger.info(f"Total files processed: {len(processed_ids)}")
        
        if processed_ids:
            # Get some statistics from database
            conn = extractor.get_connection()
            cursor = conn.cursor()
            
            # Count topics
            cursor.execute("SELECT COUNT(DISTINCT name) FROM topics")
            topic_count = cursor.fetchone()[0]
            
            # Count people
            cursor.execute("SELECT COUNT(DISTINCT name) FROM people")
            people_count = cursor.fetchone()[0]
            
            # Count projects
            cursor.execute("SELECT COUNT(DISTINCT name) FROM projects")
            project_count = cursor.fetchone()[0]
            
            conn.close()
            
            logger.info(f"Topics extracted: {topic_count}")
            logger.info(f"People identified: {people_count}")
            logger.info(f"Projects found: {project_count}")
        
        logger.info("="*60)
        logger.info("✅ Chronicle import completed successfully!")
        
        return 0
        
    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import chronicle files into metadata database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "chronicle_path",
        help="Path to chronicle folder"
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
    exit_code = import_chronicle_files(args.chronicle_path, args.db_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()