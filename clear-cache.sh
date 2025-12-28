#!/bin/bash
# Clear the Claude Code plugin cache for nethercore-ai-plugins
# Run this after making changes to plugin files

CACHE_DIR="$HOME/.claude/plugins/cache/nethercore-ai-plugins"

if [ -d "$CACHE_DIR" ]; then
    rm -rf "$CACHE_DIR"
    echo "Cleared: $CACHE_DIR"
    echo "Restart Claude Code to reload plugins"
else
    echo "Cache directory not found: $CACHE_DIR"
fi
