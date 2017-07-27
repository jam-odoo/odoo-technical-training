# -*- coding: utf-8 -*-
{
    "name": "OpenAcademy Managment",
    "summary": "OpenAcademy Course, Sessions",
    "version": "1.0",
    "description": """
OpenAcademy Managment
======================================
- Course Managment
- Session Managment
- Attadance Managment
""",
    "author": "Odoo, Inc",
    "website": "https://www.odoo.com",
    "license": "AGPL-3",
    "depends": ['sale', 'mail', 'website'],
    "category": "Custom Addons",
    "data": [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "wizard/wizard_add_attendee_view.xml",
        "views/openacademy_views.xml",
        "views/partner_views.xml",
        "views/templates.xml",
        "views/openacademy_workflow.xml",
        "reports/report_openacademy_session.xml",
        "reports/openacademy_report.xml",
    ],
    "demo": [
        # "demo/openacademy_session_demo.xml",
    ],
    "application": True,
    "sequence": 0,
    "installable": True,
    "auto_intall": False
}