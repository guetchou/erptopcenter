#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8082/api/method/ping}"

curl -fsS "$URL" >/dev/null
echo "OK healthcheck: $URL"
