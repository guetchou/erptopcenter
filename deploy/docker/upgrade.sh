#!/usr/bin/env bash
set -euo pipefail

# Usage: ./deploy/docker/upgrade.sh v1.0.1

TAG="${1:-}"
if [[ -z "$TAG" ]]; then
  echo "Usage: $0 <tag>"
  exit 1
fi

cd "$(dirname "${BASH_SOURCE[0]}")"

export VERSION="$TAG"

echo "=== Upgrade vers image ghcr.io/topcenter/topcenter-erpnext:$TAG ==="
docker compose -f compose.prod.yaml pull backend frontend websocket scheduler queue-short queue-long
docker compose -f compose.prod.yaml up -d

docker compose -f compose.prod.yaml exec backend bash -lc "
  cd /home/frappe/frappe-bench
  for s in \$(ls sites); do
    echo \"Migrating site: \$s\"
    bench --site \"\$s\" migrate
  done
"

echo "Upgrade terminé."

