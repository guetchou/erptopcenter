# Modules a la carte

## Vue d'ensemble

Le produit erptopcenter permet d'installer un **noyau** (core) et des **modules metier optionnels** via `install.sh --modules`.

| Module | Apps installees | Description |
|--------|-----------------|-------------|
| **core** | erpnext, hrms, topcenter_core, topcenter_branding | Noyau obligatoire |
| **hr** | topcenter_hr | Extensions RH (refactor congo_hrms) |
| **finance** | topcenter_finance | Extensions Finance / Tresorerie |
| **transport** | topcenter_transport | Module Transport |
| **cleaning** | topcenter_cleaning | Module Cleaning (refactor cleaning_crm) |
| **callcenter** | topcenter_callcenter | Module Call Center |

## Fichiers de reference

- **deploy/modules.yaml** : liste des modules et des apps par module.
- **deploy/docker/install.sh** : script d'installation ; `--modules core,hr,finance` installe le core puis topcenter_hr et topcenter_finance.
- **deploy/docker/Dockerfile** : installe en image toutes les apps `topcenter_*` presentes dans `apps/`.

## Structure des apps metier

Chaque module metier est une app Frappe minimale (squelette) :

- `apps/topcenter_hr/`, `topcenter_finance/`, `topcenter_transport/`, `topcenter_cleaning/`, `topcenter_callcenter/`
- Contenu type : `setup.py`, `MANIFEST.in`, `README.md`, `topcenter_<module>/__init__.py`, `topcenter_<module>/hooks.py`

Les squelettes sont **installables** (`bench install-app topcenter_hr` etc.) et pret pour le refactor (migration de congo_hrms vers topcenter_hr, cleaning_crm vers topcenter_cleaning, etc.).

## Exemples de commandes

```bash
# Installation minimale (core uniquement)
./deploy/docker/install.sh --site erp.topcenter.cg --modules core

# Core + HR + Finance
./deploy/docker/install.sh --site erp.topcenter.cg --modules core,hr,finance

# Tous les modules
./deploy/docker/install.sh --site erp.topcenter.cg --modules core,hr,finance,transport,cleaning,callcenter
```

## Suite (refactor)

- **topcenter_hr** : migrer customisations, Print Formats, workflows et logique depuis congo_hrms.
- **topcenter_cleaning** : migrer depuis cleaning_crm.
- **topcenter_finance**, **topcenter_transport**, **topcenter_callcenter** : ajouter DocTypes et logique selon besoins metier.
