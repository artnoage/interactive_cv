#!/bin/bash

# Syncthing configuration script for chronicle sync
# This sets up a one-way sync from Obsidian Notes to chronicle folder

SYNCTHING_API="http://127.0.0.1:8384"
CONFIG_DIR="$HOME/.local/state/syncthing"

# Wait for Syncthing to be ready
echo "Waiting for Syncthing to be ready..."
while ! curl -s "$SYNCTHING_API/rest/system/ping" > /dev/null; do
    sleep 1
done

# Get API key
API_KEY=$(grep -oP '<apikey>\K[^<]+' "$CONFIG_DIR/config.xml")

echo "Found API key: ${API_KEY:0:8}..."

# Remove default folder
echo "Removing default folder..."
curl -X DELETE -H "X-API-Key: $API_KEY" "$SYNCTHING_API/rest/config/folders/default"

# Add Obsidian Notes folder (Send Only)
echo "Adding Obsidian Notes folder..."
curl -X PUT -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
    "$SYNCTHING_API/rest/config/folders/obsidian-notes" \
    -d '{
        "id": "obsidian-notes",
        "label": "Obsidian Notes",
        "path": "/home/artnoage/OneDrive/Second_Mind/Second Mind/Notes",
        "type": "sendonly",
        "devices": [{"deviceID": "'"$(curl -s -H "X-API-Key: $API_KEY" "$SYNCTHING_API/rest/system/status" | grep -oP '"myID":"\K[^"]+' )"'"}],
        "rescanIntervalS": 60,
        "ignorePerms": false,
        "autoNormalize": true
    }'

# Add Chronicle folder (Receive Only)
echo "Adding Chronicle folder..."
curl -X PUT -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
    "$SYNCTHING_API/rest/config/folders/chronicle" \
    -d '{
        "id": "chronicle",
        "label": "Chronicle",
        "path": "/home/artnoage/Projects/interactive_cv/chronicle",
        "type": "receiveonly",
        "devices": [{"deviceID": "'"$(curl -s -H "X-API-Key: $API_KEY" "$SYNCTHING_API/rest/system/status" | grep -oP '"myID":"\K[^"]+' )"'"}],
        "rescanIntervalS": 60,
        "ignorePerms": false,
        "autoNormalize": true
    }'

# Restart Syncthing to apply changes
echo "Restarting Syncthing..."
curl -X POST -H "X-API-Key: $API_KEY" "$SYNCTHING_API/rest/system/restart"

echo "Configuration complete!"
echo ""
echo "However, Syncthing doesn't support direct local-to-local folder sync."
echo "You'll need to use one of these alternatives:"
echo ""
echo "1. Use rsync with inotify for real-time sync (recommended)"
echo "2. Set up a scheduled rsync job"
echo "3. Use Syncthing with two instances (more complex)"
echo ""
echo "Would you like me to set up an rsync-based solution instead?"