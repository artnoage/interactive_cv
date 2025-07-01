#!/bin/bash

# Chronicle sync script - sync to both local and remote
SOURCE="/home/artnoage/OneDrive/Second_Mind/Second Mind/Notes/"
LOCAL_DEST="/home/artnoage/Projects/interactive_cv/chronicle/"
REMOTE_HOST="Google"  # Your Google Cloud host alias from SSH config
REMOTE_DEST="~/chronicle/"  # Chronicle folder in your home directory on remote

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Chronicle Multi-Sync${NC}"

# Local sync
echo "1. Syncing locally..."
rsync -av --delete \
    --exclude='.obsidian/' \
    --exclude='.trash/' \
    --exclude='.DS_Store' \
    "$SOURCE" "$LOCAL_DEST"

# Remote sync (over Tailscale)
echo ""
echo "2. Syncing to Google Cloud..."
rsync -av --delete \
    --exclude='.obsidian/' \
    --exclude='.trash/' \
    --exclude='.DS_Store' \
    "$SOURCE" "$REMOTE_HOST:$REMOTE_DEST"

echo ""
echo -e "${GREEN}All syncs complete!${NC}"