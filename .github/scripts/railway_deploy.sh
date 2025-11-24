#!/bin/sh
# railway_deploy.sh — deploys repository to a Railway environment
# Usage: .github/scripts/railway_deploy.sh <ENV_ID>

set -euo pipefail

ENV_ID=${1:-}

if [ -z "${RAILWAY_TOKEN:-}" ]; then
  echo "ERROR: RAILWAY_TOKEN not set"
  exit 1
fi

if [ -z "${PROJECT_ID:-}" ]; then
  echo "ERROR: PROJECT_ID not set"
  exit 1
fi

if [ -z "$ENV_ID" ]; then
  echo "Usage: $0 <ENVIRONMENT_ID>"
  exit 1
fi

echo "Installing Railway CLI..."
curl -fsSL https://railway.app/cli | sh
export PATH="$HOME/.railway/bin:$PATH"

echo "Linking project..."
# Try linking the project; ignore failures
railway link --project "$PROJECT_ID" || true

echo "Starting deployment to environment: $ENV_ID"
# Detach so the CLI returns; adjust flags as needed for your setup
railway up --environment "$ENV_ID" --detach

echo "Deployment triggered for environment: $ENV_ID"
exit 0
