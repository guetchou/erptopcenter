#!/usr/bin/env bash
set -euo pipefail

# Bootstrap client WSL / Linux serveur
# Usage:
#   ./bootstrap_client.sh --repo https://github.com/guetchou/erptopcenter.git --tag v1.0.1 --site client.example.com --modules core,branding --admin-password 'StrongPass!'

REPO_URL=""
TAG=""
SITE=""
MODULES="core,branding"
ADMIN_PASSWORD=""
WORKDIR="/opt/erptopcenter"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO_URL="$2"; shift 2 ;;
    --tag) TAG="$2"; shift 2 ;;
    --site) SITE="$2"; shift 2 ;;
    --modules) MODULES="$2"; shift 2 ;;
    --admin-password) ADMIN_PASSWORD="$2"; shift 2 ;;
    --workdir) WORKDIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$REPO_URL" || -z "$TAG" || -z "$SITE" || -z "$ADMIN_PASSWORD" ]]; then
  echo "Missing required args: --repo --tag --site --admin-password"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found"
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "docker compose not found"
  exit 1
fi

sudo mkdir -p "$WORKDIR"
sudo chown -R "$USER":"$USER" "$WORKDIR"

if [[ -d "$WORKDIR/.git" ]]; then
  git -C "$WORKDIR" fetch --tags --all
  git -C "$WORKDIR" checkout "$TAG"
else
  git clone "$REPO_URL" "$WORKDIR"
  git -C "$WORKDIR" checkout "$TAG"
fi

cd "$WORKDIR/deploy/docker"

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

# VERSION = tag de release
if grep -q '^VERSION=' .env; then
  sed -i "s/^VERSION=.*/VERSION=$TAG/" .env
else
  echo "VERSION=$TAG" >> .env
fi

# SITE par d?faut (peut ?tre multi-site ensuite)
if grep -q '^FRAPPE_SITE_NAME=' .env; then
  sed -i "s/^FRAPPE_SITE_NAME=.*/FRAPPE_SITE_NAME=$SITE/" .env
else
  echo "FRAPPE_SITE_NAME=$SITE" >> .env
fi

if ! grep -q '^MYSQL_ROOT_PASSWORD=' .env; then
  echo "MYSQL_ROOT_PASSWORD=change_me" >> .env
  echo "Set MYSQL_ROOT_PASSWORD in $WORKDIR/deploy/docker/.env before production use."
fi

ADMIN_PASSWORD="$ADMIN_PASSWORD" ./install.sh --site "$SITE" --modules "$MODULES" --demo no

./healthcheck.sh "http://localhost:8082/api/method/ping"
echo "Bootstrap OK for $SITE on tag $TAG"
