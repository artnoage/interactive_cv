#!/bin/bash

# Chronicle sync script - one-way sync from Obsidian to project
# This script can be run manually or automated with cron/systemd

SOURCE="/home/artnoage/OneDrive/Second_Mind/Second Mind/Notes/"
DEST="/home/artnoage/Projects/interactive_cv/chronicle/"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Chronicle Sync${NC}"
echo "Syncing from: $SOURCE"
echo "         to: $DEST"
echo ""

# Create destination if it doesn't exist
mkdir -p "$DEST"

# Perform the sync
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose
# --delete: delete files in dest that don't exist in source
# --exclude: exclude Obsidian metadata
rsync -av --delete \
    --exclude='.obsidian/' \
    --exclude='.trash/' \
    --exclude='.DS_Store' \
    "$SOURCE" "$DEST"

echo ""
echo -e "${GREEN}Sync complete!${NC}"

# Show summary
echo ""
echo "Summary:"
find "$DEST" -type f -name "*.md" | wc -l | xargs echo "  Total markdown files:"
echo "  Recent notes:"
find "$DEST" -type f -name "*.md" -printf "    %f\n" | sort | tail -5