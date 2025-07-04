#!/usr/bin/env python3
"""
Entity deduplication agent using Gemini 2.5 Flash.
Finds and merges duplicate entities in the knowledge graph.
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import difflib
from datetime import datetime
import json
from collections import defaultdict

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Load environment variables
load_dotenv()


class DuplicateVerification(BaseModel):
    """Schema for duplicate verification response."""
    are_same: bool = Field(description="Whether the entities are the same")
    explanation: str = Field(description="Brief explanation (1 line)")
    canonical_name: Optional[str] = Field(
        description="If same, the preferred name to keep", 
        default=None
    )


class EntityDeduplicator:
    """Deduplicate entities using string matching, embeddings, and LLM verification."""
    
    def __init__(self, db_path: str = "DB/metadata.db", similarity_threshold: float = 0.85):
        self.db_path = db_path
        self.similarity_threshold = similarity_threshold
        
        # Initialize Gemini 2.5 Flash
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
            
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
            model="google/gemini-2.5-flash",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Entity Deduplicator",
            },
            temperature=0.1,
        )
        
        self.parser = PydanticOutputParser(pydantic_object=DuplicateVerification)
        
        # Audit log
        self.audit_log = []
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_entity_context(self, entity_type: str, entity_id: int) -> Dict:
        """Get context for an entity including related documents."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get entity details
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        
        table = table_map[entity_type]
        cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (entity_id,))
        entity = dict(cursor.fetchone())
        
        # Get related documents
        cursor.execute("""
            SELECT r.source_id, r.relationship_type
            FROM relationships r
            WHERE r.target_type = ? AND r.target_id = ?
            AND r.source_type = 'document'
            LIMIT 5
        """, (entity_type, str(entity_id)))
        
        docs = []
        for rel in cursor.fetchall():
            doc_type, doc_id = rel['source_id'].split('_')
            table = f"{doc_type}_documents"
            cursor.execute(f"SELECT title FROM {table} WHERE id = ?", (doc_id,))
            doc = cursor.fetchone()
            if doc:
                docs.append(doc['title'])
        
        entity['related_documents'] = docs
        
        # Get relationship count
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM relationships
            WHERE (target_type = ? AND target_id = ?)
            OR (source_type = ? AND source_id = ?)
        """, (entity_type, str(entity_id), entity_type, str(entity_id)))
        
        entity['relationship_count'] = cursor.fetchone()['cnt']
        
        conn.close()
        return entity
    
    def find_string_duplicates(self, entity_type: str) -> List[Tuple[int, int, float]]:
        """Find potential duplicates using string similarity."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        
        table = table_map[entity_type]
        
        # Get all entities
        cursor.execute(f"SELECT id, name FROM {table} ORDER BY name")
        entities = [(row['id'], row['name']) for row in cursor.fetchall()]
        
        candidates = []
        
        # Find exact matches (case-insensitive)
        name_to_ids = defaultdict(list)
        for entity_id, name in entities:
            name_to_ids[name.lower()].append((entity_id, name))
        
        for _, items in name_to_ids.items():
            if len(items) > 1:
                # Add all pairs of exact matches
                for i in range(len(items)):
                    for j in range(i + 1, len(items)):
                        candidates.append((items[i][0], items[j][0], 1.0))
        
        # Find fuzzy matches
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                id1, name1 = entities[i]
                id2, name2 = entities[j]
                
                # Skip if already added as exact match
                if name1.lower() == name2.lower():
                    continue
                
                # Calculate similarity
                ratio = difflib.SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
                
                # Entity-specific thresholds
                threshold = {
                    'person': 0.9,      # Names need high similarity
                    'institution': 0.9,  # Organizations too
                    'topic': 0.85,      # Some variation expected
                    'method': 0.85,
                    'project': 0.8,
                    'application': 0.8
                }.get(entity_type, 0.85)
                
                if ratio >= threshold:
                    candidates.append((id1, id2, ratio))
        
        conn.close()
        return sorted(candidates, key=lambda x: x[2], reverse=True)
    
    def find_embedding_duplicates(self, entity_type: str) -> List[Tuple[int, int, float]]:
        """Find potential duplicates using embedding similarity."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get all embeddings for this entity type
        cursor.execute("""
            SELECT entity_id, embedding
            FROM embeddings
            WHERE entity_type = ?
        """, (entity_type,))
        
        embeddings = []
        entity_ids = []
        
        for row in cursor.fetchall():
            # Extract numeric ID from entity_id (e.g., "topic_123" -> 123)
            numeric_id = int(row['entity_id'].split('_')[1])
            entity_ids.append(numeric_id)
            
            # Convert bytes to numpy array
            embedding = np.frombuffer(row['embedding'], dtype=np.float32)
            embeddings.append(embedding)
        
        candidates = []
        
        # Calculate pairwise cosine similarities
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                # Cosine similarity
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                
                if similarity >= self.similarity_threshold:
                    candidates.append((entity_ids[i], entity_ids[j], float(similarity)))
        
        conn.close()
        return sorted(candidates, key=lambda x: x[2], reverse=True)
    
    def find_duplicate_clusters(self, candidates: List[Tuple[int, int, float]]) -> List[Dict]:
        """Group transitively connected duplicates into clusters."""
        # Build adjacency list
        graph = defaultdict(set)
        scores = {}
        
        for id1, id2, score in candidates:
            graph[id1].add(id2)
            graph[id2].add(id1)
            key = (min(id1, id2), max(id1, id2))
            scores[key] = score
        
        # Find connected components using DFS
        visited = set()
        clusters = []
        
        def dfs(node, cluster):
            visited.add(node)
            cluster.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, cluster)
        
        for node in graph:
            if node not in visited:
                cluster = set()
                dfs(node, cluster)
                if len(cluster) > 1:  # Only keep actual duplicates
                    clusters.append({
                        'ids': sorted(list(cluster)),
                        'pairs': [(a, b, scores.get((min(a,b), max(a,b)), 0)) 
                                 for i, a in enumerate(cluster) 
                                 for b in list(cluster)[i+1:]]
                    })
        
        return sorted(clusters, key=lambda x: len(x['ids']), reverse=True)
    
    def choose_canonical_entity(self, entity_type: str, entity_ids: List[int]) -> Tuple[int, str]:
        """Choose the best entity from a cluster to keep."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        table = table_map[entity_type]
        
        # Get all entities
        entities = []
        for entity_id in entity_ids:
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (entity_id,))
            entity = dict(cursor.fetchone())
            
            # Get relationship count
            cursor.execute("""
                SELECT COUNT(*) as cnt FROM relationships
                WHERE (target_type = ? AND target_id = ?)
                OR (source_type = ? AND source_id = ?)
            """, (entity_type, str(entity_id), entity_type, str(entity_id)))
            entity['relationship_count'] = cursor.fetchone()['cnt']
            
            entities.append(entity)
        
        conn.close()
        
        # Score each entity
        scored_entities = []
        for entity in entities:
            score = 0
            name = entity['name']
            
            # 1. Relationship count (most important)
            score += entity['relationship_count'] * 100
            
            # 2. Proper capitalization
            if name[0].isupper():
                score += 50
            
            # 3. No kebab-case or underscores
            if '-' not in name and '_' not in name:
                score += 30
            
            # 4. Proper spacing after punctuation
            if '. ' in name:
                score += 20
            elif '.' in name and not name.endswith('.'):
                score -= 10
            
            # 5. Length (prefer more complete names)
            score += len(name) * 0.1
            
            # 6. Has additional metadata
            if entity.get('description'):
                score += 10
            if entity.get('category') or entity.get('role') or entity.get('affiliation'):
                score += 10
            
            scored_entities.append((entity['id'], entity['name'], score))
        
        # Sort by score (highest first), then by name for consistency
        scored_entities.sort(key=lambda x: (-x[2], x[1]))
        
        return scored_entities[0][0], scored_entities[0][1]
    
    def verify_duplicate(self, entity_type: str, id1: int, id2: int) -> DuplicateVerification:
        """Use LLM to verify if two entities are duplicates."""
        # Get entity contexts
        entity1 = self.get_entity_context(entity_type, id1)
        entity2 = self.get_entity_context(entity_type, id2)
        
        # Get entity categories for context
        conn = self.get_connection()
        cursor = conn.cursor()
        table = {'topic': 'topics'}.get(entity_type)
        categories = []
        if table:
            cursor.execute(f"SELECT DISTINCT category FROM {table} WHERE category IS NOT NULL LIMIT 10")
            categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        
        # Build prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are helping deduplicate entities in an Interactive CV knowledge graph system.

