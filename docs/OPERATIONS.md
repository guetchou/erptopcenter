# OPERATIONS – Exploitation TopCenter ERPNext

**Test et itération Docker (prod + dev)** : voir [DOCKER-TEST.md](DOCKER-TEST.md).

## Démarrage / Arrêt

```bash
cd deploy/docker
docker compose -f compose.prod.yaml up -d      # démarrage
docker compose -f compose.prod.yaml down       # arrêt (non recommandé en prod sans backup)
```

## Healthcheck

```bash
./deploy/docker/healthcheck.sh http://localhost:8082/api/method/ping
```

## Sauvegardes

- Base de données : `mysqldump` du volume `db-data`.
- Sites : archive du volume `sites`.

## Restauration

1. Restaurer la base dans le conteneur `db`.
2. Restaurer le volume `sites`.
3. Relancer `docker compose up -d` puis `bench migrate` sur chaque site.

---

## RISQUES & MITIGATIONS (basés sur l’existant observé)

| Risque observé | Impact | Mitigation (produit industrialisé) |
|----------------|--------|-------------------------------------|
| **pip install au démarrage** (conteneurs) | Dépendances non figées, builds non reproductibles, échecs réseau au boot | Image immuable : toutes les apps sont installées au **build** (Dockerfile `RUN bench pip install -e apps/...`). Aucun `pip install` dans la commande de démarrage en prod. |
| **Bind mounts patches** (`/opt/frappe_docker/patches/*`) | Déploiement dépend du chemin local, pas de versioning propre, impossible livraison client | Patches et correctifs sont **dans les apps** (ex. `topcenter_core/patches/v1_0/`). Livrés avec l’image. |
| **Volume apps en prod** | Modifications manuelles possibles, pas d’immutabilité, fuite IP si volume livré | `compose.prod.yaml` : **aucun volume `apps`**. Seuls `sites` et `logs` sont montés. Apps figées dans l’image. |
| **Scripts setup_* dans sites/** | Scripts hors Git, non reproductibles, perdus au recréation site | Logique déplacée dans **patches idempotents** (hooks `after_migrate`) et **fixtures** déclarées dans `hooks.py`. |
| **Customisations non versionnées** (114 Custom Fields, 141 Property Setter, etc.) | Dérive entre environnements, pas de rollback propre | Export JSON horodaté (`scripts/export_customizations.py`), **fixtures** dans `topcenter_core` par filtres DocType, rapport `customizations_report.md`. |
| **Absence de versioning / tag** | Impossible de déployer une version précise ou de rollback | Tags Git `vX.Y.Z`, CI sur tag, image `ghcr.io/.../<tag>`, `upgrade.sh <tag>` et `rollback.sh <tag>`. |
| **Secrets / env en clair** | Fuite de mots de passe ou clés | `.env` hors Git, `deploy/docker/.env.example` sans valeurs sensibles. Secrets injectés via env ou secret manager. |

