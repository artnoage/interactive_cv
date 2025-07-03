import sqlite3
import json

conn = sqlite3.connect("metadata_system/metadata.db")
cursor = conn.cursor()

print("=== Checking metadata columns for relationships ===\n")

# Check chronicle documents
print("Chronicle Document Metadata Sample:")
cursor.execute("SELECT id, title, metadata FROM chronicle_documents WHERE metadata IS NOT NULL LIMIT 2")
for row in cursor.fetchall():
    doc_id, title, metadata_json = row
    if metadata_json:
        metadata = json.loads(metadata_json)
        print(f"\nDocument {doc_id}: {title}")
        print(f"Metadata keys: {list(metadata.keys())}")
        # Look for relationship-like fields
        for key in ['papers', 'tools', 'insights', 'references', 'collaborators', 'related_to']:
            if key in metadata and metadata[key]:
                print(f"  {key}: {metadata[key][:2] if isinstance(metadata[key], list) else metadata[key]}")

# Check academic documents
print("\n\nAcademic Document Metadata Sample:")
cursor.execute("SELECT id, title, metadata FROM academic_documents WHERE metadata IS NOT NULL LIMIT 2")
for row in cursor.fetchall():
    doc_id, title, metadata_json = row
    if metadata_json:
        metadata = json.loads(metadata_json)
        print(f"\nDocument {doc_id}: {title[:50]}...")
        print(f"Metadata keys: {list(metadata.keys())}")
        # Look for relationship-like fields
        for key in ['collaborators', 'references', 'builds_on', 'applications', 'related_work']:
            if key in metadata and metadata[key]:
                print(f"  {key}: {metadata[key][:2] if isinstance(metadata[key], list) else metadata[key]}")

# Check semantic relationships table
print("\n\nSemantic Relationships Sample:")
cursor.execute("""
    SELECT source_type, source_id, target_type, target_id, relationship_type, description 
    FROM semantic_relationships 
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"  {row[0]} '{row[1]}' --[{row[4]}]--> {row[2]} '{row[3]}'")
    if row[5]:
        print(f"    Description: {row[5]}")

conn.close()