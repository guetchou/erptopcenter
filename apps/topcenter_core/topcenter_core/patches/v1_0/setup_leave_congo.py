from __future__ import unicode_literals

import frappe


def log(msg: str) -> None:
    frappe.logger("topcenter_core.patches").info(msg)


def ensure_workflow():
    # HRMS non install?: skip s?r
    if not frappe.db.exists("DocType", "Leave Application"):
        log("DocType Leave Application absent (HRMS non install?), skip workflow.")
        return

    name = "Leave Application Workflow - TopCenter"
    if frappe.db.exists("Workflow", name):
        log(f"Workflow '{name}' d?j? pr?sent, skip.")
        return

    if not frappe.db.exists("Role", "Leave Approver"):
        log("Role 'Leave Approver' absent, skip workflow.")
        return
    if not frappe.db.exists("Role", "Employee"):
        log("Role 'Employee' absent, skip workflow.")
        return

    log(f"Cr?ation du Workflow '{name}'...")
    wf = frappe.get_doc(
        {
            "doctype": "Workflow",
            "workflow_name": name,
            "document_type": "Leave Application",
            "is_active": 1,
            "send_email_alert": 1,
            "workflow_state_field": "workflow_state",
            "states": [
                {"state": "Draft", "doc_status": 0, "allow_edit": "Employee"},
                {
                    "state": "Pending Approval",
                    "doc_status": 0,
                    "allow_edit": "Leave Approver",
                },
                {"state": "Approved", "doc_status": 1, "allow_edit": "Leave Approver"},
                {"state": "Rejected", "doc_status": 1, "allow_edit": "Leave Approver"},
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
        }
    )
    wf.insert(ignore_permissions=True)
    log(f"Workflow '{name}' cr??.")


def ensure_leave_type():
    # HRMS non install?: skip s?r
    if not frappe.db.exists("DocType", "Leave Type"):
        log("DocType Leave Type absent (HRMS non install?), skip leave type.")
        return

    name = "Cong? pay? - Congo"
    if frappe.db.exists("Leave Type", name):
        log(f"Leave Type '{name}' d?j? pr?sent, skip.")
        return

    log(f"Cr?ation du Leave Type '{name}'...")
    lt = frappe.get_doc(
        {
            "doctype": "Leave Type",
            "leave_type_name": name,
            "max_days_allowed": 30,
            "include_holiday": 0,
            "is_lwp": 0,
            "is_carry_forward": 1,
        }
    )
    lt.insert(ignore_permissions=True)
    log(f"Leave Type '{name}' cr??.")


def apply():
    """Patch idempotent : configuration cong?s pour Congo."""
    log("Patch v1_0.setup_leave_congo: START")
    ensure_workflow()
    ensure_leave_type()
    log("Patch v1_0.setup_leave_congo: DONE")
