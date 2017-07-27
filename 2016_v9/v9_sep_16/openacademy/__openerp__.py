# -*- coding: utf-8 -*-
{
    "name": "Open Academy",
    "version": "1.0",
    "summary": "Session, Course Mangment",
    "sequence": "1",
    "author": "Odoo, Inc",
    "website": "https://www.odoo.com",
    "description": """
Open Academy Managment
====================================
- Course Managment
- **Session Managment**

""",
    "depends": ["mail"],
    "category": "Tools",
    "data": [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "wizard/wizard_add_partner_views.xml",
        "views/openacademy_views.xml",
        "views/partner_views.xml",
        "views/openacademy_workflow.xml",
        "views/report_openacademy_session.xml",
        "views/openacademy_reports.xml",
    ],
    "demo": [
    ],
}