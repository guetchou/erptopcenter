from __future__ import unicode_literals

app_name = "topcenter_core"
app_title = "TopCenter Core"
app_publisher = "Top Center"
app_description = "Noyau fonctionnel et customisations ERPNext/HRMS pour Top Center"
app_email = "contact@topcenter.cg"
app_license = "MIT"

# Fixtures : uniquement les éléments explicitement listés
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["name", "in", [
            # Exemple : champs Leave Application / Employee / Salary Slip
            "Leave Application-tc_leave_reason",
            "Leave Application-tc_qr_code_printed",
            "Employee-tc_internal_id",
        ]]],
    },
    {
        "dt": "Property Setter",
        "filters": [["name", "in", [
            "Leave Application-from_date-reqd",
            "Leave Application-to_date-reqd",
        ]]],
    },
    {
        "dt": "Client Script",
        "filters": [["name", "in", [
            "Leave Application-Client",
            "Salary Slip-Validate Net Pay",
        ]]],
    },
    {
        "dt": "Server Script",
        "filters": [["name", "in", [
            "Leave Application-Auto Set Posting Date",
        ]]],
    },
    {
        "dt": "Print Format",
        "filters": [["name", "in", [
            "Demande Congé - TopCenter",
            "Salaire-TopCenter",
        ]]],
    },
    {
        "dt": "Workflow",
        "filters": [["name", "in", [
            "Leave Application Workflow - TopCenter",
        ]]],
    },
    {
        "dt": "Role",
        "filters": [["name", "in", [
            "HR Manager Congo",
            "Finance Manager Congo",
        ]]],
    },
    {
        "dt": "Role Profile",
        "filters": [["name", "in", [
            "TopCenter HR",
            "TopCenter Finance",
        ]]],
    },
]

# Patches de données / paramétrage (idempotents)
after_migrate = [
    "topcenter_core.patches.v1_0.setup_leave_congo.apply",
    "topcenter_core.patches.v1_0.setup_payroll_congo.apply",
]

