#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Interactive CV - Unified Server${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if metadata.db exists
if [ ! -f "DB/metadata.db" ]; then
    echo -e "${RED}Database not found. Please run: python DB/build_database.py${NC}"
    exit 1
fi

# Check if knowledge graph exists (prefer pruned version in web_ui)
if [ ! -f "web_ui/knowledge_graph.json" ] && [ ! -f "KG/knowledge_graph.json" ]; then
    echo -e "${YELLOW}Knowledge graph not found. Generating...${NC}"
    python KG/graph_builder.py DB/metadata.db --output KG/knowledge_graph.json
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to generate knowledge graph${NC}"
        exit 1
    fi
    echo -e "${YELLOW}Note: Consider creating a pruned version in web_ui/knowledge_graph.json for better performance${NC}"
elif [ -f "web_ui/knowledge_graph.json" ]; then
    echo -e "${GREEN}Using pruned knowledge graph from web_ui/${NC}"
else
    echo -e "${GREEN}Using knowledge graph from KG/${NC}"
fi

# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Optional: Start datasette in background
if [[ "$1" == "--with-datasette" ]]; then
    echo -e "${GREEN}Starting Datasette on http://localhost:8001${NC}"
    datasette serve DB/metadata.db -p 8001 &
    DATASETTE_PID=$!
    echo -e "${GREEN}Datasette PID: $DATASETTE_PID${NC}"
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down...${NC}"
    if [[ -n "$DATASETTE_PID" ]]; then
        echo -e "${YELLOW}Stopping Datasette (PID: $DATASETTE_PID)${NC}"
        kill $DATASETTE_PID 2>/dev/null
    fi
    exit 0
}

trap cleanup INT TERM

# Start the main server
echo -e "${GREEN}Starting Interactive CV server on http://localhost:8888${NC}"
echo -e "${GREEN}The UI includes:${NC}"
echo -e "${GREEN}  - Knowledge Graph Visualization${NC}"
echo -e "${GREEN}  - Interactive Chat with AI Assistant${NC}"
echo -e "${GREEN}  - Graph Filtering and Search${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

python serve_ui.py

# Cleanup will be called automatically on exit