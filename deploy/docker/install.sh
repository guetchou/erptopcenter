#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   COMPOSE_FILES='-f compose.prod.yaml -f compose.override.test.yaml' \
#   VERSION=test ADMIN_PASSWORD='StrongPass!' \
#   ./install.sh --site qa.local --modules core,branding --demo no

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

SITE=""
MODULES="core"
DEMO="no"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-}"
COMPOSE_FILES="${COMPOSE_FILES:--f compose.prod.yaml}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --site) SITE="$2"; shift 2 ;;
    --modules) MODULES="$2"; shift 2 ;;
    --demo) DEMO="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$SITE" ]]; then
  echo "Erreur: --site est obligatoire"
  exit 1
fi
if [[ -z "$ADMIN_PASSWORD" ]]; then
  echo "Erreur: variable ADMIN_PASSWORD obligatoire"
  exit 1
fi

echo "=== Installation TopCenter ERPNext ==="
echo "Site: $SITE"
echo "Modules: $MODULES"
echo "Demo data: $DEMO"
echo "Compose: $COMPOSE_FILES"

cd "$ROOT_DIR/deploy/docker"

docker compose $COMPOSE_FILES up -d

for i in $(seq 1 60); do
  if docker compose $COMPOSE_FILES exec -T backend curl -fsS http://localhost:8000/api/method/ping >/dev/null 2>&1; then
    echo "Backend ready"
    break
  fi
  if [[ $i -eq 60 ]]; then
    echo "Erreur: backend non pret"
    exit 1
  fi
  sleep 2
done

docker compose $COMPOSE_FILES exec -T backend bash -lc "
set -e
cd /home/frappe/frappe-bench

if [[ ! -f \"sites/common_site_config.json\" ]] || [[ \"\$(cat sites/common_site_config.json)\" == \"{}\" ]]; then
  cat > sites/common_site_config.json <<'JSON'
{\"db_host\":\"db\",\"redis_cache\":\"redis://redis-cache:6379\",\"redis_queue\":\"redis://redis-queue:6379\",\"redis_socketio\":\"redis://redis-queue:6379\"}
JSON
fi

if [[ ! -f \"sites/$SITE/site_config.json\" ]]; then
  bench new-site '$SITE' --mariadb-user-host-login-scope='%' --admin-password '$ADMIN_PASSWORD' --db-root-password \"\$MYSQL_ROOT_PASSWORD\"
fi

for a in topcenter_core topcenter_branding topcenter_hr topcenter_finance topcenter_transport topcenter_cleaning topcenter_callcenter; do
  if [ -d \"apps/\$a\" ] && ! grep -qx \"\$a\" sites/apps.txt 2>/dev/null; then
    echo \"\$a\" >> sites/apps.txt
  fi
done

bench --site '$SITE' list-apps | grep -q erpnext || bench --site '$SITE' install-app erpnext
if [ -d apps/hrms ]; then
  bench --site '$SITE' list-apps | grep -q hrms || bench --site '$SITE' install-app hrms
fi

if echo '$MODULES' | grep -qE 'core|branding'; then
  bench --site '$SITE' list-apps | grep -q topcenter_core || bench --site '$SITE' install-app topcenter_core
  bench --site '$SITE' list-apps | grep -q topcenter_branding || bench --site '$SITE' install-app topcenter_branding
fi

for mod in hr finance transport cleaning callcenter; do
  if echo '$MODULES' | grep -q \"\$mod\"; then
    app=topcenter_\$mod
    if [ -d \"apps/\$app\" ]; then
      bench --site '$SITE' list-apps | grep -q \"\$app\" || bench --site '$SITE' install-app \"\$app\"
    else
      echo \"ERREUR: module '\$app' absent de l image\"
      exit 1
    fi
  fi
done

bench --site '$SITE' migrate
bench --site '$SITE' clear-cache
"

if [[ "$DEMO" == "yes" ]]; then
  docker compose $COMPOSE_FILES cp "$ROOT_DIR/datasets" backend:/home/frappe/frappe-bench/
  docker compose $COMPOSE_FILES exec -T backend bash -lc "cd /home/frappe/frappe-bench && bench --site '$SITE' execute datasets.demo.seed.run"
fi

docker compose $COMPOSE_FILES exec -T backend bash -lc "cd /home/frappe/frappe-bench && bench --site '$SITE' execute topcenter_branding.branding.apply_branding_for_current_site || true"

echo "Installation terminee pour $SITE"
