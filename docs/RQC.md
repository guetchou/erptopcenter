# RQC – CHECKLIST QUALITÉ RUN / CHANGE

## 1. Avant déploiement

- [ ] Tag Git créé (format `vX.Y.Z`) et poussé.
- [ ] `docs/RELEASE.md` mis à jour avec le tag.
- [ ] Pipeline GitHub Actions `Release` passé au vert.
- [ ] Image disponible sur GHCR (`docker pull ghcr.io/topcenter/topcenter-erpnext:<tag>` OK).

## 2. Déploiement / Upgrade

- [ ] Fichier `.env` renseigné (DB, secrets, FRAPPE_SITE_NAME).
- [ ] `deploy/docker/compose.prod.yaml` validé dans le contexte client (ports, DNS).
- [ ] `deploy/docker/upgrade.sh <tag>` exécuté sans erreur.
- [ ] `bench migrate` succès pour tous les sites (logs vérifiés).
- [ ] Healthcheck HTTP OK (`/api/method/ping` sur chaque site).

## 3. Customisations

- [ ] `bench --site <site> list-apps` montre `topcenter_core` (et modules requis).
- [ ] Export JSON + rapport des customisations conservés en artefacts.
- [ ] Patches `topcenter_core.patches` exécutés sans erreur (aucun nouvel échec dans Error Log).

## 4. Branding

- [ ] DocType `Tenant Branding Settings` existe.
- [ ] Hook `topcenter_branding.branding.apply_branding_for_current_site` exécuté (log OK).
- [ ] Les Print Formats (Demande de congé, Salaire-TopCenter, …) utilisent bien le logo + footer du tenant.

## 5. Sécurité / Anti-patterns

- [ ] Aucun `pip install` dans les scripts de démarrage des conteneurs.
- [ ] Aucun volume `apps` en prod.
- [ ] Aucun bind-mount de scripts dans `sites/` (tous les scripts sont packagés en app).
- [ ] Settings sensibles injectés via secrets/env, pas dans Git.

## 6. Rollback

- [ ] Tag précédent disponible sur GHCR.
- [ ] `rollback.sh` testé en environnement de pré-prod.
- [ ] Retour à l’image précédente OK, sans corruption de données.

