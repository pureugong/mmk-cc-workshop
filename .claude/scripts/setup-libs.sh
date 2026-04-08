#!/bin/bash
# Install libraries needed for this project
# Runs at SessionStart — only in remote environments

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

echo "=== Installing Libraries ==="

# yt-dlp: download YouTube transcripts
if command -v yt-dlp >/dev/null 2>&1; then
  echo "yt-dlp    : $(yt-dlp --version) (already installed)"
else
  echo "yt-dlp    : installing..."
  pip install -q yt-dlp 2>/dev/null || pip3 install -q yt-dlp 2>/dev/null || {
    echo "yt-dlp    : FAILED (pip not available)"
    echo "=== Done ==="
    exit 0
  }
  echo "yt-dlp    : $(yt-dlp --version) (installed)"
fi

echo "=== Done ==="
exit 0
