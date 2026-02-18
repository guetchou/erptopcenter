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