Context: This database contains entities extracted from academic papers and personal notes by Vaios Laschos,
a mathematician transitioning to ML/AI. The system tracks research topics, collaborators, methods, and projects.

Entity type: {entity_type}
{categories_section}

Your task: Determine if these two {entity_type} entities refer to the same thing.
Consider variations in naming, abbreviations, and context.

{format_instructions}"""),
            ("user", """Are these two {entity_type} entities the same?

Entity 1: "{name1}"
{attrs1}
Appears in: {docs1}
Relationships: {rel_count1}

Entity 2: "{name2}"
{attrs2}
Appears in: {docs2}
Relationships: {rel_count2}

Answer with: YES (if same entity) or NO (if different).
If YES, provide the canonical_name (the best name to keep).
Brief explanation (1 line).""")
        ])
        
        # Format attributes
        def format_attrs(entity):
            attrs = []
            for key, val in entity.items():
                if key not in ['id', 'name', 'related_documents', 'relationship_count', 'created_at'] and val:
                    attrs.append(f"{key}: {val}")
            return '\n'.join(attrs) if attrs else "No additional attributes"
        
        # Prepare categories section
        categories_section = ""
        if categories:
            categories_section = f"Common categories: {', '.join(categories)}"
        
        # Execute chain
        chain = prompt | self.llm | self.parser
        
        result = chain.invoke({
            'entity_type': entity_type,
            'categories_section': categories_section,
            'name1': entity1['name'],
            'attrs1': format_attrs(entity1),
            'docs1': ', '.join(entity1['related_documents'][:3]) if entity1['related_documents'] else "No documents",
            'rel_count1': entity1['relationship_count'],
            'name2': entity2['name'],
            'attrs2': format_attrs(entity2),
            'docs2': ', '.join(entity2['related_documents'][:3]) if entity2['related_documents'] else "No documents",
            'rel_count2': entity2['relationship_count'],
            'format_instructions': self.parser.get_format_instructions()
        })
        
        return result
    
    def verify_duplicates_parallel(self, entity_type: str, pairs: List[Tuple[int, int, float]], 
                                  max_workers: int = 5) -> List[Dict]:
        """Verify multiple duplicate pairs in parallel."""
        verified_duplicates = []
        
        def verify_pair(pair_data):
            id1, id2, score = pair_data
            try:
                result = self.verify_duplicate(entity_type, id1, id2)
                if result.are_same:
                    # Get contexts for canonical name selection
                    entity1 = self.get_entity_context(entity_type, id1)
                    entity2 = self.get_entity_context(entity_type, id2)
                    
                    if result.canonical_name:
                        if entity1['name'] == result.canonical_name:
                            keeper_id, duplicate_id = id1, id2
                        else:
                            keeper_id, duplicate_id = id2, id1
                    else:
                        if entity1['relationship_count'] >= entity2['relationship_count']:
                            keeper_id, duplicate_id = id1, id2
                        else:
                            keeper_id, duplicate_id = id2, id1
                    
                    return {
                        'keeper_id': keeper_id,
                        'duplicate_id': duplicate_id,
                        'score': score,
                        'explanation': result.explanation,
                        'is_duplicate': True
                    }
                else:
                    return {
                        'id1': id1,
                        'id2': id2,
                        'score': score,
                        'explanation': result.explanation,
                        'is_duplicate': False
                    }
            except Exception as e:
                return {
                    'id1': id1,
                    'id2': id2,
                    'score': score,
                    'error': str(e),
                    'is_duplicate': False
                }
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(verify_pair, pair) for pair in pairs]
            
            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                print(f"   [{i+1}/{len(pairs)}] ", end='')
                
                if result.get('error'):
                    print(f"ERROR: {result['error']}")
                elif result['is_duplicate']:
                    print(f"DUPLICATE! {result['explanation']}")
                    verified_duplicates.append(result)
                else:
                    print(f"Different. {result['explanation']}")
        
        return verified_duplicates
    
    def merge_entities(self, entity_type: str, keeper_id: int, duplicate_id: int, dry_run: bool = True):
        """Merge duplicate entity into keeper."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get entity names for logging
            table_map = {
                'topic': 'topics',
                'person': 'people',
                'project': 'projects',
                'institution': 'institutions',
                'method': 'methods',
                'application': 'applications'
            }
            table = table_map[entity_type]
            
            cursor.execute(f"SELECT name FROM {table} WHERE id = ?", (keeper_id,))
            keeper_name = cursor.fetchone()['name']
            
            cursor.execute(f"SELECT name FROM {table} WHERE id = ?", (duplicate_id,))
            duplicate_name = cursor.fetchone()['name']
            
            actions = []
            
            # 1. Transfer relationships where duplicate is target
            cursor.execute("""
                SELECT COUNT(*) FROM relationships
                WHERE target_type = ? AND target_id = ?
            """, (entity_type, str(duplicate_id)))
            target_count = cursor.fetchone()[0]
            
            if target_count > 0:
                if not dry_run:
                    # First, check for conflicts
                    cursor.execute("""
                        SELECT source_type, source_id, relationship_type 
                        FROM relationships 
                        WHERE target_type = ? AND target_id = ?
                    """, (entity_type, str(duplicate_id)))
                    
                    duplicate_rels = cursor.fetchall()
                    
                    for rel in duplicate_rels:
                        # Check if keeper already has this relationship
                        cursor.execute("""
                            SELECT 1 FROM relationships 
                            WHERE source_type = ? AND source_id = ? 
                            AND target_type = ? AND target_id = ? 
                            AND relationship_type = ?
                        """, (rel['source_type'], rel['source_id'], entity_type, str(keeper_id), rel['relationship_type']))
                        
                        if cursor.fetchone():
                            # Delete duplicate relationship
                            cursor.execute("""
                                DELETE FROM relationships 
                                WHERE source_type = ? AND source_id = ? 
                                AND target_type = ? AND target_id = ? 
                                AND relationship_type = ?
                            """, (rel['source_type'], rel['source_id'], entity_type, str(duplicate_id), rel['relationship_type']))
                        else:
                            # Update to point to keeper
                            cursor.execute("""
                                UPDATE relationships 
                                SET target_id = ?
                                WHERE source_type = ? AND source_id = ? 
                                AND target_type = ? AND target_id = ? 
                                AND relationship_type = ?
                            """, (str(keeper_id), rel['source_type'], rel['source_id'], entity_type, str(duplicate_id), rel['relationship_type']))
                    
                actions.append(f"Transfer {target_count} relationships as target")
            
            # 2. Transfer relationships where duplicate is source
            cursor.execute("""
                SELECT COUNT(*) FROM relationships
                WHERE source_type = ? AND source_id = ?
            """, (entity_type, str(duplicate_id)))
            source_count = cursor.fetchone()[0]
            
            if source_count > 0:
                if not dry_run:
                    # First, check for conflicts
                    cursor.execute("""
                        SELECT target_type, target_id, relationship_type 
                        FROM relationships 
                        WHERE source_type = ? AND source_id = ?
                    """, (entity_type, str(duplicate_id)))
                    
                    duplicate_rels = cursor.fetchall()
                    
                    for rel in duplicate_rels:
                        # Check if keeper already has this relationship
                        cursor.execute("""
                            SELECT 1 FROM relationships 
                            WHERE source_type = ? AND source_id = ? 
                            AND target_type = ? AND target_id = ? 
                            AND relationship_type = ?
                        """, (entity_type, str(keeper_id), rel['target_type'], rel['target_id'], rel['relationship_type']))
                        
                        if cursor.fetchone():
                            # Delete duplicate relationship
                            cursor.execute("""
                                DELETE FROM relationships 
                                WHERE source_type = ? AND source_id = ? 
                                AND target_type = ? AND target_id = ? 
                                AND relationship_type = ?
                            """, (entity_type, str(duplicate_id), rel['target_type'], rel['target_id'], rel['relationship_type']))
                        else:
                            # Update to point to keeper
                            cursor.execute("""
                                UPDATE relationships 
                                SET source_id = ?
                                WHERE source_type = ? AND source_id = ? 
                                AND target_type = ? AND target_id = ? 
                                AND relationship_type = ?
                            """, (str(keeper_id), entity_type, str(duplicate_id), rel['target_type'], rel['target_id'], rel['relationship_type']))
                    
                actions.append(f"Transfer {source_count} relationships as source")
            
            # 3. Merge attributes (keep best of both)
            cursor.execute(f"SELECT * FROM {table} WHERE id IN (?, ?)", (keeper_id, duplicate_id))
            entities = cursor.fetchall()
            # Convert Row objects to dicts first
            entity_dicts = [dict(e) for e in entities]
            keeper_data = entity_dicts[0] if entity_dicts[0]['id'] == keeper_id else entity_dicts[1]
            duplicate_data = entity_dicts[1] if entity_dicts[0]['id'] == keeper_id else entity_dicts[0]
            
            updates = {}
            for col in ['description', 'category', 'role', 'affiliation', 'domain', 'type', 'location']:
                if col in keeper_data:
                    if not keeper_data.get(col) and duplicate_data.get(col):
                        updates[col] = duplicate_data[col]
            
            if updates and not dry_run:
                set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [keeper_id]
                cursor.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", values)
                actions.append(f"Merged attributes: {list(updates.keys())}")
            elif updates:
                actions.append(f"Would merge attributes: {list(updates.keys())}")
            
            # 4. Delete duplicate
            if not dry_run:
                cursor.execute(f"DELETE FROM {table} WHERE id = ?", (duplicate_id,))
            actions.append("Delete duplicate entity")
            
            # 5. Delete duplicate embeddings
            if not dry_run:
                cursor.execute("""
                    DELETE FROM embeddings
                    WHERE entity_type = ? AND entity_id = ?
                """, (entity_type, f"{entity_type}_{duplicate_id}"))
            actions.append("Delete duplicate embeddings")
            
            # Commit or rollback
            if not dry_run:
                conn.commit()
                self.audit_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'merge',
                    'entity_type': entity_type,
                    'keeper': {'id': keeper_id, 'name': keeper_name},
                    'duplicate': {'id': duplicate_id, 'name': duplicate_name},
                    'actions': actions
                })
            else:
                conn.rollback()
            
            return {
                'keeper': {'id': keeper_id, 'name': keeper_name},
                'duplicate': {'id': duplicate_id, 'name': duplicate_name},
                'actions': actions
            }
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def merge_cluster(self, entity_type: str, cluster_ids: List[int], dry_run: bool = True) -> Dict:
        """Merge a cluster of duplicate entities into one canonical entity."""
        if len(cluster_ids) < 2:
            return {'error': 'Cluster must have at least 2 entities'}
        
        # Choose canonical entity
        keeper_id, keeper_name = self.choose_canonical_entity(entity_type, cluster_ids)
        duplicate_ids = [id for id in cluster_ids if id != keeper_id]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get names for logging
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        table = table_map[entity_type]
        
        duplicate_names = []
        for dup_id in duplicate_ids:
            cursor.execute(f"SELECT name FROM {table} WHERE id = ?", (dup_id,))
            duplicate_names.append(cursor.fetchone()['name'])
        
        conn.close()
        
        # Merge each duplicate into keeper
        actions = []
        for dup_id in duplicate_ids:
            result = self.merge_entities(entity_type, keeper_id, dup_id, dry_run=dry_run)
            actions.extend(result['actions'])
        
        return {
            'keeper': {'id': keeper_id, 'name': keeper_name},
            'duplicates': [{'id': did, 'name': dname} for did, dname in zip(duplicate_ids, duplicate_names)],
            'cluster_size': len(cluster_ids),
            'actions': actions
        }
    
    def deduplicate_entity_type(self, entity_type: str, dry_run: bool = True, 
                                use_embeddings: bool = True, batch_size: int = 10,
                                use_clustering: bool = True, parallel_workers: int = 5):
        """Deduplicate all entities of a given type."""
        print(f"\n{'='*60}")
        print(f"DEDUPLICATING {entity_type.upper()} ENTITIES")
        print(f"{'='*60}")
        
        # Get total entity count
        conn = self.get_connection()
        cursor = conn.cursor()
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        table = table_map[entity_type]
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_entities = cursor.fetchone()[0]
        conn.close()
        
        print(f"\nTotal {entity_type}s in database: {total_entities}")
        
        # Find candidates
        print("\n1. Finding duplicate candidates...")
        
        # String-based candidates
        string_candidates = self.find_string_duplicates(entity_type)
        print(f"   String-based candidates: {len(string_candidates)}")
        if string_candidates:
            string_scores = [s[2] for s in string_candidates]
            print(f"     - Exact matches (score=1.0): {sum(1 for s in string_scores if s == 1.0)}")
            print(f"     - Fuzzy matches: {sum(1 for s in string_scores if s < 1.0)}")
            if any(s < 1.0 for s in string_scores):
                print(f"     - Score range: {min(s for s in string_scores if s < 1.0):.3f} - {max(s for s in string_scores if s < 1.0):.3f}")
        
        # Embedding-based candidates
        embedding_candidates = []
        if use_embeddings:
            try:
                embedding_candidates = self.find_embedding_duplicates(entity_type)
                print(f"   Embedding-based candidates: {len(embedding_candidates)}")
                if embedding_candidates:
                    emb_scores = [s[2] for s in embedding_candidates]
                    print(f"     - Score range: {min(emb_scores):.3f} - {max(emb_scores):.3f}")
                    print(f"     - Lowest score above threshold: {min(emb_scores):.3f}")
            except Exception as e:
                print(f"   Warning: Could not use embeddings: {e}")
        
        # Combine and deduplicate candidate pairs
        all_candidates = {}
        string_only = set()
        embedding_only = set()
        both_methods = set()
        
        for id1, id2, score in string_candidates:
            key = (min(id1, id2), max(id1, id2))
            all_candidates[key] = max(score, all_candidates.get(key, 0))
            string_only.add(key)
        
        for id1, id2, score in embedding_candidates:
            key = (min(id1, id2), max(id1, id2))
            if key in string_only:
                both_methods.add(key)
                string_only.remove(key)
            else:
                embedding_only.add(key)
            all_candidates[key] = max(score, all_candidates.get(key, 0))
        
        # Sort by score
        sorted_candidates = sorted(
            [(k[0], k[1], v) for k, v in all_candidates.items()],
            key=lambda x: x[2],
            reverse=True
        )
        
        print(f"\n   Detection method breakdown:")
        print(f"     - Found by string matching only: {len(string_only)}")
        print(f"     - Found by embeddings only: {len(embedding_only)}")
        print(f"     - Found by both methods: {len(both_methods)}")
        print(f"   Total unique pairs: {len(sorted_candidates)}")
        
        if not sorted_candidates:
            print("\nNo duplicate candidates found!")
            return []
        
        verified_clusters = []  # Initialize at top level
        
        if use_clustering:
            # Find transitive clusters
            print("\n2. Finding duplicate clusters...")
            clusters = self.find_duplicate_clusters(sorted_candidates)
            print(f"   Found {len(clusters)} clusters")
            
            # Show cluster sizes
            if clusters:
                cluster_sizes = [len(c['ids']) for c in clusters]
                print(f"   Cluster sizes: {', '.join(map(str, sorted(cluster_sizes, reverse=True)))}")
                print(f"   Largest cluster: {max(cluster_sizes)} entities")
            
            # Verify clusters with parallel processing
            print(f"\n3. Verifying clusters with LLM (parallel workers: {parallel_workers})...")
            
            total_pairs = sum(len(c['pairs']) for c in clusters)
            print(f"   Total pairs to verify: {total_pairs}")
            
            start_time = time.time()
            
            for cluster_idx, cluster in enumerate(clusters):
                print(f"\n   Cluster {cluster_idx + 1}/{len(clusters)} ({len(cluster['ids'])} entities):")
                
                # Show entities in cluster
                conn = self.get_connection()
                cursor = conn.cursor()
                table = {'topic': 'topics', 'person': 'people', 'project': 'projects',
                        'institution': 'institutions', 'method': 'methods', 
                        'application': 'applications'}[entity_type]
                
                names = []
                for eid in cluster['ids']:
                    cursor.execute(f"SELECT name FROM {table} WHERE id = ?", (eid,))
                    names.append(cursor.fetchone()['name'])
                conn.close()
                
                print(f"     Entities: {', '.join(names[:5])}")
                if len(names) > 5:
                    print(f"     ... and {len(names) - 5} more")
                
                # Verify pairs in parallel
                verified_pairs = self.verify_duplicates_parallel(
                    entity_type, cluster['pairs'], max_workers=parallel_workers
                )
                
                # Check if cluster is valid (all pairs verified as duplicates)
                if len(verified_pairs) == len(cluster['pairs']):
                    verified_clusters.append({
                        'cluster_ids': cluster['ids'],
                        'verified_pairs': verified_pairs
                    })
                    print(f"     ✓ All {len(verified_pairs)} pairs verified as duplicates")
                else:
                    print(f"     ⚠ Only {len(verified_pairs)}/{len(cluster['pairs'])} pairs verified")
                    # Handle partial clusters - break them up
                    # This is a more complex case we can implement later
            
            elapsed = time.time() - start_time
            print(f"\n   Verification completed in {elapsed:.1f} seconds")
            
            # Convert to flat list for compatibility
            verified_duplicates = []
            for cluster in verified_clusters:
                verified_duplicates.extend(cluster['verified_pairs'])
        
        else:
            # Original sequential verification
            print(f"\n2. Verifying duplicates with LLM (batch size: {batch_size})...")
            
            verified_duplicates = []
            processed = 0
            
            for i in range(0, len(sorted_candidates), batch_size):
                batch = sorted_candidates[i:i+batch_size]
                print(f"\n   Batch {i//batch_size + 1}/{(len(sorted_candidates) + batch_size - 1)//batch_size}")
                
                for id1, id2, score in batch:
                    processed += 1
                    print(f"   [{processed}/{len(sorted_candidates)}] Checking pair (score: {score:.3f})...", end='')
                    
                    try:
                        result = self.verify_duplicate(entity_type, id1, id2)
                        
                        if result.are_same:
                            # Determine keeper (prefer one with more relationships or canonical name)
                            entity1 = self.get_entity_context(entity_type, id1)
                            entity2 = self.get_entity_context(entity_type, id2)
                            
                            if result.canonical_name:
                                # Use LLM's suggestion
                                if entity1['name'] == result.canonical_name:
                                    keeper_id, duplicate_id = id1, id2
                                else:
                                    keeper_id, duplicate_id = id2, id1
                            else:
                                # Use relationship count
                                if entity1['relationship_count'] >= entity2['relationship_count']:
                                    keeper_id, duplicate_id = id1, id2
                                else:
                                    keeper_id, duplicate_id = id2, id1
                            
                            verified_duplicates.append({
                                'keeper_id': keeper_id,
                                'duplicate_id': duplicate_id,
                                'score': score,
                                'explanation': result.explanation
                            })
                            print(f" DUPLICATE! {result.explanation}")
                        else:
                            print(f" Different. {result.explanation}")
                            
                    except Exception as e:
                        print(f" ERROR: {e}")
        
        print(f"\n3. Found {len(verified_duplicates)} verified duplicates")
        
        # Calculate statistics
        if sorted_candidates:
            detection_rate = len(verified_duplicates) / len(sorted_candidates) * 100
            print(f"   Detection rate: {detection_rate:.1f}% of candidates were true duplicates")
        
        if verified_duplicates:
            scores = [d['score'] for d in verified_duplicates]
            print(f"   Score range of verified duplicates: {min(scores):.3f} - {max(scores):.3f}")
        
        # Merge duplicates
        if verified_duplicates and use_clustering and verified_clusters:
            print(f"\n4. {'Merging' if not dry_run else 'Planning merges for'} {len(verified_clusters)} clusters...")
            
            merge_results = []
            total_merged = 0
            
            for cluster_idx, cluster in enumerate(verified_clusters):
                cluster_result = self.merge_cluster(
                    entity_type,
                    cluster['cluster_ids'],
                    dry_run=dry_run
                )
                merge_results.append(cluster_result)
                
                print(f"\n   Cluster {cluster_idx + 1}: {'[DRY RUN] Would merge' if dry_run else 'Merged'} {cluster_result['cluster_size']} entities:")
                print(f"     Keep: {cluster_result['keeper']['name']} (id:{cluster_result['keeper']['id']})")
                print(f"     Remove: {', '.join([d['name'] for d in cluster_result['duplicates'][:3]])}")
                if len(cluster_result['duplicates']) > 3:
                    print(f"            ... and {len(cluster_result['duplicates']) - 3} more")
                
                total_merged += len(cluster_result['duplicates'])
            
            # Update verified_duplicates count for statistics
            verified_duplicates = [{'merged': True}] * total_merged
            
        elif verified_duplicates:
            print(f"\n4. {'Merging' if not dry_run else 'Planning merges for'} {len(verified_duplicates)} duplicates...")
            
            merge_results = []
            for dup in verified_duplicates:
                result = self.merge_entities(
                    entity_type,
                    dup['keeper_id'],
                    dup['duplicate_id'],
                    dry_run=dry_run
                )
                merge_results.append(result)
                
                print(f"\n   {'[DRY RUN] Would merge' if dry_run else 'Merged'}:")
                print(f"     Keep: {result['keeper']['name']} (id:{result['keeper']['id']})")
                print(f"     Remove: {result['duplicate']['name']} (id:{result['duplicate']['id']})")
                print(f"     Actions: {', '.join(result['actions'])}")
        
        # Final statistics
        print(f"\n5. Summary for {entity_type}s:")
        print(f"   Original count: {total_entities}")
        print(f"   Duplicates found: {len(verified_duplicates)}")
        print(f"   Final count after dedup: {total_entities - len(verified_duplicates)}")
        print(f"   Reduction: {len(verified_duplicates) / total_entities * 100:.1f}%")
        
        return verified_duplicates
    
    def deduplicate_all(self, dry_run: bool = True, use_clustering: bool = True, 
                       parallel_workers: int = 5):
        """Deduplicate all entity types."""
        entity_types = ['topic', 'person', 'project', 'institution', 'method', 'application']
        
        all_results = {}
        entity_stats = {}
        
        # Get initial counts
        conn = self.get_connection()
        cursor = conn.cursor()
        table_map = {
            'topic': 'topics',
            'person': 'people',
            'project': 'projects',
            'institution': 'institutions',
            'method': 'methods',
            'application': 'applications'
        }
        
        for entity_type in entity_types:
            table = table_map[entity_type]
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            entity_stats[entity_type] = {
                'original': cursor.fetchone()[0],
                'duplicates': 0
            }
        conn.close()
        
        for entity_type in entity_types:
            results = self.deduplicate_entity_type(
                entity_type, 
                dry_run=dry_run,
                use_clustering=use_clustering,
                parallel_workers=parallel_workers
            )
            all_results[entity_type] = results
            entity_stats[entity_type]['duplicates'] = len(results)
        
        # Summary
        print("\n" + "="*60)
        print("DEDUPLICATION SUMMARY")
        print("="*60)
        
        print("\n" + " "*15 + "Original  Duplicates  Final  Reduction")
        print("-"*60)
        
        total_original = 0
        total_duplicates = 0
        
        for entity_type in entity_types:
            stats = entity_stats[entity_type]
            original = stats['original']
            duplicates = stats['duplicates']
            final = original - duplicates
            reduction = (duplicates / original * 100) if original > 0 else 0
            
            total_original += original
            total_duplicates += duplicates
            
            print(f"{entity_type.capitalize():12s}  {original:8d}  {duplicates:10d}  {final:5d}  {reduction:6.1f}%")
        
        print("-"*60)
        total_final = total_original - total_duplicates
        total_reduction = (total_duplicates / total_original * 100) if total_original > 0 else 0
        print(f"{'TOTAL':12s}  {total_original:8d}  {total_duplicates:10d}  {total_final:5d}  {total_reduction:6.1f}%")
        
        if dry_run:
            print("\nThis was a DRY RUN. No changes were made.")
            print("Run with --merge to actually merge duplicates.")
        
        # Save audit log
        if not dry_run and self.audit_log:
            # Ensure logs directory exists
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            log_file = logs_dir / f"deduplication_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(self.audit_log, f, indent=2)
            print(f"\nAudit log saved to: {log_file}")
        
        return all_results


