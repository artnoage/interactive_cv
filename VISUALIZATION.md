# Visualization Tools for Interactive CV

## 1. Database Visualization with Datasette

### Quick Start
```bash
./view_database.sh
```

This will:
- Install Datasette (if needed)
- Launch a web interface at http://localhost:8001
- Allow you to:
  - Browse all tables interactively
  - Run SQL queries
  - Export data in various formats
  - Create custom views

### Features
- Automatic API generation for all queries
- Faceted search
- JSON/CSV export
- Plugin ecosystem for extensions

## 2. Knowledge Graph Visualization

### Generate/Update Graph
```bash
python3 metadata_system/knowledge_graph.py
```

This creates:
- `metadata_system/knowledge_graph.json` - Raw graph data
- `metadata_system/knowledge_graph.html` - Interactive visualization

### View the Graph
Open `metadata_system/knowledge_graph.html` in your browser

### Graph Statistics (Current)
- **218 nodes** total:
  - 20 documents (papers + chronicles)
  - 170 topics
  - 18 projects  
  - 3 people
- **286 edges** (connections)
- **2 connected components**

### Features
- Interactive network visualization using vis.js
- Color-coded nodes by type:
  - 🔴 Documents (red)
  - 🔵 Topics (blue)
  - 🟢 People (green)
  - 🟠 Projects (orange)
- Draggable nodes
- Zoom and pan
- Hover for details

## 3. Alternative Desktop Tools

### DB Browser for SQLite
```bash
sudo apt install sqlitebrowser
sqlitebrowser metadata_system/metadata.db
```

### DBeaver (Professional)
Download from: https://dbeaver.io/

## Integration with Future UI

The knowledge graph data (`knowledge_graph.json`) is ready to be integrated into any web framework:
- D3.js for custom visualizations
- React/Vue components
- Three.js for 3D graphs
- Neo4j for advanced graph queries

## Usage in Research

The graph reveals:
- Research topic clusters
- Collaboration patterns
- Project evolution over time
- Connection between academic work and daily practice