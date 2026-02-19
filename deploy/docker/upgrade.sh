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

# Migration sur chaque site valide (site_config.json pr?sent)
docker compose -f compose.prod.yaml exec backend bash -lc '
  cd /home/frappe/frappe-bench
  for s in $(find sites -mindepth 1 -maxdepth 1 -type d -exec test -f "{}/site_config.json" \; -print | xargs -n1 basename); do
    echo "Migrating site: $s"
    bench --site "$s" migrate
  done
'

# V?rification assets + ping
./healthcheck.sh "http://localhost:8082/api/method/ping"

echo "Upgrade termin?."
