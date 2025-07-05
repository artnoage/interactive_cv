# Post-Mortem: Interactive CV Agent Tool Development

## What Went Wrong Initially

### 1. **Misunderstanding the Task Requirements**
**Problem**: I initially started creating scripts that directly queried the database and read raw metadata files, instead of creating tools that an agent would use.

**Root Cause**: I didn't fully grasp that we were building tools FOR an agent to use, not answering the questions ourselves.

**Example of Wrong Approach**:
```python
# I was doing this - directly reading files:
with open("raw_data/academic/extracted_metadata/UNOT_metadata.json") as f:
    data = json.load(f)
```

**What We Should Have Done**:
```python
# Creating tools that query the database:
def search_academic_papers(query: str) -> List[Dict]:
    # Query the database, not raw files
```

### 2. **Database Schema Confusion**

**Problem**: Multiple issues with understanding the actual database structure:
- Assumed columns that didn't exist (`analysis_path`, `core_contribution`)
- Didn't understand the document ID format (`academic_1` vs just `1`)
- Confused about table names (`documents` vs `academic_documents`/`chronicle_documents`)

**Root Cause**: We didn't properly examine the database schema before writing queries. We made assumptions based on the conceptual model rather than the actual implementation.

**Key Learning**: The database uses a specific ID format for relationships:
- Documents: `academic_1`, `chronicle_2` (type_id format)
- This is crucial for joining relationships correctly

### 3. **Tool Interface Mismatch**

**Problem**: The existing interactive agent expected specific tool signatures that we weren't matching.

**Root Cause**: Didn't examine the existing agent's tool expectations before creating new ones.

## How We Fixed It

### 1. **Pivoted to Tool Creation**
- Stopped trying to answer questions directly
- Created reusable tools that query the database
- Followed the pattern of: input query → database search → structured output

### 2. **Examined Actual Database Structure**
Used SQLite commands to understand the real schema:
```bash
sqlite3 DB/metadata.db ".tables"
sqlite3 DB/metadata.db ".schema table_name"
sqlite3 DB/metadata.db "SELECT DISTINCT relationship_type FROM relationships"
```

### 3. **Used Configuration Files as Reference**
The blueprints in `blueprints/academic/` helped understand the data model without looking at raw data:
- `extraction_schema.yaml` - what fields exist
- `database_mapping.yaml` - how they map to database tables

### 4. **Created Clean, Focused Tools**
Built `tools/agent_tools.py` with clear, single-purpose functions that match what an agent needs:
- `search_academic_papers()`
- `get_paper_authors()`
- `search_chronicle_notes()`
- `find_research_topics()`
- etc.

## Key Insights

1. **Configuration-Driven Architecture**: The system's strength is its configuration-driven design. Understanding the YAML blueprints is more important than looking at raw data.

2. **Document ID Format**: The `type_id` format (e.g., `academic_1`) is crucial for relationships. This wasn't immediately obvious.

3. **Tool Design Philosophy**: Tools should be simple, focused, and return structured data. The agent handles natural language generation.

4. **Database First**: Always check the actual database schema rather than making assumptions based on conceptual understanding.

## Lessons for Future Development

1. **Start with Schema**: Always examine database schema first
2. **Read Existing Code**: Check how existing tools work before creating new ones
3. **Test Incrementally**: Test each query/tool individually before combining
4. **Use Configuration**: Leverage the blueprint system rather than hardcoding assumptions
5. **Think in Tools**: Design tools for agents to use, not scripts that solve problems directly

The final solution (`tools/agent_tools.py`) provides a clean, comprehensive toolset that properly interfaces with the database and can answer all test questions effectively.