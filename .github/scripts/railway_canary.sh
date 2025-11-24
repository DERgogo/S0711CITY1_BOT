#!/bin/sh
# railway_canary.sh — deploy a canary, run smoke tests, optionally promote
# Usage: railway_canary.sh <CANARY_ENV_ID> <PROD_ENV_ID> [PROMOTE_ON_SUCCESS=yes]

set -euo pipefail

CANARY_ENV=${1:-}
PROD_ENV=${2:-}
PROMOTE_ON_SUCCESS=${3:-yes}

if [ -z "${RAILWAY_TOKEN:-}" ]; then
  echo "ERROR: RAILWAY_TOKEN not set"
  exit 1
fi
if [ -z "${PROJECT_ID:-}" ]; then
  echo "ERROR: PROJECT_ID not set"
  exit 1
fi
if [ -z "$CANARY_ENV" ] || [ -z "$PROD_ENV" ]; then
  echo "Usage: $0 <CANARY_ENV_ID> <PROD_ENV_ID> [PROMOTE_ON_SUCCESS=yes]"
  exit 1
fi

echo "Installing Railway CLI..."
curl -fsSL https://railway.app/cli | sh
export PATH="$HOME/.railway/bin:$PATH"

railway login --token "$RAILWAY_TOKEN"

echo "Deploying canary to environment: $CANARY_ENV"
railway up --environment "$CANARY_ENV" --detach

echo "Waiting briefly for canary startup..."
sleep 8

# Run smoke test if DEPLOY_HEALTHCHECK_URL provided
if [ -n "${DEPLOY_HEALTHCHECK_URL:-}" ]; then
  echo "Running smoke test against: $DEPLOY_HEALTHCHECK_URL"
  if ! sh .github/scripts/smoke_test.sh "$DEPLOY_HEALTHCHECK_URL"; then
    echo "Canary smoke test failed — aborting"
    exit 2
  fi
else
  echo "No DEPLOY_HEALTHCHECK_URL defined — skipping smoke test"
fi

if [ "$PROMOTE_ON_SUCCESS" = "yes" ]; then
  echo "Promoting canary commit to production ($PROD_ENV)"
  railway up --environment "$PROD_ENV" --detach
  echo "Promotion triggered"
else
  echo "PROMOTE_ON_SUCCESS != yes — leaving canary running"
fi

exit 0
