from __future__ import unicode_literals

import frappe


def log(msg: str) -> None:
    frappe.logger("topcenter_core.patches").info(msg)


def ensure_salary_component(code: str, label: str, type_: str):
    if frappe.db.exists("Salary Component", code):
        log(f"Salary Component '{code}' déjà présent, skip.")
        return

    log(f"Création du Salary Component '{code}' ({type_})...")
    sc = frappe.get_doc({
        "doctype": "Salary Component",
        "salary_component": code,
        "description": label,
        "type": type_,
        "abbr": code[:8],
    })
    sc.insert(ignore_permissions=True)
    log(f"Salary Component '{code}' créé.")


def ensure_payroll_settings():
    ps = frappe.get_single("Payroll Settings")
    changed = False

    if ps.salary_slip_based_on_timesheet:
        ps.salary_slip_based_on_timesheet = 0
        changed = True

    if ps.round_to_the_nearest_integer != 1:
        ps.round_to_the_nearest_integer = 1
        changed = True

    if changed:
        ps.flags.ignore_permissions = True
        ps.save()
        frappe.db.commit()
        log("Payroll Settings mis à jour (round_to_the_nearest_integer=1, no timesheet).")
    else:
        log("Payroll Settings déjà configurés, skip.")


def apply():
    """Patch idempotent : configuration paie Congo."""
    log("Patch v1_0.setup_payroll_congo: START")
    ensure_salary_component("BASE", "Salaire de base", "Earning")
    ensure_salary_component("CNSS_EMP", "CNSS Employé", "Deduction")
    ensure_salary_component("CNSS_EMPLOYER", "CNSS Employeur", "Earning")
    ensure_payroll_settings()
    log("Patch v1_0.setup_payroll_congo: DONE")

