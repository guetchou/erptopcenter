# ARCHITECTURE PRODUIT TOPCENTER ERPNext

## 1. Monorepo

Ce dépôt contient :

- `apps/topcenter_core` : noyau fonctionnel (fixtures + patches Congo).
- `apps/topcenter_branding` : branding multi-tenant (DocType Tenant Branding Settings).
- `deploy/docker` : images et docker-compose (prod/dev).
- `datasets/demo` : jeu de données démo idempotent.
- `docs/` : documentation d’architecture, opérations, sécurité, releases.

## 2. Image Docker immuable

L’image `ghcr.io/topcenter/topcenter-erpnext:<tag>` embarque :

- Frappe, ERPNext, HRMS, CRM, Drive, Payments, etc.
- Apps TopCenter (`topcenter_core`, `topcenter_branding`, …).
- Assets buildés (`bench build`) au moment du build CI.

En production :

- Aucun volume `apps`.
- Seuls `sites` et `logs` sont montés.

## 3. Customisations

Les customisations UI/DB (Custom Field, Property Setter, Print Format, Workflow, Roles, …) sont :

- Exportées en JSON (scripts/export_customizations.py dans l’ancien environnement).
- Sélectionnées et importées comme fixtures dans `topcenter_core`.
- Complétées par des patches idempotents (`topcenter_core.patches.v1_0.*`).

Aucune modification manuelle en prod : tout passe par Git + release.

## 4. Branding multi-tenant

- DocType `Tenant Branding Settings` par site.
- Hook `topcenter_branding.branding.apply_branding_for_current_site` appliqué après chaque migration.
- Print Formats consomment ces settings (logo, couleurs, footer) → pas de duplication par client.

## 5. Modules à la carte

Le fichier `deploy/modules.yaml` décrit les plans :

- `core` : obligatoire (topcenter_core).
- `branding` : recommandé.
- `hr`, `transport`, `cleaning`, `callcenter` : optionnels.

`deploy/docker/install.sh` accepte `--modules core,hr,branding` et installe uniquement les apps nécessaires pour le site.

