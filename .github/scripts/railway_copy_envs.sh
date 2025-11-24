#!/bin/sh
# railway_copy_envs.sh — copy environment variables from one Railway environment to another
# Usage: railway_copy_envs.sh <SOURCE_ENV_ID> <TARGET_ENV_ID>

set -euo pipefail

SRC=${1:-}
TGT=${2:-}

if [ -z "${RAILWAY_TOKEN:-}" ]; then
  echo "ERROR: RAILWAY_TOKEN not set"
  exit 1
fi
if [ -z "${PROJECT_ID:-}" ]; then
  echo "ERROR: PROJECT_ID not set"
  exit 1
fi
if [ -z "$SRC" ] || [ -z "$TGT" ]; then
  echo "Usage: $0 <SOURCE_ENV_ID> <TARGET_ENV_ID>"
  exit 1
fi

echo "Installing Railway CLI..."
curl -fsSL https://railway.app/cli | sh
export PATH="$HOME/.railway/bin:$PATH"

echo "Logging in..."
railway login --token "$RAILWAY_TOKEN"

echo "Attempting to fetch variables from source environment: $SRC"

# Try JSON output (preferred)
vars_json=""
if railway variables list --environment "$SRC" --json >/dev/null 2>&1; then
  vars_json=$(railway variables list --environment "$SRC" --json 2>/dev/null)
fi

if [ -n "$vars_json" ]; then
  echo "Detected JSON output; parsing variables"
  echo "$vars_json" | jq -r '.[] | "" + .key + "" + .value' | while IFS=$'\u001f' read -r _ k v; do
    echo "Setting $k on target environment"
    railway variables set --environment "$TGT" "$k" "$v" || echo "Failed to set $k"
  done
  exit 0
fi

# Fallback: parse KEY=VALUE lines
if railway variables list --environment "$SRC" >/dev/null 2>&1; then
  railway variables list --environment "$SRC" | while IFS='=' read -r key val; do
    [ -z "$key" ] && continue
    # trim quotes/spaces
    val=$(echo "$val" | sed -e 's/^"//' -e 's/"$//' )
    echo "Setting $key on $TGT"
    railway variables set --environment "$TGT" "$key" "$val" || echo "Failed to set $key"
  done
  exit 0
fi

echo "Unable to list variables with Railway CLI. Please adapt this script to use Railway API or CLI version available in your environment."
exit 2
