# CUSTOMISATIONS ? Strat?gie produit

## Objectif

Versionner toutes les customisations ERPNext/Frappe (z?ro custom manuelle en prod).

## 1) Export factuel (contexte: h?te + conteneur backend)

H?te:

```bash
docker cp scripts/export_customizations.py <backend_container>:/tmp/export_customizations.py
```

Conteneur backend:

```bash
cd /home/frappe/frappe-bench
bench --site <site> console
# puis dans la console:
exec(open('/tmp/export_customizations.py').read()); run()
```

R?sultat:

- `/home/frappe/frappe-bench/artifacts/customizations_*.json`
- `/home/frappe/frappe-bench/artifacts/customizations_report_*.md`

## 2) Conversion en fixtures

- Fichiers fixtures versionn?s dans:
  - `apps/topcenter_core/topcenter_core/fixtures/`
- D?claration dans:
  - `apps/topcenter_core/topcenter_core/hooks.py`

## 3) Patches idempotents

- `topcenter_core.patches.v1_0.setup_leave_congo`
- `topcenter_core.patches.v1_0.setup_payroll_congo`

R?gles:

- v?rifier existence avant insert/update
- logger les actions
- relan?able sans effet destructif
