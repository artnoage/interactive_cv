#!/bin/bash

# Git-based chronicle sync
# First time: git init, add remote
# Regular use: auto-commit and push

CHRONICLE_DIR="/home/artnoage/Projects/interactive_cv/chronicle"
cd "$CHRONICLE_DIR"

# Initialize git if needed
if [ ! -d .git ]; then
    git init
    echo "*.obsidian/" > .gitignore
    git add .
    git commit -m "Initial chronicle"
    echo "Add your remote with: git remote add origin <your-repo-url>"
    exit 0
fi

# Regular sync
git add .
git commit -m "Chronicle update: $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo "Chronicle pushed to git!"