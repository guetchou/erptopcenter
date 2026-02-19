# RQC ? CHECKLIST QUALIT? RUN / CHANGE

## 0. Pr?-requis

- [ ] Contexte h?te: Docker + Docker Compose install?s
- [ ] Contexte conteneur: backend accessible (`docker compose exec backend ...`)

## 1. Avant d?ploiement

- [ ] Tag Git cr?? au format `vX.Y.Z`
- [ ] `docs/RELEASE.md` mis ? jour
- [ ] Pipeline GitHub Actions `Release` vert
- [ ] Image disponible: `docker pull ghcr.io/topcenter/topcenter-erpnext:<tag>`

## 2. D?ploiement / Upgrade (h?te)

- [ ] `.env` renseign? (`MYSQL_ROOT_PASSWORD`, `FRAPPE_SITE_NAME`, `VERSION`)
- [ ] Installation initiale valid?e:
  - `ADMIN_PASSWORD='***' ./deploy/docker/install.sh --site <site> --modules core,hr --demo no`
- [ ] Upgrade valid?:
  - `./deploy/docker/upgrade.sh <tag>`
- [ ] Healthcheck OK:
  - `./deploy/docker/healthcheck.sh http://localhost:8082/api/method/ping`

## 3. Migration multi-sites (conteneur backend)

- [ ] Pour chaque site (avec `site_config.json`), `bench --site <site> migrate` est pass?
- [ ] `bench --site <site> list-apps` contient `topcenter_core` (et modules requis)

## 4. Customisations

- [ ] Export customisations ex?cut? (contexte backend):
  - `exec(open('/tmp/export_customizations.py').read()); run()`
- [ ] Artefacts pr?sents:
  - `/home/frappe/frappe-bench/artifacts/customizations_*.json`
  - `/home/frappe/frappe-bench/artifacts/customizations_report_*.md`
- [ ] Fixtures versionn?es dans `apps/topcenter_core/topcenter_core/fixtures/`

## 5. Branding

- [ ] DocType `Tenant Branding Settings` existe
- [ ] Hook branding ex?cut? apr?s migrate
- [ ] Print Formats consomment `branding.*` (logo/couleurs/footer/signature)

## 6. S?curit? / Anti-patterns

- [ ] Aucun `pip install` dans les commandes de d?marrage prod
- [ ] Aucun volume `apps` en prod
- [ ] Aucun bind-mount patch/prod depuis h?te
- [ ] Aucun script setup copi? dans `sites/` en prod

## 7. Rollback

- [ ] Tag pr?c?dent disponible
- [ ] `./deploy/docker/rollback.sh <tag_precedent>` test? en pr?-prod
- [ ] Notes migrations irr?versibles document?es dans `docs/ROLLBACK.md`
