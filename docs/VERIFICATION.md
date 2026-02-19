# V?rification factuelle ? Industrialisation produit

## P?rim?tre v?rifi?

R?pertoire: `/opt/frappe_docker/erptopcenter`

## R?sultat global

- Socle industrialisation: **impl?ment?**
- Migration progressive depuis l?existant: **pr?par?e** (script export customisations + modules ? la carte + runbooks)

## Points valid?s

1. Monorepo produit
- `apps/`, `deploy/`, `datasets/`, `docs/`, `.github/workflows/release.yml`

2. Core + branding + modules
- `apps/topcenter_core`
- `apps/topcenter_branding`
- modules optionnels `topcenter_hr|finance|transport|cleaning|callcenter`

3. Customisations versionnables
- script: `scripts/export_customizations.py`
- fixtures: `apps/topcenter_core/topcenter_core/fixtures/*.json`
- patches idempotents: `topcenter_core/patches/v1_0/*.py`

4. Docker prod/dev s?par?s
- prod: `deploy/docker/compose.prod.yaml` (pas de volume apps)
- dev: `deploy/docker/compose.dev.yaml` (bind mount apps pour it?ration)

5. CI release
- trigger tags `v*`
- build/push image GHCR
- smoke test image
- SBOM + scan vuln?rabilit?s
- upload artifacts (compose/scripts/docs)

6. CD scripts
- `install.sh` (site/modules/demo + s?curit? ADMIN_PASSWORD)
- `upgrade.sh` (pull + up + migrate multi-sites + healthcheck)
- `rollback.sh` (revert tag + healthcheck)

7. Docs op?rationnelles
- `ARCHITECTURE.md`, `OPERATIONS.md`, `RELEASE.md`, `ROLLBACK.md`, `SECURITY.md`, `CUSTOMIZATIONS.md`, `RQC.md`

## Commandes de contr?le rapide

Contexte h?te:

```bash
cd /opt/frappe_docker/erptopcenter
docker compose -f deploy/docker/compose.prod.yaml config >/dev/null
bash -n deploy/docker/install.sh
bash -n deploy/docker/upgrade.sh
bash -n deploy/docker/rollback.sh
```

Contexte conteneur backend:

```bash
bench --site <site> list-apps
bench --site <site> migrate
```
