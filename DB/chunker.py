#!/usr/bin/env python3
"""
Document chunking module for the Interactive CV project
Implements smart chunking with entity preservation
"""

import re
import sqlite3
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import tiktoken


class DocumentChunker:
    """Chunks documents intelligently while preserving entity context"""
    
    def __init__(self, 
                 chunk_size: int = 1200,
                 chunk_overlap: int = 200,
                 min_chunk_size: int = 500,
                 model: str = "gpt-3.5-turbo"):
        """
        Initialize the chunker
        
        Args:
            chunk_size: Target size in tokens (default 1200)
            chunk_overlap: Overlap between chunks in tokens (default 200)
            min_chunk_size: Minimum chunk size to avoid tiny fragments
            model: Model to use for tokenization
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.tokenizer = tiktoken.encoding_for_model(model)
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def find_section_boundaries(self, content: str) -> List[Tuple[int, int, str]]:
        """
        Find section boundaries in markdown content
        Returns list of (start_pos, end_pos, section_name)
        """
        # Pattern for markdown headers (# Title, ## Subtitle, etc.)
        header_pattern = r'^(#{1,6})\s+(.+?)$'
        
        sections = []
        current_section = "Introduction"
        current_start = 0
        
        lines = content.split('\n')
        position = 0
        
        for i, line in enumerate(lines):
            match = re.match(header_pattern, line.strip())
            if match:
                # Save previous section
                if position > current_start:
                    sections.append((current_start, position, current_section))
                
                # Start new section
                level = len(match.group(1))
                current_section = match.group(2).strip()
                current_start = position
            
            position += len(line) + 1  # +1 for newline
        
        # Add final section
        if current_start < len(content):
            sections.append((current_start, len(content), current_section))
        
        return sections
    
    def split_by_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split by double newlines, but preserve single newlines within paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def create_chunks_from_section(self, 
                                 section_text: str, 
                                 section_name: str,
                                 start_char: int) -> List[Dict[str, Any]]:
        """
        Create chunks from a section, trying to preserve paragraph boundaries
        """
        chunks = []
        paragraphs = self.split_by_paragraphs(section_text)
        
        if not paragraphs:
            return chunks
        
        current_chunk = f"## {section_name}\n\n"
        current_tokens = self.count_tokens(current_chunk)
        chunk_start = start_char
        
        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            # If paragraph itself is too large, split it
            if para_tokens > self.chunk_size:
                # Save current chunk if it has content
                if current_tokens > self.count_tokens(f"## {section_name}\n\n"):
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_name': section_name,
                        'start_char': chunk_start,
                        'end_char': chunk_start + len(current_chunk),
                        'token_count': current_tokens
                    })
                
                # Split large paragraph by sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current_chunk = f"## {section_name}\n\n"
                current_tokens = self.count_tokens(current_chunk)
                chunk_start = start_char + len(section_text) - len(para)
                
                for sent in sentences:
                    sent_tokens = self.count_tokens(sent)
                    if current_tokens + sent_tokens > self.chunk_size and current_tokens > self.min_chunk_size:
                        chunks.append({
                            'content': current_chunk.strip(),
                            'section_name': section_name,
                            'start_char': chunk_start,
                            'end_char': chunk_start + len(current_chunk),
                            'token_count': current_tokens
                        })
                        current_chunk = f"## {section_name}\n\n{sent} "
                        current_tokens = self.count_tokens(current_chunk)
                        chunk_start += len(current_chunk)
                    else:
                        current_chunk += sent + " "
                        current_tokens += sent_tokens
            
            # Normal paragraph processing
            elif current_tokens + para_tokens > self.chunk_size:
                # Save current chunk
                if current_tokens > self.min_chunk_size:
                    chunks.append({
                        'content': current_chunk.strip(),
                        'section_name': section_name,
                        'start_char': chunk_start,
                        'end_char': chunk_start + len(current_chunk),
                        'token_count': current_tokens
                    })
                    # Start new chunk with overlap (last paragraph of previous chunk)
                    if chunks and self.chunk_overlap > 0:
                        # Find last paragraph of previous chunk
                        prev_paragraphs = self.split_by_paragraphs(chunks[-1]['content'])
                        if prev_paragraphs:
                            overlap_text = prev_paragraphs[-1]
                            current_chunk = f"## {section_name}\n\n{overlap_text}\n\n{para}\n\n"
                    else:
                        current_chunk = f"## {section_name}\n\n{para}\n\n"
                    
                    current_tokens = self.count_tokens(current_chunk)
                    chunk_start = start_char + len(section_text) - len(para)
            else:
                current_chunk += para + "\n\n"
                current_tokens += para_tokens
        
        # Add final chunk
        if current_tokens > self.min_chunk_size:
            chunks.append({
                'content': current_chunk.strip(),
                'section_name': section_name,
                'start_char': chunk_start,
                'end_char': start_char + len(section_text),
                'token_count': current_tokens
            })
        
        return chunks
    
    def chunk_document(self, content: str, preserve_sections: bool = True) -> List[Dict[str, Any]]:
        """
        Chunk a document into semantic segments
        
        Args:
            content: Document content
            preserve_sections: Whether to try to preserve section boundaries
            
        Returns:
            List of chunk dictionaries with content and metadata
        """
        if not content:
            return []
        
        chunks = []
        
        if preserve_sections:
            # Find sections and chunk each separately
            sections = self.find_section_boundaries(content)
            
            for start, end, section_name in sections:
                section_text = content[start:end]
                section_chunks = self.create_chunks_from_section(
                    section_text, section_name, start
                )
                chunks.extend(section_chunks)
        else:
            # Simple paragraph-based chunking
            chunks = self.create_chunks_from_section(
                content, "Document", 0
            )
        
        # Add chunk indices
        for i, chunk in enumerate(chunks):
            chunk['chunk_index'] = i
        
        return chunks
    
    def chunk_and_store(self, 
                       db_path: str,
                       doc_id: int,
                       doc_type: str,
                       content: str,
                       preserve_sections: bool = True) -> List[int]:
        """
        Chunk a document and store chunks in database
        
        Args:
            db_path: Path to database
            doc_id: Document ID
            doc_type: Document type (academic or chronicle)
            content: Document content
            preserve_sections: Whether to preserve section boundaries
            
        Returns:
            List of chunk IDs created
        """
        chunks = self.chunk_document(content, preserve_sections)
        
        if not chunks:
            return []
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        chunk_ids = []
        
        try:
            # Clear existing chunks for this document
            cursor.execute("""
                DELETE FROM document_chunks 
                WHERE document_type = ? AND document_id = ?
            """, (doc_type, doc_id))
            
            # Insert new chunks
            for chunk in chunks:
                cursor.execute("""
                    INSERT INTO document_chunks 
                    (document_type, document_id, chunk_index, content, 
                     section_name, chunk_metadata, start_char, end_char, token_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc_type,
                    doc_id,
                    chunk['chunk_index'],
                    chunk['content'],
                    chunk['section_name'],
                    '{}',  # Empty metadata for now
                    chunk['start_char'],
                    chunk['end_char'],
                    chunk['token_count']
                ))
                chunk_ids.append(cursor.lastrowid)
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        
        return chunk_ids
    
    def map_entities_to_chunks(self,
                             db_path: str,
                             doc_id: int,
                             doc_type: str) -> int:
        """
        Map entities mentioned in document to specific chunks
        This creates entries in chunk_entities table
        
        Returns:
            Number of entity-chunk mappings created
        """
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Get all chunks for this document
            cursor.execute("""
                SELECT id, content FROM document_chunks
                WHERE document_type = ? AND document_id = ?
                ORDER BY chunk_index
            """, (doc_type, doc_id))
            chunks = cursor.fetchall()
            
            # Get all entities related to this document
            unified_doc_id = f"{doc_type}_{doc_id}"
            cursor.execute("""
                SELECT DISTINCT target_type, target_id 
                FROM relationships
                WHERE source_type = 'document' AND source_id = ?
            """, (unified_doc_id,))
            entities = cursor.fetchall()
            
            # Clear existing mappings
            chunk_ids = [c[0] for c in chunks]
            if chunk_ids:
                placeholders = ','.join('?' * len(chunk_ids))
                cursor.execute(f"""
                    DELETE FROM chunk_entities 
                    WHERE chunk_id IN ({placeholders})
                """, chunk_ids)
            
            # Map entities to chunks
            mappings_created = 0
            
            for chunk_id, chunk_content in chunks:
                chunk_lower = chunk_content.lower()
                
                for entity_type, entity_id in entities:
                    # Get entity name
                    table_map = {
                        'topic': 'topics',
                        'person': 'people',
                        'project': 'projects',
                        'institution': 'institutions',
                        'method': 'methods',
                        'application': 'applications'
                    }
                    
                    table = table_map.get(entity_type, 'topics')
                    cursor.execute(f"SELECT name FROM {table} WHERE id = ?", (entity_id,))
                    result = cursor.fetchone()
                    
                    if result:
                        entity_name = result[0].lower()
                        
                        # Check if entity is mentioned in chunk
                        # Simple substring match for now, could be improved
                        if entity_name in chunk_lower:
                            # Calculate relevance based on frequency
                            occurrences = chunk_lower.count(entity_name)
                            relevance = min(1.0, occurrences * 0.2)  # Cap at 1.0
                            
                            cursor.execute("""
                                INSERT OR IGNORE INTO chunk_entities
                                (chunk_id, entity_type, entity_id, relevance_score)
                                VALUES (?, ?, ?, ?)
                            """, (chunk_id, entity_type, int(entity_id), relevance))
                            
                            mappings_created += 1
            
            conn.commit()
            return mappings_created
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


