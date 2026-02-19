from __future__ import unicode_literals

app_name = "topcenter_branding"
app_title = "TopCenter Branding"
app_publisher = "Top Center"
app_description = "Branding multi-tenant pour ERPNext (logos, couleurs, footer, letter head)"
app_email = "contact@topcenter.cg"
app_license = "MIT"

after_migrate = [
    "topcenter_branding.branding.apply_branding_for_current_site",
]

# Contexte Print Format / PDF : expose branding (logo, couleurs, footer, signature) dans tous les Print Formats
pdf_body_html = [
    "topcenter_branding.print_hooks.get_pdf_body_html_with_branding",
]

