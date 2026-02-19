# ARCHITECTURE PRODUIT TOPCENTER ERPNext

## 1. Monorepo

Ce d?p?t contient:

- `apps/topcenter_core`: noyau fonctionnel (fixtures + patches Congo).
- `apps/topcenter_branding`: branding multi-tenant (DocType Tenant Branding Settings).
- `apps/topcenter_hr`, `apps/topcenter_finance`, `apps/topcenter_transport`, `apps/topcenter_cleaning`, `apps/topcenter_callcenter`: modules ? la carte.
- `deploy/docker`: images et docker-compose (prod/dev).
- `datasets/demo`: jeu de donn?es d?mo idempotent.
- `docs/`: documentation d'architecture, op?rations, s?curit?, releases.

## 2. Branching / Release

- Branches: `main`, `develop`, `release/*`
- Tags: `vX.Y.Z`
- Pipeline release: `.github/workflows/release.yml` (build image immuable + artifacts)
- Changelog: `docs/RELEASE.md`

## 3. Image Docker immuable

L'image `ghcr.io/topcenter/topcenter-erpnext:<tag>` embarque:

- Frappe, ERPNext, HRMS et apps TopCenter.
- Assets build?s (`bench build`) au moment du build CI.
- Aucun `pip install` au d?marrage en production.

En production:

- Aucun volume `apps`.
- Volumes autoris?s: `sites`, `logs`, `db-data`, `redis-*`.

## 4. Customisations

Les customisations UI/DB (Custom Field, Property Setter, Print Format, Workflow, Roles, etc.) sont:

- Export?es en JSON + rapport via `scripts/export_customizations.py`.
- Converties en fixtures versionn?es dans `apps/topcenter_core/topcenter_core/fixtures/`.
- Compl?t?es par des patches idempotents (`topcenter_core.patches.v1_0.*`).

Aucune modification manuelle en prod: tout passe par Git + release.

## 5. Branding multi-tenant

- DocType `Tenant Branding Settings` par site.
- Hook `topcenter_branding.branding.apply_branding_for_current_site` apr?s migration.
- Print Formats consomment `branding.*` (logo, couleurs, footer, signature) sans duplication par client.

## 6. Modules ? la carte

Le fichier `deploy/modules.yaml` d?crit les plans:

- `core`: obligatoire (ERPNext/HRMS + topcenter_core + topcenter_branding).
- `hr`, `finance`, `transport`, `cleaning`, `callcenter`: optionnels.

`deploy/docker/install.sh` accepte `--modules core,hr,finance` et installe uniquement les apps n?cessaires.
