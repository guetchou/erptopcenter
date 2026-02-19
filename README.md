# TopCenter ERPNext Product

Produit industrialis? ERPNext/Frappe pour SaaS, on-prem et WSL.

## Branching et versioning

- Branches: `main`, `develop`, `release/*`
- Tags de release: `vX.Y.Z`
- Notes de release: `docs/RELEASE.md`

## Commandes cl?s (avec contexte)

### 1) Initialiser le repo (h?te)

```bash
git clone <repo-url> topcenter-erpnext-product
cd topcenter-erpnext-product
git checkout develop
```

### 2) Build local image (h?te)

```bash
docker build -f deploy/docker/Dockerfile -t ghcr.io/topcenter/topcenter-erpnext:local .
```

### 3) Publier un tag release (h?te)

```bash
git checkout main
git pull --ff-only
git tag v1.0.0
git push origin v1.0.0
```

### 4) Installation client on-prem/WSL (h?te)

```bash
cd deploy/docker
cp .env.example .env
# ?diter .env: MYSQL_ROOT_PASSWORD, FRAPPE_SITE_NAME, VERSION
ADMIN_PASSWORD='StrongPass!' ./install.sh --site client.example.com --modules core,hr,finance --demo no
```

### 5) Provisionner un nouveau tenant SaaS (h?te)

```bash
cd deploy/docker
ADMIN_PASSWORD='StrongPass!' ./install.sh --site tenant2.example.com --modules core,branding,hr --demo no
```

### 6) Upgrade / Rollback (h?te)

```bash
cd deploy/docker
./upgrade.sh v1.0.1
./rollback.sh v1.0.0
```

## Modules ? la carte

Voir `deploy/modules.yaml` et `docs/MODULES-A-LA-CARTE.md`.

## Qualit? op?rationnelle

- Checklist: `docs/RQC.md`
- Architecture: `docs/ARCHITECTURE.md`
- Ops/backup/restore: `docs/OPERATIONS.md`
