#!/usr/bin/env python3
"""
Export des customisations ERPNext/Frappe vers artifacts (JSON + rapport Markdown).

Contexte d'ex?cution:
- H?te: copier ce script dans le conteneur backend
- Conteneur: bench --site <site> console
- Console: exec(open('/tmp/export_customizations.py').read()); run()
"""

from __future__ import annotations

import json
import os
from typing import Any

import frappe


ARTIFACTS_DIR = "/home/frappe/frappe-bench/artifacts"

DOCTYPES = [
    "Custom Field",
    "Property Setter",
    "Client Script",
    "Server Script",
    "Workflow",
    "Workflow State",
    "Print Format",
    "Letter Head",
    "Role",
    "Role Profile",
]


def _group_key(dt: str, rec: dict[str, Any]) -> str:
    if dt == "Custom Field":
        return rec.get("dt") or "Custom Field"
    if dt == "Property Setter":
        return rec.get("doc_type") or "Property Setter"
    if dt == "Client Script":
        return rec.get("dt") or rec.get("reference_doctype") or "Client Script"
    if dt == "Server Script":
        return rec.get("reference_doctype") or "Server Script"
    if dt == "Workflow":
        return rec.get("document_type") or "Workflow"
    if dt == "Print Format":
        return rec.get("doc_type") or "Print Format"
    if dt in ("Role", "Role Profile", "Letter Head", "Workflow State"):
        return dt
    return "Other"


def _safe_json(v: Any) -> Any:
    try:
        json.dumps(v)
        return v
    except TypeError:
        return str(v)


def run() -> None:
    now = frappe.utils.now()
    ts = now.replace("-", "").replace(" ", "_").replace(":", "").split(".")[0]

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    json_path = os.path.join(ARTIFACTS_DIR, f"customizations_{ts}.json")
    md_path = os.path.join(ARTIFACTS_DIR, f"customizations_report_{ts}.md")

    items: list[dict[str, Any]] = []
    totals: dict[str, int] = {}
    grouped: dict[str, dict[str, int]] = {}

    for dt in DOCTYPES:
        rows = frappe.get_all(dt, fields=["*"])
        totals[dt] = len(rows)
        for r in rows:
            rec = {k: _safe_json(v) for k, v in dict(r).items()}
            rec["doctype"] = dt
            items.append(rec)

            gk = _group_key(dt, rec)
            bucket = grouped.setdefault(gk, {})
            bucket[dt] = bucket.get(dt, 0) + 1

    payload = {
        "generated_at": now,
        "site": frappe.local.site if getattr(frappe.local, "site", None) else None,
        "totals": totals,
        "items": items,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    top50 = sorted(items, key=lambda x: x.get("modified") or "", reverse=True)[:50]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Customizations Report\n\n")
        f.write(f"Generated at: {now}\n\n")
        f.write(f"Site: `{payload['site']}`\n\n")

        f.write("## Totals\n\n")
        f.write("| Type | Count |\n")
        f.write("|---|---:|\n")
        for dt in sorted(totals):
            f.write(f"| {dt} | {totals[dt]} |\n")

        f.write("\n## Top 50 modified\n\n")
        f.write("| # | Type | Name | Modified | Group |\n")
        f.write("|---:|---|---|---|---|\n")
        for i, rec in enumerate(top50, 1):
            dt = rec.get("doctype", "")
            f.write(
                f"| {i} | {dt} | {rec.get('name', '')} | {rec.get('modified', '')} | {_group_key(dt, rec)} |\n"
            )

        f.write("\n## Grouped by functional DocType\n\n")
        f.write("| Group | Custom Field | Property Setter | Client Script | Server Script | Workflow | Print Format | Other |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for gk in sorted(grouped):
            b = grouped[gk]
            cf = b.get("Custom Field", 0)
            ps = b.get("Property Setter", 0)
            cs = b.get("Client Script", 0)
            ss = b.get("Server Script", 0)
            wf = b.get("Workflow", 0)
            pf = b.get("Print Format", 0)
            other = sum(v for k, v in b.items() if k not in {"Custom Field", "Property Setter", "Client Script", "Server Script", "Workflow", "Print Format"})
            f.write(f"| {gk} | {cf} | {ps} | {cs} | {ss} | {wf} | {pf} | {other} |\n")

    print(f"OK JSON: {json_path}")
    print(f"OK REPORT: {md_path}")


if __name__ == "__main__":
    run()
