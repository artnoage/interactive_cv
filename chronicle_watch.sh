#!/bin/bash

# Real-time chronicle sync using inotify
# This watches for changes and syncs immediately

SOURCE="/home/artnoage/OneDrive/Second_Mind/Second Mind/Notes"
DEST="/home/artnoage/Projects/interactive_cv/chronicle"
SYNC_SCRIPT="/home/artnoage/Projects/interactive_cv/sync_chronicle.sh"

# Check if inotify-tools is installed
if ! command -v inotifywait &> /dev/null; then
    echo "inotify-tools is not installed."
    echo "Please install it with: sudo apt install inotify-tools"
    exit 1
fi

echo "Starting Chronicle real-time sync..."
echo "Watching: $SOURCE"
echo "Press Ctrl+C to stop"
echo ""

# Initial sync
bash "$SYNC_SCRIPT"

# Watch for changes and sync
while true; do
    inotifywait -r -e modify,create,delete,move "$SOURCE" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Change detected, syncing..."
        bash "$SYNC_SCRIPT"
    fi
done