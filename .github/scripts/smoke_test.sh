#!/bin/sh
# smoke_test.sh — simple healthcheck runner
# Usage: smoke_test.sh <URL>

set -euo pipefail

URL=${1:-}

if [ -z "$URL" ]; then
  echo "No healthcheck URL provided, skipping smoke test"
  exit 78
fi

echo "Running smoke test against: $URL"

status=$(curl --max-time 10 -s -o /dev/null -w "%{http_code}" "$URL" || true)
echo "HTTP status: $status"

if [ "$status" -ge 200 ] && [ "$status" -lt 400 ]; then
  echo "Smoke test passed"
  exit 0
fi

echo "Smoke test failed"
exit 2
