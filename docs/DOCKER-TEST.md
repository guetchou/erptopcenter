# Docker prod/dev – Test et itération

## Prérequis

- Docker et Docker Compose
- Pour **prod** : image `ghcr.io/topcenter/topcenter-erpnext:<tag>` disponible (ou build local avec le même Dockerfile)
- Fichier `.env` dans `deploy/docker/` (copier depuis `.env.example`, renseigner `MYSQL_ROOT_PASSWORD`, `FRAPPE_SITE_NAME` si besoin)

---

## Test stack PROD (image pré-buildée ou locale)

1. **Préparer l’env**
   ```bash
   cd /chemin/erptopcenter/deploy/docker
   cp .env.example .env
   # Éditer .env : MYSQL_ROOT_PASSWORD, FRAPPE_SITE_NAME
   ```

2. **Option A – Image registry**  
   Définir `VERSION` si autre que `v1.0.0` :
   ```bash
   export VERSION=v1.0.0
   ```

   **Option B – Build image locale (pour test sans push)**  
   Build depuis la racine du produit :
   ```bash
   docker build -f deploy/docker/Dockerfile -t topcenter-erpnext:test .
   ```
   Puis dans `compose.prod.yaml` utiliser `image: topcenter-erpnext:test` temporairement, ou utiliser un override.

3. **Lancer la stack**
   ```bash
   docker compose -f compose.prod.yaml up -d
   ```

4. **Installation du site (première fois)**
   ```bash
   ./install.sh --site erp.topcenter.cg --modules core --demo no
   ```

5. **Vérifications**
   - Healthcheck : `./healthcheck.sh http://localhost:8082/api/method/ping` (frontend) ou depuis le host vers le port exposé (8082)
   - Ou : `curl -s http://localhost:8082/api/method/ping`

6. **Logs**
   ```bash
   docker compose -f compose.prod.yaml logs -f backend
   ```

---

## Test stack DEV (build local + volume apps)

1. **Préparer l’env**
   ```bash
   cd /chemin/erptopcenter/deploy/docker
   cp .env.example .env
   # MYSQL_ROOT_PASSWORD obligatoire (ex. admin pour dev)
   ```

2. **Build et démarrage**
   ```bash
   docker compose -f compose.dev.yaml build
   docker compose -f compose.dev.yaml up -d
   ```

3. **Création du site (première fois)**  
   Le backend dev utilise par défaut `FRAPPE_SITE_NAME=erp.topcenter.local`. Créer le site à la main ou via un script :
   ```bash
   docker compose -f compose.dev.yaml exec backend bash -lc "
     cd /home/frappe/frappe-bench
     bench new-site erp.topcenter.local --no-mariadb-socket --admin-password admin --db-root-password \"\$MYSQL_ROOT_PASSWORD\"
     bench --site erp.topcenter.local install-app erpnext
     bench --site erp.topcenter.local install-app hrms
     bench --site erp.topcenter.local install-app topcenter_core
     bench --site erp.topcenter.local install-app topcenter_branding
     bench --site erp.topcenter.local migrate
   "
   ```

4. **Accès**  
   Backend exposé sur `http://localhost:8000` (pas de frontend nginx en dev par défaut).

5. **Itération**  
   Les apps sont montées depuis `../../apps` ; modifier le code puis redémarrer le backend (ou recharger selon la config) sans rebuild :
   ```bash
   docker compose -f compose.dev.yaml restart backend
   ```

---

## Upgrade / Rollback (prod)

- **Upgrade** vers une nouvelle image (tag) :
  ```bash
  ./upgrade.sh v1.0.1
  ```
  Lance un pull des images, recrée les conteneurs, puis `bench migrate` sur chaque site.

- **Rollback** vers une version précédente :
  ```bash
  ./rollback.sh v1.0.0
  ```
  Les migrations éventuellement irréversibles sont à gérer manuellement (voir `rollback.sh`).

---

## Checklist rapide (itération 80 % → 100 %)

- [ ] `.env` créé depuis `.env.example`, `MYSQL_ROOT_PASSWORD` défini
- [ ] Prod : `up -d` puis `install.sh --site ... --modules core` ; healthcheck OK
- [ ] Dev : `compose.dev.yaml` up ; backend répond sur :8000 ; site créé et migrate OK
- [ ] Upgrade : `upgrade.sh <tag>` puis vérifier site et migrate
- [ ] Rollback : `rollback.sh <tag>` puis vérifier
