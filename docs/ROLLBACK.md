# ROLLBACK – Revenir à une version précédente

## Principe

- Les images Docker sont taguées `vX.Y.Z`.
- En cas de souci après un déploiement, on revient au tag précédent.

## Procédure

```bash
cd deploy/docker
./rollback.sh vX.Y.(Z-1)
```

Ensuite :

- Vérifier l’état des sites.
- Si des migrations de schéma étaient irréversibles, consulter les notes dans `docs/RELEASE.md` avant rollback.

