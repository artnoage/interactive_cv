#!/usr/bin/env python3
"""Comprehensive query of the metadata database."""

import sqlite3
import json
from pathlib import Path

db_path = "metadata_system/metadata.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("="*80)
print("INTERACTIVE CV DATABASE SUMMARY")
print("="*80)

# Document counts by type
cursor.execute("""
    SELECT doc_type, COUNT(*) as count 
    FROM documents 
    GROUP BY doc_type
""")
print("\n📚 DOCUMENTS BY TYPE:")
for row in cursor.fetchall():
    print(f"  - {row['doc_type'].capitalize()}: {row['count']} documents")

# Total unique entities
cursor.execute("SELECT COUNT(*) FROM topics")
topic_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM people")
people_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM projects")
project_count = cursor.fetchone()[0]

print(f"\n🏷️  UNIQUE ENTITIES:")
print(f"  - Topics: {topic_count}")
print(f"  - People: {people_count}")
print(f"  - Projects: {project_count}")

# Academic papers
print("\n🎓 ACADEMIC PAPERS:")
cursor.execute("""
    SELECT title, json_extract(metadata, '$.year') as year
    FROM documents 
    WHERE doc_type = 'academic'
    ORDER BY title
""")
for i, row in enumerate(cursor.fetchall(), 1):
    year = row['year'] if row['year'] != 'not specified' else 'year unknown'
    print(f"  {i}. {row['title']} ({year})")

# Top research areas
print("\n🔬 TOP RESEARCH AREAS (from academic papers):")
cursor.execute("""
    SELECT t.name, COUNT(dt.document_id) as count
    FROM topics t
    JOIN document_topics dt ON t.id = dt.topic_id
    JOIN documents d ON dt.document_id = d.id
    WHERE d.doc_type = 'academic'
    GROUP BY t.id
    ORDER BY count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"  - {row['name']}: {row['count']} papers")

# Chronicle projects
print("\n💼 CHRONICLE PROJECTS:")
cursor.execute("""
    SELECT p.name, COUNT(dp.document_id) as count
    FROM projects p
    JOIN document_projects dp ON p.id = dp.project_id
    GROUP BY p.id
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"  - {row['name']}: {row['count']} mentions")

# Recent chronicle activity
print("\n📅 RECENT CHRONICLE ACTIVITY:")
cursor.execute("""
    SELECT date, title, 
           json_extract(metadata, '$.work_focus') as work_focus
    FROM documents 
    WHERE doc_type = 'chronicle'
    ORDER BY date DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    focus = row['work_focus'] if row['work_focus'] else 'General work'
    print(f"  - {row['date']}: {focus}")

# Sample cross-references
print("\n🔗 SAMPLE CONNECTIONS:")
print("  Topics appearing in both academic and chronicle:")
cursor.execute("""
    SELECT t.name
    FROM topics t
    WHERE EXISTS (
        SELECT 1 FROM document_topics dt
        JOIN documents d ON dt.document_id = d.id
        WHERE dt.topic_id = t.id AND d.doc_type = 'academic'
    )
    AND EXISTS (
        SELECT 1 FROM document_topics dt
        JOIN documents d ON dt.document_id = d.id
        WHERE dt.topic_id = t.id AND d.doc_type = 'chronicle'
    )
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"    - {row[0]}")

conn.close()

print("\n" + "="*80)
print("✅ Database ready for RAG queries!")
print("="*80)