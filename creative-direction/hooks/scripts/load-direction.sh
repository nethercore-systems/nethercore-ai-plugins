#!/bin/bash
# Load creative direction context at session start
# This script checks for direction files and reports their status

set -euo pipefail

# Read hook input
input=$(cat)
cwd=$(echo "$input" | jq -r '.cwd // ""')

# Default to current directory if not provided
if [ -z "$cwd" ] || [ "$cwd" == "null" ]; then
  cwd="."
fi

# Check for creative direction file
direction_file="$cwd/.claude/creative-direction.local.md"
status_file="$cwd/.claude/project-status.md"
architecture_dir="$cwd/.claude/architecture"

output=""

# Check creative direction
if [ -f "$direction_file" ]; then
  # Extract key settings from frontmatter
  art_style=$(grep -E "^art_style:" "$direction_file" 2>/dev/null | head -1 | cut -d':' -f2- | xargs || echo "")

  if [ -n "$art_style" ]; then
    output="Creative direction loaded. Art style: $art_style"
  else
    output="Creative direction file exists but may need configuration."
  fi
else
  output="No creative direction file found. Consider running /establish-vision to set up project direction."
fi

# Check project status
if [ -f "$status_file" ]; then
  output="$output | Project status file present."
fi

# Check architecture decisions
if [ -d "$architecture_dir" ]; then
  adr_count=$(find "$architecture_dir" -name "*.md" -type f 2>/dev/null | wc -l || echo "0")
  if [ "$adr_count" -gt "1" ]; then
    output="$output | $adr_count architecture decisions documented."
  fi
fi

# Output for Claude's context
if [ -n "$output" ]; then
  echo "{\"systemMessage\": \"$output\"}"
else
  echo "{}"
fi
