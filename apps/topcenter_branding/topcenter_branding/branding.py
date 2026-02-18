from __future__ import unicode_literals

import frappe


def get_settings():
    """Renvoie le doc Tenant Branding Settings principal (s'il existe)."""
    if not frappe.db.exists("DocType", "Tenant Branding Settings"):
        return None
    name = frappe.db.get_value("Tenant Branding Settings", {}, "name")
    if not name:
        return None
    return frappe.get_doc("Tenant Branding Settings", name)


def apply_branding_for_current_site():
    """Hook after_migrate – idempotent."""
    try:
        settings = get_settings()
        if not settings:
            frappe.logger("topcenter_branding").info(
                "Aucun Tenant Branding Settings trouvé, skip."
            )
            return
        settings.apply()
    except Exception:
        frappe.log_error(
            title="topcenter_branding.apply_branding_for_current_site",
            message=frappe.get_traceback(),
        )


def apply_branding(site: str):
    """API manuelle appelée avec un site explicite."""
    frappe.init(site=site)
    frappe.connect()
    try:
        apply_branding_for_current_site()
    finally:
        frappe.destroy()

