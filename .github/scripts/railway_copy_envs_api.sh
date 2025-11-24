#!/bin/sh
# railway_copy_envs_api.sh — copy env vars using Railway GraphQL API
# Usage: railway_copy_envs_api.sh <SOURCE_ENV_ID> <TARGET_ENV_ID>
# Requires: RAILWAY_TOKEN, PROJECT_ID

set -euo pipefail

SRC_ENV=${1:-}
TGT_ENV=${2:-}

if [ -z "${RAILWAY_TOKEN:-}" ]; then
  echo "ERROR: RAILWAY_TOKEN not set"
  exit 1
fi
if [ -z "${PROJECT_ID:-}" ]; then
  echo "ERROR: PROJECT_ID not set"
  exit 1
fi
if [ -z "$SRC_ENV" ] || [ -z "$TGT_ENV" ]; then
  echo "Usage: $0 <SOURCE_ENV_ID> <TARGET_ENV_ID>"
  exit 1
fi

API_URL="https://api.railway.app/graphql"

echo "Querying Railway GraphQL API for variables in source environment: $SRC_ENV"

read -r -d '' QUERY <<'GRAPHQL'
query GetEnvironmentVariables($projectId: ID!, $envId: ID!) {
  project(id: $projectId) {
    environments {
      id
      name
      variables {
        key
        value
      }
    }
  }
}
GRAPHQL

payload=$(jq -n --arg pj "$PROJECT_ID" --arg ev "$SRC_ENV" --arg query "$QUERY" '{query: $query, variables: {projectId: $pj, envId: $ev}}')

resp=$(curl -sS -X POST "$API_URL" \
  -H "Authorization: Bearer $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$payload") || true

if [ -z "$resp" ]; then
  echo "Empty response from API — falling back to CLI method"
  .github/scripts/railway_copy_envs.sh "$SRC_ENV" "$TGT_ENV"
  exit 0
fi

# Try to locate variables in common response shapes
vars=$(echo "$resp" | jq -r '.data.project.environments[] | select(.id=="'"$SRC_ENV"'" ) | .variables // empty')

if [ -z "$vars" ] || [ "$vars" = "null" ]; then
  # Try alternative path: top-level environment object
  vars=$(echo "$resp" | jq -r '.data.environment.variables // empty')
fi

if [ -z "$vars" ] || [ "$vars" = "null" ] || [ "$vars" = "[]" ]; then
  echo "Could not parse variables from GraphQL response. Response snippet:" >&2
  echo "$resp" | jq 'del(.data.project.environments[].variables[].value) | .data' || true
  echo "Falling back to CLI copy (best-effort)"
  .github/scripts/railway_copy_envs.sh "$SRC_ENV" "$TGT_ENV"
  exit 0
fi

echo "$vars" | jq -c '.[]' | while read -r item; do
  key=$(echo "$item" | jq -r '.key')
  value=$(echo "$item" | jq -r '.value')
  echo "Setting variable $key on target env $TGT_ENV"

  # GraphQL mutation: try a common mutation name; if not present, fallback to CLI
  MUTATION='mutation SetVariable($envId: ID!, $key: String!, $value: String!) { environmentVariableSet(environment: $envId, key: $key, value: $value) { key } }'
  mpayload=$(jq -n --arg env "$TGT_ENV" --arg k "$key" --arg v "$value" '{query: $MUTATION, variables: {envId: $env, key: $k, value: $v}}')

  mresp=$(curl -sS -X POST "$API_URL" \
    -H "Authorization: Bearer $RAILWAY_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$mpayload") || true

  ok=$(echo "$mresp" | jq -r '.data.environmentVariableSet.key // empty' 2>/dev/null || true)
  if [ -n "$ok" ]; then
    echo "Set $ok via GraphQL"
  else
    echo "GraphQL set failed for $key, falling back to CLI set"
    railway variables set --environment "$TGT_ENV" "$key" "$value" || echo "CLI set failed for $key"
  fi
done

echo "Env copy complete"
exit 0
