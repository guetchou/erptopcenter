# TopCenter Branding

Branding multi-tenant : **Tenant Branding Settings** + `apply_branding` (Company, Letter Head) + **contexte Print Format / PDF**.

## Print Formats – variables de branding

Le hook `pdf_body_html` injecte un objet **`branding`** dans le contexte Jinja de tous les Print Formats. Dans tout template (type Jinja), vous pouvez utiliser :

| Variable | Description |
|----------|-------------|
| `{{ branding.logo_url }}` | URL du logo (pour `<img src="{{ branding.logo_url }}">`) |
| `{{ branding.logo }}` | Chemin fichier du logo |
| `{{ branding.primary_color }}` | Couleur primaire (hex) |
| `{{ branding.secondary_color }}` | Couleur secondaire (hex) |
| `{{ branding.footer_text }}` | Texte de pied de page |
| `{{ branding.print_signature }}` | Bloc signature (HTML) |
| `{{ branding.company }}` | Nom de la Company liée |
| `{{ branding.letter_head_template }}` | Contenu brut du template Letter Head |

Exemple d'en-tête dans un Print Format :

```html
<div class="print-header">
  {% if branding.logo_url %}
  <img src="{{ branding.logo_url }}" alt="Logo" style="max-height: 60px;" />
  {% endif %}
  <span style="color: {{ branding.primary_color }};">{{ doc.title or doc.name }}</span>
</div>
```

## Letter Head par défaut

`apply_branding()` crée/met à jour un **Letter Head** nommé `{Company} - Default Letter Head` et le définit par défaut. Les Print Formats qui utilisent le Letter Head (sans « No Letterhead ») affichent automatiquement l'en-tête défini dans **Tenant Branding Settings** (champ *Letter Head Template*).
