# TopCenter ERPNext Product

Produit industrialise ERPNext/Frappe pour SaaS, on-prem et WSL.

## Branching et versioning

- Branches: main, develop, elease/*
- Tags de release: X.Y.Z
- Notes de release: docs/RELEASE.md

## Commandes cles (avec contexte)

### 1) Initialiser le repo (hote)

`ash
git clone <repo-url> topcenter-erpnext-product
cd topcenter-erpnext-product
git checkout develop
`

### 2) Build local image (hote)

`ash
docker build -f deploy/docker/Dockerfile -t ghcr.io/topcenter/topcenter-erpnext:local .
`

### 3) Publier un tag release (hote)

`ash
git checkout main
git pull --ff-only
git tag v1.0.0
git push origin v1.0.0
`

### 4) Installation client on-prem/WSL (hote)

`ash
cd deploy/docker
cp .env.example .env
# editer .env: MYSQL_ROOT_PASSWORD, FRAPPE_SITE_NAME, VERSION
ADMIN_PASSWORD='StrongPass!' ./install.sh --site client.example.com --modules core,hr,finance --demo no
`

### 5) Provisionner un nouveau tenant SaaS (hote)

`ash
cd deploy/docker
ADMIN_PASSWORD='StrongPass!' ./install.sh --site tenant2.example.com --modules core,branding,hr --demo no
`

### 6) Upgrade / Rollback (hote)

`ash
cd deploy/docker
./upgrade.sh v1.0.1
./rollback.sh v1.0.0
`

## Modules a la carte

Voir deploy/modules.yaml et docs/MODULES-A-LA-CARTE.md.

## Qualite operationnelle

- Checklist: docs/RQC.md
- Architecture: docs/ARCHITECTURE.md
- Ops/backup/restore: docs/OPERATIONS.md
