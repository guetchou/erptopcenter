from __future__ import unicode_literals

import frappe


def log(msg: str) -> None:
    frappe.logger("topcenter_core.patches").info(msg)


def ensure_workflow():
    name = "Leave Application Workflow - TopCenter"
    if frappe.db.exists("Workflow", name):
        log(f"Workflow '{name}' déjà présent, skip.")
        return

    log(f"Création du Workflow '{name}'...")
    wf = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": name,
        "document_type": "Leave Application",
        "is_active": 1,
        "send_email_alert": 1,
        "workflow_state_field": "workflow_state",
        "states": [
            {
                "state": "Draft",
                "doc_status": 0,
                "allow_edit": "Employee",
            },
            {
                "state": "Pending Approval",
                "doc_status": 0,
                "allow_edit": "Leave Approver",
            },
            {
                "state": "Approved",
                "doc_status": 1,
                "allow_edit": "Leave Approver",
            },
            {
                "state": "Rejected",
                "doc_status": 1,
                "allow_edit": "Leave Approver",
            },
        ],
        "transitions": [
            {
                "state": "Draft",
                "action": "Submit for Approval",
                "next_state": "Pending Approval",
                "allowed": "Employee",
            },
            {
                "state": "Pending Approval",
                "action": "Approve",
                "next_state": "Approved",
                "allowed": "Leave Approver",
            },
            {
                "state": "Pending Approval",
                "action": "Reject",
                "next_state": "Rejected",
                "allowed": "Leave Approver",
            },
        ],
    })
    wf.insert(ignore_permissions=True)
    log(f"Workflow '{name}' créé.")


def ensure_leave_type():
    name = "Congé payé - Congo"
    if frappe.db.exists("Leave Type", name):
        log(f"Leave Type '{name}' déjà présent, skip.")
        return

    log(f"Création du Leave Type '{name}'...")
    lt = frappe.get_doc({
        "doctype": "Leave Type",
        "leave_type_name": name,
        "max_days_allowed": 30,
        "include_holiday": 0,
        "is_lwp": 0,
        "is_carry_forward": 1,
    })
    lt.insert(ignore_permissions=True)
    log(f"Leave Type '{name}' créé.")


def apply():
    """Patch idempotent : configuration congés pour Congo."""
    log("Patch v1_0.setup_leave_congo: START")
    ensure_workflow()
    ensure_leave_type()
    log("Patch v1_0.setup_leave_congo: DONE")

