FROM frappe/erpnext:v15.94.1 AS base

# Ici, on pourrait remplacer par ton image custom existante si n?cessaire :
# FROM local/erpnext-custom:v15.94.1 AS base

USER root

# Copier apps + datasets produit dans le bench (chown pour pip install -e en user frappe)
COPY apps /home/frappe/frappe-bench/apps
COPY datasets /home/frappe/frappe-bench/datasets
RUN chown -R frappe:frappe /home/frappe/frappe-bench/apps /home/frappe/frappe-bench/datasets

USER frappe
WORKDIR /home/frappe/frappe-bench

# Installer les apps produit (editable) dans l'env (align? deploy/modules.yaml)
RUN for app in topcenter_core topcenter_branding topcenter_hr topcenter_finance topcenter_transport topcenter_cleaning topcenter_callcenter; do \
      [ -d "apps/$app" ] && bench pip install -e "apps/$app" || true; \
    done

# Build des assets une seule fois ? l'image
RUN bench build

# Image finale (r?utilise la m?me, build en place)
FROM base

USER frappe
WORKDIR /home/frappe/frappe-bench
