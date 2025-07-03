#!/usr/bin/env python3
"""
Complete pipeline for processing an academic paper:
1. Analyze with academic_analyzer
2. Extract metadata with academic_extractor  
3. Store in database
4. Create chunks with entity mapping
5. Generate embeddings

This script processes ONE paper to demonstrate the full pipeline.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import hashlib
import re

from agents.academic_analyzer import AcademicAnalyzer
from agents.academic_extractor import AcademicExtractor
from dotenv import load_dotenv
import tiktoken
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class AcademicPaperPipeline:
    """Complete pipeline for processing academic papers"""
    
    def __init__(self, db_path: str = "DB/metadata.db", use_pro_model: bool = True):
        self.db_path = db_path
        self.use_pro_model = use_pro_model
        
        # Initialize components
        self.analyzer = AcademicAnalyzer(use_pro_model=use_pro_model)
        self.extractor = AcademicExtractor(use_pro_model=use_pro_model)
        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Ensure database exists
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema if not exists"""
        conn = sqlite3.connect(self.db_path)
        
        # Read and execute schema
        schema_path = Path(__file__).parent / "DATABASE_SCHEMA.md"
        if schema_path.exists():
            # Extract SQL from schema file
            with open(schema_path, 'r') as f:
                content = f.read()
            
            # Extract SQL blocks
            sql_blocks = re.findall(r'```sql\n(.*?)\n```', content, re.DOTALL)
            
            for sql_block in sql_blocks:
                try:
                    conn.executescript(sql_block)
                except sqlite3.Error as e:
                    print(f"Schema already exists or error: {e}")
        
        # Add enhanced chunks table if not exists
        conn.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY,
                document_type TEXT NOT NULL,
                document_id INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                section_name TEXT,
                chunk_metadata JSON,
                start_char INTEGER,
                end_char INTEGER,
                token_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(document_type, document_id, chunk_index)
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunk_entities (
                chunk_id INTEGER REFERENCES document_chunks(id),
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                relevance_score FLOAT DEFAULT 1.0,
                PRIMARY KEY (chunk_id, entity_type, entity_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def process_paper(self, paper_path: Path) -> Dict:
        """Process a single paper through the full pipeline"""
        print(f"\n{'='*80}")
        print(f"Processing: {paper_path.name}")
        print(f"{'='*80}\n")
        
        results = {
            'paper': paper_path.name,
            'status': 'started',
            'steps': {}
        }
        
        try:
            # Step 1: Analyze paper
            print("Step 1: Analyzing paper...")
            analysis = self._analyze_paper(paper_path)
            results['steps']['analysis'] = {'status': 'success', 'output_file': str(analysis['output_path'])}
            
            # Step 2: Extract metadata
            print("\nStep 2: Extracting metadata...")
            metadata = self._extract_metadata(analysis['output_path'])
            results['steps']['extraction'] = {'status': 'success', 'entities_found': self._count_entities(metadata)}
            
            # Step 3: Store in database
            print("\nStep 3: Storing in database...")
            doc_id = self._store_in_database(analysis, metadata)
            results['steps']['storage'] = {'status': 'success', 'document_id': doc_id}
            
            # Step 4: Create chunks
            print("\nStep 4: Creating chunks...")
            chunks = self._create_chunks(doc_id, analysis['content'], metadata)
            results['steps']['chunking'] = {'status': 'success', 'chunks_created': len(chunks)}
            
            # Step 5: Generate embeddings
            print("\nStep 5: Generating embeddings...")
            embedding_count = self._generate_embeddings(doc_id, analysis['content'], chunks, metadata)
            results['steps']['embeddings'] = {'status': 'success', 'embeddings_created': embedding_count}
            
            results['status'] = 'success'
            print(f"\n✓ Pipeline completed successfully!")
            
        except Exception as e:
            results['status'] = 'failed'
            results['error'] = str(e)
            print(f"\n✗ Pipeline failed: {e}")
            raise
        
        return results
    
    def _analyze_paper(self, paper_path: Path) -> Dict:
        """Step 1: Analyze paper with academic_analyzer"""
        output_dir = Path("raw_data/academic/generated_analyses")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"{paper_path.stem}_analysis.md"
        
        # Run analyzer
        analysis = self.analyzer.analyze_file(paper_path)
        self.analyzer.save_analysis(analysis, output_path)
        
        # Read the generated content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'output_path': output_path,
            'content': content,
            'analysis_object': analysis
        }
    
    def _extract_metadata(self, analysis_path: Path) -> Dict:
        """Step 2: Extract metadata with academic_extractor"""
        with open(analysis_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self.extractor.extract_metadata(content)
        
        # Save metadata for debugging
        output_path = analysis_path.parent.parent / "extracted_metadata" / f"{analysis_path.stem}_metadata.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata.model_dump(), f, indent=2, ensure_ascii=False)
        
        return metadata.model_dump()
    
    def _store_in_database(self, analysis: Dict, metadata: Dict) -> str:
        """Step 3: Store document and metadata in database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        
        try:
            # Start transaction
            conn.execute("BEGIN")
            
            # 1. Store document
            content_hash = hashlib.sha256(analysis['content'].encode()).hexdigest()
            
            cursor = conn.execute("""
                INSERT INTO academic_documents (
                    file_path, title, date, document_type, domain, 
                    content, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(analysis['output_path']),
                metadata.get('title', 'Unknown'),
                datetime.now().date().isoformat(),
                'analysis',
                metadata.get('domain', 'mathematics'),
                analysis['content'],
                content_hash
            ))
            
            doc_id = cursor.lastrowid
            
            # 2. Store entities and collect their IDs
            entity_ids = {
                'topics': {},
                'people': {},
                'projects': {},
                'institutions': {},
                'methods': {},
                'applications': {}
            }
            
            # Store mathematical concepts as topics
            for concept in metadata.get('mathematical_concepts', []):
                cursor = conn.execute("""
                    INSERT OR IGNORE INTO topics (name, category, description)
                    VALUES (?, ?, ?)
                """, (
                    concept['name'],
                    concept.get('category', 'mathematical'),
                    concept.get('description', '')
                ))
                
                # Get the ID
                result = conn.execute("SELECT id FROM topics WHERE name = ?", (concept['name'],)).fetchone()
                if result:
                    entity_ids['topics'][concept['name']] = result[0]
            
            # Store research areas as topics
            for area in metadata.get('research_areas', []):
                cursor = conn.execute("""
                    INSERT OR IGNORE INTO topics (name, category)
                    VALUES (?, ?)
                """, (area, 'research_area'))
                
                result = conn.execute("SELECT id FROM topics WHERE name = ?", (area,)).fetchone()
                if result:
                    entity_ids['topics'][area] = result[0]
            
            # Store methods
            for method in metadata.get('methods', []):
                cursor = conn.execute("""
                    INSERT OR IGNORE INTO methods (name, category, description)
                    VALUES (?, ?, ?)
                """, (
                    method['name'],
                    method.get('type', 'method'),
                    method.get('description', '')
                ))
                
                result = conn.execute("SELECT id FROM methods WHERE name = ?", (method['name'],)).fetchone()
                if result:
                    entity_ids['methods'][method['name']] = result[0]
            
            # Store people (from authors)
            for author in metadata.get('authors', []):
                cursor = conn.execute("""
                    INSERT OR IGNORE INTO people (name, role)
                    VALUES (?, ?)
                """, (author, 'author'))
                
                result = conn.execute("SELECT id FROM people WHERE name = ?", (author,)).fetchone()
                if result:
                    entity_ids['people'][author] = result[0]
            
            # Store applications
            for app in metadata.get('applications', []):
                if isinstance(app, dict):
                    cursor = conn.execute("""
                        INSERT OR IGNORE INTO applications (name, domain, description)
                        VALUES (?, ?, ?)
                    """, (
                        app.get('name', 'Unknown'),
                        app.get('domain', ''),
                        app.get('description', '')
                    ))
            
            # 3. Create relationships
            # Document -> Topics
            for topic_name, topic_id in entity_ids['topics'].items():
                conn.execute("""
                    INSERT OR IGNORE INTO relationships (
                        source_type, source_id, target_type, target_id, 
                        relationship_type, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, ('document', f'academic_{doc_id}', 'topic', str(topic_id), 'discusses', 1.0))
            
            # Document -> Methods
            for method_name, method_id in entity_ids['methods'].items():
                conn.execute("""
                    INSERT OR IGNORE INTO relationships (
                        source_type, source_id, target_type, target_id,
                        relationship_type, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, ('document', f'academic_{doc_id}', 'method', str(method_id), 'uses_method', 1.0))
            
            # Document -> People (authors)
            for person_name, person_id in entity_ids['people'].items():
                conn.execute("""
                    INSERT OR IGNORE INTO relationships (
                        source_type, source_id, target_type, target_id,
                        relationship_type, confidence
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, ('document', f'academic_{doc_id}', 'person', str(person_id), 'authored_by', 1.0))
            
            # Commit transaction
            conn.commit()
            print(f"✓ Stored document with ID: {doc_id}")
            print(f"  - Topics: {len(entity_ids['topics'])}")
            print(f"  - Methods: {len(entity_ids['methods'])}")
            print(f"  - People: {len(entity_ids['people'])}")
            
            # Return doc_id and entity_ids for chunking phase
            self.entity_ids = entity_ids
            return doc_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _create_chunks(self, doc_id: int, content: str, metadata: Dict) -> List[Dict]:
        """Step 4: Create semantic chunks with entity mapping"""
        chunks = []
        
        # Split by sections (## headers)
        sections = re.split(r'\n## ', content)
        
        # Process each section
        chunk_index = 0
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            # Add back the ## for sections after the first
            if i > 0:
                section = "## " + section
            
            # Extract section name
            lines = section.split('\n')
            section_name = lines[0].replace('#', '').strip() if lines else "Unknown Section"
            
            # Further split large sections into smaller chunks
            section_chunks = self._split_into_chunks(section, max_tokens=1200)
            
            for chunk_text in section_chunks:
                # Count tokens
                token_count = len(self.tokenizer.encode(chunk_text))
                
                # Create chunk metadata
                chunk_metadata = {
                    'section': section_name,
                    'position': 'start' if chunk_index == 0 else 'middle',
                    'has_math': bool(re.search(r'\$.*?\$', chunk_text)),
                    'has_citations': bool(re.search(r'\[[\w\d]+\]', chunk_text))
                }
                
                chunk = {
                    'document_type': 'academic',
                    'document_id': doc_id,
                    'chunk_index': chunk_index,
                    'content': chunk_text,
                    'section_name': section_name,
                    'chunk_metadata': json.dumps(chunk_metadata),
                    'token_count': token_count
                }
                
                chunks.append(chunk)
                chunk_index += 1
        
        # Store chunks in database
        conn = sqlite3.connect(self.db_path)
        try:
            for chunk in chunks:
                cursor = conn.execute("""
                    INSERT INTO document_chunks (
                        document_type, document_id, chunk_index, content,
                        section_name, chunk_metadata, token_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    chunk['document_type'],
                    chunk['document_id'], 
                    chunk['chunk_index'],
                    chunk['content'],
                    chunk['section_name'],
                    chunk['chunk_metadata'],
                    chunk['token_count']
                ))
                
                chunk_id = cursor.lastrowid
                
                # Map entities to chunks
                self._map_entities_to_chunk(conn, chunk_id, chunk['content'])
            
            conn.commit()
            print(f"✓ Created {len(chunks)} chunks")
            
        finally:
            conn.close()
        
        return chunks
    
    def _split_into_chunks(self, text: str, max_tokens: int = 1200) -> List[str]:
        """Split text into chunks respecting token limits and sentence boundaries"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence))
            
            if current_tokens + sentence_tokens > max_tokens and current_chunk:
                # Save current chunk
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _map_entities_to_chunk(self, conn: sqlite3.Connection, chunk_id: int, chunk_content: str):
        """Map entities that appear in this chunk"""
        chunk_lower = chunk_content.lower()
        
        # Check each entity type
        for entity_type, entities in self.entity_ids.items():
            table_name = entity_type  # 'topics', 'methods', etc.
            
            for entity_name, entity_id in entities.items():
                # Simple check: is the entity name in the chunk?
                if entity_name.lower() in chunk_lower:
                    # Calculate relevance based on frequency
                    count = chunk_lower.count(entity_name.lower())
                    relevance = min(1.0, count * 0.2)  # Cap at 1.0
                    
                    conn.execute("""
                        INSERT OR IGNORE INTO chunk_entities (
                            chunk_id, entity_type, entity_id, relevance_score
                        ) VALUES (?, ?, ?, ?)
                    """, (chunk_id, entity_type.rstrip('s'), entity_id, relevance))
    
    def _generate_embeddings(self, doc_id: int, content: str, chunks: List[Dict], metadata: Dict) -> int:
        """Step 5: Generate embeddings for document, chunks, and entities"""
        conn = sqlite3.connect(self.db_path)
        embeddings_created = 0
        
        try:
            # 1. Full document embedding
            print("  - Generating document embedding...")
            doc_embedding = self.embeddings_model.embed_documents([content])[0]
            
            conn.execute("""
                INSERT OR REPLACE INTO embeddings (
                    entity_type, entity_id, embedding, model_name
                ) VALUES (?, ?, ?, ?)
            """, ('document', f'academic_{doc_id}', 
                  json.dumps(doc_embedding), 'text-embedding-3-small'))
            embeddings_created += 1
            
            # 2. Chunk embeddings
            print(f"  - Generating {len(chunks)} chunk embeddings...")
            chunk_texts = [chunk['content'] for chunk in chunks]
            chunk_embeddings = self.embeddings_model.embed_documents(chunk_texts)
            
            for chunk, embedding in zip(chunks, chunk_embeddings):
                # Get chunk ID from database
                result = conn.execute("""
                    SELECT id FROM document_chunks 
                    WHERE document_type = ? AND document_id = ? AND chunk_index = ?
                """, ('academic', doc_id, chunk['chunk_index'])).fetchone()
                
                if result:
                    chunk_db_id = result[0]
                    conn.execute("""
                        INSERT OR REPLACE INTO embeddings (
                            entity_type, entity_id, embedding, model_name
                        ) VALUES (?, ?, ?, ?)
                    """, ('chunk', str(chunk_db_id), 
                          json.dumps(embedding), 'text-embedding-3-small'))
                    embeddings_created += 1
            
            # 3. Entity embeddings (topics and methods)
            print("  - Generating entity embeddings...")
            
            # Topics
            for topic_name, topic_id in self.entity_ids['topics'].items():
                embedding = self.embeddings_model.embed_documents([topic_name])[0]
                conn.execute("""
                    INSERT OR REPLACE INTO embeddings (
                        entity_type, entity_id, embedding, model_name
                    ) VALUES (?, ?, ?, ?)
                """, ('topic', str(topic_id), 
                      json.dumps(embedding), 'text-embedding-3-small'))
                embeddings_created += 1
            
            # Methods
            for method_name, method_id in self.entity_ids['methods'].items():
                embedding = self.embeddings_model.embed_documents([method_name])[0]
                conn.execute("""
                    INSERT OR REPLACE INTO embeddings (
                        entity_type, entity_id, embedding, model_name
                    ) VALUES (?, ?, ?, ?)
                """, ('method', str(method_id),
                      json.dumps(embedding), 'text-embedding-3-small'))
                embeddings_created += 1
            
            conn.commit()
            print(f"✓ Generated {embeddings_created} embeddings")
            
        finally:
            conn.close()
        
        return embeddings_created
    
    def _count_entities(self, metadata: Dict) -> Dict:
        """Count entities in extracted metadata"""
        return {
            'mathematical_concepts': len(metadata.get('mathematical_concepts', [])),
            'methods': len(metadata.get('methods', [])),
            'research_areas': len(metadata.get('research_areas', [])),
            'authors': len(metadata.get('authors', [])),
            'key_insights': len(metadata.get('key_insights', [])),
            'future_work': len(metadata.get('future_work', []))
        }


def main():
    """Run the pipeline on a test paper"""
    # Test with the first paper
    test_paper = Path("raw_data/academic/Transcript_MDs/Cone_geometry_Hellinger_Kantorovich.md")
    
    if not test_paper.exists():
        print(f"Error: Test paper not found at {test_paper}")
        return
    
    # Initialize pipeline
    pipeline = AcademicPaperPipeline(use_pro_model=True)
    
    # Process the paper
    results = pipeline.process_paper(test_paper)
    
    # Print summary
    print(f"\n{'='*80}")
    print("Pipeline Summary")
    print(f"{'='*80}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENROUTER_API_KEY and OPENAI_API_KEY in your .env file")
        exit(1)
    
    main()