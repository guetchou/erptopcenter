# Copyright (c) 2025, Top Center and contributors
# Injecte le branding (Tenant Branding Settings) dans le contexte du rendu Print Format
# pour que tous les Print Formats puissent utiliser {{ branding.logo }}, {{ branding.primary_color }}, etc.

from __future__ import unicode_literals

import frappe

from topcenter_branding.branding import get_settings


def get_branding_context():
    """
    Construit le dict de branding pour le contexte Jinja des Print Formats.
    Utilisable dans les templates : {{ branding.logo_url }}, {{ branding.primary_color }}, etc.
    """
    settings = get_settings()
    if not settings:
        return _empty_branding()

    logo_url = ""
    if settings.logo:
        try:
            # Chemin relatif type "files/xxx" -> URL utilisable en print/PDF
            logo_url = frappe.utils.get_url(settings.logo)
        except Exception:
            logo_url = "/" + settings.logo if not settings.logo.startswith("/") else settings.logo

    return {
        "company": settings.company or "",
        "logo": settings.logo or "",
        "logo_url": logo_url,
        "primary_color": settings.primary_color or "",
        "secondary_color": settings.secondary_color or "",
        "footer_text": settings.footer_text or "",
        "letter_head_template": settings.letter_head_template or "",
        "print_signature": settings.print_signature or "",
    }


def _empty_branding():
    return {
        "company": "",
        "logo": "",
        "logo_url": "",
        "primary_color": "",
        "secondary_color": "",
        "footer_text": "",
        "letter_head_template": "",
        "print_signature": "",
    }


def get_pdf_body_html_with_branding(jenv=None, template=None, print_format=None, args=None):
    """
    Hook pdf_body_html : injecte `branding` dans args pour le rendu Print Format / PDF.
    Les templates Jinja peuvent utiliser :
      {{ branding.logo_url }}, {{ branding.primary_color }}, {{ branding.secondary_color }},
      {{ branding.footer_text }}, {{ branding.print_signature }}, {{ branding.company }}.
    Puis délègue au hook suivant (ex. congo_hrms pour QR).
    """
    args = args or {}
    try:
        args["branding"] = get_branding_context()
    except Exception:
        frappe.log_error(
            title="topcenter_branding.get_pdf_body_html_with_branding",
            message=frappe.get_traceback(),
        )
        args["branding"] = _empty_branding()

    hooks = frappe.get_hooks("pdf_body_html") or []
    our_ref = "topcenter_branding.print_hooks.get_pdf_body_html_with_branding"
    try:
        idx = next(i for i, h in enumerate(hooks) if our_ref in str(h))
    except StopIteration:
        idx = -1
    next_hooks = hooks[idx + 1:] if idx >= 0 else []
    if not next_hooks:
        return template.render(**args) if template else ""
    return frappe.get_attr(next_hooks[0])(
        jenv=jenv, template=template, print_format=print_format, args=args
    )
