#!/bin/sh
# traffic_split.sh — generic traffic-splitting plugin stub
# Usage: traffic_split.sh <PROVIDER> <TARGET> <PERCENT>
# Providers supported: cloudflare (plugin must be implemented), nginx (local config reload)

set -euo pipefail

PROVIDER=${1:-}
TARGET=${2:-}
PERCENT=${3:-}

if [ -z "$PROVIDER" ] || [ -z "$TARGET" ] || [ -z "$PERCENT" ]; then
  echo "Usage: $0 <PROVIDER> <TARGET> <PERCENT>"
  exit 1
fi

echo "Traffic split request: provider=$PROVIDER target=$TARGET percent=$PERCENT"

case "$PROVIDER" in
  cloudflare)
    echo "Cloudflare traffic-split requested. This script provides a hook — implement provider-specific calls in .github/scripts/providers/cloudflare.sh"
    if [ -x .github/scripts/providers/cloudflare.sh ]; then
      ./.github/scripts/providers/cloudflare.sh "$TARGET" "$PERCENT"
    else
      echo "No Cloudflare provider script found at .github/scripts/providers/cloudflare.sh — skipping"
    fi
    ;;
  nginx)
    echo "nginx traffic split requested. Expecting that you mount a config and reload nginx. Example:
    - update upstream weights
    - reload nginx
    "
    # No-op: user must implement specifics
    ;;
  *)
    echo "Unknown provider: $PROVIDER. Supported: cloudflare, nginx (stubs)."
    exit 2
    ;;
esac

echo "Traffic split step completed (stub)"
exit 0