def main():
    """Main entry point."""
    import argparse
    import shutil
    
    parser = argparse.ArgumentParser(description='Deduplicate entities in the knowledge graph')
    parser.add_argument('--db', default="DB/metadata.db", 
                       help='Database path')
    parser.add_argument('--threshold', type=float, default=0.85,
                       help='Embedding similarity threshold (0-1)')
    parser.add_argument('--entity-type', choices=['topic', 'person', 'project', 'institution', 'method', 'application'],
                       help='Deduplicate only this entity type')
    parser.add_argument('--merge', action='store_true',
                       help='Actually merge duplicates (default is dry run)')
    parser.add_argument('--no-embeddings', action='store_true',
                       help='Skip embedding-based duplicate detection')
    parser.add_argument('--batch-size', type=int, default=10,
                       help='LLM verification batch size')
    parser.add_argument('--backup', action='store_true',
                       help='Create database backup before merging')
    parser.add_argument('--no-clustering', action='store_true',
                       help='Disable transitive clustering')
    parser.add_argument('--parallel-workers', type=int, default=5,
                       help='Number of parallel workers for LLM verification')
    
    args = parser.parse_args()
    
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return 1
    
    # Create backup if requested
    if args.backup and args.merge:
        backup_path = db_path.with_suffix('.backup.db')
        print(f"Creating backup at: {backup_path}")
        shutil.copy2(db_path, backup_path)
    
    try:
        deduplicator = EntityDeduplicator(str(db_path), args.threshold)
        
        if args.entity_type:
            # Deduplicate single entity type
            deduplicator.deduplicate_entity_type(
                args.entity_type,
                dry_run=not args.merge,
                use_embeddings=not args.no_embeddings,
                batch_size=args.batch_size,
                use_clustering=not args.no_clustering,
                parallel_workers=args.parallel_workers
            )
        else:
            # Deduplicate all
            deduplicator.deduplicate_all(
                dry_run=not args.merge,
                use_clustering=not args.no_clustering,
                parallel_workers=args.parallel_workers
            )
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 1
    except Exception as e:
        import traceback
        print(f"\nError: {e}")
        print("\nFull traceback:")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())