#!/usr/bin/env bash
set -euo pipefail

# Usage: ./deploy/docker/rollback.sh <previous_tag>

TAG="${1:-}"
if [[ -z "$TAG" ]]; then
  echo "Usage: $0 <previous_tag>"
  exit 1
fi

cd "$(dirname "${BASH_SOURCE[0]}")"

export VERSION="$TAG"

echo "=== Rollback vers ghcr.io/topcenter/topcenter-erpnext:$TAG ==="
docker compose -f compose.prod.yaml pull backend frontend websocket scheduler queue-short queue-long
docker compose -f compose.prod.yaml up -d

./healthcheck.sh "http://localhost:8082/api/method/ping"

echo "Rollback termin?."
echo "NOTE: si une migration irr?versible a ?t? appliqu?e, suivre docs/ROLLBACK.md avant remise en production."
