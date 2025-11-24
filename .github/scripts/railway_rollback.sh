#!/bin/sh
# railway_rollback.sh — best-effort rollback helper
# Usage: railway_rollback.sh [RELEASE_ID]
# If RELEASE_ID is omitted, the script will print guidance.

set -euo pipefail

RELEASE_ID=${1:-}

if [ -z "${RAILWAY_TOKEN:-}" ]; then
  echo "ERROR: RAILWAY_TOKEN not set"
  exit 1
fi

echo "Installing Railway CLI (for rollback)..."
curl -fsSL https://railway.app/cli | sh
export PATH="$HOME/.railway/bin:$PATH"

if [ -n "$RELEASE_ID" ]; then
  echo "Attempting to rollback to release: $RELEASE_ID"
  # The Railway CLI may support a releases:rollback command; try best-effort
  railway releases:rollback "$RELEASE_ID" || (
    echo "railway releases:rollback not available or failed — please rollback manually via Railway console"
    exit 2
  )
  echo "Rollback attempted"
  exit 0
fi

echo "No RELEASE_ID provided. To rollback manually, visit the Railway project dashboard and promote/rollback a previous release."
exit 0
