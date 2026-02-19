# SECURITY – Bonnes pratiques

- Aucun `pip install` au démarrage des conteneurs.
- Aucun secret (mot de passe DB, token) dans Git :
  - utiliser `.env` + gestionnaire de secrets (GitHub, Docker, etc.).
- Vérifier régulièrement les images de base (frappe/erpnext) pour les mises à jour de sécurité.
- Optionnel : ajouter un scan de vulnérabilités (Trivy, etc.) dans la CI.

