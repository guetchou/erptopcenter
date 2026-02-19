# Branding multi-tenant – Print Formats

## Contexte

L’étape 4 du branding multi-tenant consiste à **brancher tous les Print Formats** sur Tenant Branding Settings : logo, couleurs, footer, signature, Letter Head.

## Ce qui est en place

1. **DocType Tenant Branding Settings**  
   Company, logo, primary_color, secondary_color, footer_text, letter_head_template, print_signature.

2. **apply_branding**  
   Met à jour le logo de la Company et crée/met à jour le Letter Head par défaut (`{Company} - Default Letter Head`).

3. **Hook `pdf_body_html`** (app `topcenter_branding`)  
   Injecte l’objet **`branding`** dans le contexte Jinja de chaque rendu Print Format / PDF. Tous les Print Formats (Jinja ou HTML) reçoivent donc les mêmes variables sans duplication de logique.

## Variables disponibles dans les templates Print Format

Dans tout Print Format de type **Jinja** (ou tout template utilisant le même contexte), les champs suivants sont disponibles via `{{ branding.* }}` :

| Variable | Usage typique |
|----------|----------------|
| `branding.logo_url` | `<img src="{{ branding.logo_url }}">` |
| `branding.primary_color` | Couleur d’en-tête / bordures |
| `branding.secondary_color` | Couleur secondaire |
| `branding.footer_text` | Pied de page texte |
| `branding.print_signature` | Bloc signature (HTML) |
| `branding.company` | Nom de la société |
| `branding.letter_head_template` | Contenu brut du Letter Head (si besoin d’inclusion manuelle) |

Si aucun Tenant Branding Settings n’existe (ou en cas d’erreur), `branding` est un dict avec des chaînes vides ; les templates peuvent tester `{% if branding.logo_url %}`.

## Utiliser le Letter Head par défaut

- **apply_branding** définit un Letter Head par défaut pour le site.  
- Dans un Print Format, ne pas cocher « No Letterhead » et laisser le Letter Head par défaut (ou sélectionner explicitement `{Company} - Default Letter Head`) pour que l’en-tête du Tenant Branding Settings s’affiche automatiquement en haut du PDF.

## Brancher les Print Formats existants

Pour les formats qui ont déjà un HTML/Jinja dédié (ex. « Demande Congé - TopCenter », « Salaire-TopCenter ») :

1. Remplacer les URLs/texte en dur par les variables `branding.*` (logo, couleurs, footer, signature).
2. Si le format n’utilise pas le Letter Head, ajouter en tête du HTML un bloc qui affiche `branding.logo_url`, `branding.primary_color`, etc., ou inclure le contenu du Letter Head si nécessaire.

Aucun changement n’est requis dans la logique métier : seul le template (HTML/Jinja) du Print Format doit référencer `branding`.

## Ordre des hooks

L’app **topcenter_branding** enregistre son hook en premier dans `pdf_body_html` ; les autres hooks (ex. congo_hrms pour le QR) s’exécutent ensuite. Le contexte final contient à la fois `branding` et les autres variables (ex. `get_qr_code`, `qr_code_data_uri`).
