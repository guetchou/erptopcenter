#!/usr/bin/env bash
set -euo pipefail

# Usage:
#  ./deploy/docker/install.sh --site erp.topcenter.cg --modules core,branding,hr --demo no

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

SITE=""
MODULES="core"
DEMO="no"

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

echo "=== Installation TopCenter ERPNext ==="
echo "Site: $SITE"
echo "Modules: $MODULES"
echo "Demo data: $DEMO"
echo "--------------------------------------"

cd "$ROOT_DIR/deploy/docker"

# 1) Lancer l'infra minimale
docker compose -f compose.prod.yaml up -d db redis-cache redis-queue

# 2) Créer le site si absent + installer apps
docker compose -f compose.prod.yaml exec backend bash -lc "
  cd /home/frappe/frappe-bench
  if ! ls sites | grep -qx '$SITE'; then
    echo 'Création du site $SITE...'
    bench new-site '$SITE' --no-mariadb-socket --admin-password admin --db-root-password \"\$MYSQL_ROOT_PASSWORD\"
  else
    echo 'Site $SITE déjà présent, skip new-site.'
  fi

  bench --site '$SITE' list-apps | grep -q erpnext || bench --site '$SITE' install-app erpnext
  bench --site '$SITE' list-apps | grep -q hrms || bench --site '$SITE' install-app hrms

  if echo '$MODULES' | grep -q 'core'; then
    bench --site '$SITE' install-app topcenter_core || true
  fi
  if echo '$MODULES' | grep -q 'branding'; then
    bench --site '$SITE' install-app topcenter_branding || true
  fi
  if echo '$MODULES' | grep -q 'hr'; then
    bench --site '$SITE' install-app topcenter_hr || true
  fi

  bench --site '$SITE' migrate
"

# 3) Dataset demo (optionnel)
if [[ "$DEMO" == "yes" ]]; then
  docker compose -f compose.prod.yaml exec backend bash -lc "
    cd /home/frappe/frappe-bench && \
    bench --site '$SITE' execute datasets.demo.seed.run
  "
fi

echo "Installation terminée pour le site $SITE."

