# RELEASE NOTES

Ce fichier est mis ? jour ? chaque tag `vX.Y.Z`.

## Processus de release

Contexte: h?te CI/CD (GitHub Actions).

1. `git checkout main && git pull --ff-only`
2. `git tag vX.Y.Z`
3. `git push origin vX.Y.Z`
4. Workflow `Release` ex?cute:
   - build/push image immuable GHCR
   - smoke test image
   - SBOM + scan vuln?rabilit?s
   - upload artifacts (`compose`, scripts, docs)

## v1.0.0

- Initialisation du socle industrialisation:
  - apps `topcenter_core` (patches idempotents cong?s/paie)
  - app `topcenter_branding` (Tenant Branding Settings)
  - compose prod/dev + scripts install/upgrade/rollback/healthcheck
  - CI release sur tags

## Template nouvelle release

### vX.Y.Z (YYYY-MM-DD)

- Added:
- Changed:
- Fixed:
- Security:
- Migration notes:
- Rollback notes:
