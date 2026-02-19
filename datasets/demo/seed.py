from __future__ import annotations

import frappe


def run():
    """Jeu de donn?es d?mo idempotent.

    Ex?cution (conteneur backend):
      bench --site <site> execute datasets.demo.seed.run
    """

    company = frappe.db.get_value("Company", {}, "name")
    if not company:
        frappe.logger("datasets.demo").warning("Aucune Company trouv?e, seed ignor?.")
        return

    # Employee de d?monstration (cr?ation idempotente)
    employee_name = "Demo Employee"
    if frappe.db.exists("Employee", {"employee_name": employee_name}):
        return

    doc = frappe.get_doc(
        {
            "doctype": "Employee",
            "first_name": "Demo",
            "last_name": "Employee",
            "employee_name": employee_name,
            "company": company,
            "status": "Active",
            "gender": "Other",
            "date_of_birth": "1990-01-01",
            "date_of_joining": frappe.utils.today(),
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
