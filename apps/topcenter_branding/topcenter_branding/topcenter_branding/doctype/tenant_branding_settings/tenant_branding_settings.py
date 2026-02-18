from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class TenantBrandingSettings(Document):
    def apply(self):
        """Applique le branding actuel au site (idempotent)."""
        if not self.company:
            return

        # 1) Logo Company
        company = frappe.get_doc("Company", self.company)
        changed = False
        if self.logo and company.logo != self.logo:
            company.logo = self.logo
            changed = True
        if changed:
            company.flags.ignore_permissions = True
            company.save()
            frappe.logger("topcenter_branding").info(
                f"Company '{self.company}' mis à jour (logo)."
            )

        # 2) Letter Head
        lh_name = f"{self.company} - Default Letter Head"
        if frappe.db.exists("Letter Head", lh_name):
            lh = frappe.get_doc("Letter Head", lh_name)
        else:
            lh = frappe.get_doc({
                "doctype": "Letter Head",
                "letter_head_name": lh_name,
                "is_default": 1,
                "disabled": 0,
            })
        if self.letter_head_template:
            lh.content = self.letter_head_template
        lh.flags.ignore_permissions = True
        lh.save()
        frappe.logger("topcenter_branding").info(
            f"Letter Head '{lh_name}' appliqué pour '{self.company}'."
        )

