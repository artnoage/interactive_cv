#!/bin/bash
# Launch Datasette to view the metadata database

echo "Installing Datasette if not already installed..."
pip install datasette datasette-cluster-map datasette-vega

echo ""
echo "Launching Datasette..."
echo "Database will be available at: http://localhost:8001"
echo "Press Ctrl+C to stop"
echo ""

# Launch datasette on port 8001 (to avoid conflicts)
datasette DB/metadata.db -p 8001 --open