#!/usr/bin/env python3
"""
Document chunking for academic analysis files.
Splits documents into semantic sections for granular search.
"""

import re
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentChunker:
    """Split documents into searchable chunks."""
    
    def __init__(self, db_path: str = "metadata_system/metadata.db"):
        self.db_path = db_path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def parse_markdown_sections(self, content: str) -> List[Dict[str, str]]:
        """Parse markdown content into sections based on headers."""
        chunks = []
        
        # Split by ## headers (main sections)
        # Pattern matches ## Header with optional trailing #
        section_pattern = r'^##\s+(.+?)(?:\s*#*\s*)?$'
        
        # Find all section headers and their positions
        sections = []
        for match in re.finditer(section_pattern, content, re.MULTILINE):
            sections.append({
                'title': match.group(1).strip(),
                'start': match.start(),
                'header_end': match.end()
            })
        
        # Extract content for each section
        for i, section in enumerate(sections):
            # Content starts after the header
            start = section['header_end']
            
            # Content ends at next section or end of document
            if i + 1 < len(sections):
                end = sections[i + 1]['start']
            else:
                end = len(content)
            
            section_content = content[start:end].strip()
            
            # Skip empty sections
            if not section_content:
                continue
            
            # Determine chunk type based on title
            chunk_type = self._classify_section(section['title'])
            
            chunks.append({
                'title': section['title'],
                'content': section_content,
                'type': chunk_type,
                'order': i
            })
        
        return chunks
    
    def _classify_section(self, title: str) -> str:
        """Classify section type based on title."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['theorem', 'lemma', 'proposition']):
            return 'theorem'
        elif any(word in title_lower for word in ['algorithm', 'method', 'technique']):
            return 'method'
        elif any(word in title_lower for word in ['application', 'use case']):
            return 'application'
        elif any(word in title_lower for word in ['result', 'finding']):
            return 'result'
        elif any(word in title_lower for word in ['contribution', 'innovation']):
            return 'contribution'
        elif any(word in title_lower for word in ['future', 'limitation']):
            return 'future_work'
        else:
            return 'section'
    
    def chunk_academic_document(self, doc_id: int) -> List[int]:
        """Chunk an academic document and store chunks in database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        chunk_ids = []
        
        try:
            # Get document info
            cursor.execute("""
                SELECT file_path, title 
                FROM documents 
                WHERE id = ? AND doc_type = 'academic'
            """, (doc_id,))
            
            doc = cursor.fetchone()
            if not doc:
                logger.warning(f"Document {doc_id} not found or not academic")
                return []
            
            # The file_path already points to the analysis file
            analysis_path = doc['file_path']
            
            if not Path(analysis_path).exists():
                logger.error(f"Analysis file not found: {analysis_path}")
                return []
            
            logger.info(f"Reading analysis file: {analysis_path}")
            
            with open(analysis_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse sections
            chunks = self.parse_markdown_sections(content)
            logger.info(f"Found {len(chunks)} sections in {doc['title']}")
            
            # Store chunks in database
            for chunk in chunks:
                cursor.execute("""
                    INSERT INTO document_chunks 
                    (document_id, chunk_type, chunk_title, chunk_content, chunk_order)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    doc_id,
                    chunk['type'],
                    chunk['title'],
                    chunk['content'],
                    chunk['order']
                ))
                
                chunk_ids.append(cursor.lastrowid)
                logger.debug(f"Created chunk: {chunk['title']} ({chunk['type']})")
            
            conn.commit()
            logger.info(f"Created {len(chunk_ids)} chunks for document {doc_id}")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error chunking document {doc_id}: {e}")
            raise
        finally:
            conn.close()
        
        return chunk_ids
    
    def chunk_all_academic_documents(self) -> Dict[int, List[int]]:
        """Chunk all academic documents that haven't been chunked yet."""
        conn = self.get_connection()
        cursor = conn.cursor()
        results = {}
        
        try:
            # Find academic documents without chunks
            cursor.execute("""
                SELECT d.id, d.title 
                FROM documents d
                WHERE d.doc_type = 'academic'
                AND NOT EXISTS (
                    SELECT 1 FROM document_chunks dc 
                    WHERE dc.document_id = d.id
                )
            """)
            
            documents = cursor.fetchall()
            logger.info(f"Found {len(documents)} academic documents to chunk")
            
            for doc in documents:
                logger.info(f"Chunking: {doc['title']}")
                chunk_ids = self.chunk_academic_document(doc['id'])
                results[doc['id']] = chunk_ids
            
            return results
            
        finally:
            conn.close()
    
    def get_document_chunks(self, doc_id: int) -> List[Dict]:
        """Get all chunks for a document."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, chunk_type, chunk_title, chunk_content, chunk_order
            FROM document_chunks
            WHERE document_id = ?
            ORDER BY chunk_order
        """, (doc_id,))
        
        chunks = []
        for row in cursor.fetchall():
            chunks.append({
                'id': row['id'],
                'type': row['chunk_type'],
                'title': row['chunk_title'],
                'content': row['chunk_content'],
                'order': row['chunk_order']
            })
        
        conn.close()
        return chunks


def test_chunking():
    """Test chunking on one document."""
    chunker = DocumentChunker()
    
    # Get first academic document
    conn = chunker.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM documents 
        WHERE doc_type = 'academic' 
        LIMIT 1
    """)
    doc = cursor.fetchone()
    conn.close()
    
    if doc:
        print(f"\nTesting on: {doc['title']}")
        chunk_ids = chunker.chunk_academic_document(doc['id'])
        
        if chunk_ids:
            print(f"\n✅ Created {len(chunk_ids)} chunks")
            
            # Show the chunks
            chunks = chunker.get_document_chunks(doc['id'])
            for chunk in chunks[:3]:  # Show first 3
                print(f"\n[{chunk['type'].upper()}] {chunk['title']}")
                print(f"Content preview: {chunk['content'][:150]}...")
        else:
            print("❌ No chunks created")
    else:
        print("No academic documents found")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Chunk academic documents")
    parser.add_argument("--test", action="store_true", help="Test on one document")
    parser.add_argument("--all", action="store_true", help="Chunk all academic documents")
    
    args = parser.parse_args()
    
    if args.test:
        test_chunking()
    elif args.all:
        chunker = DocumentChunker()
        results = chunker.chunk_all_academic_documents()
        print(f"\n✅ Chunked {len(results)} documents")
        for doc_id, chunk_ids in results.items():
            print(f"Document {doc_id}: {len(chunk_ids)} chunks")
    else:
        parser.print_help()