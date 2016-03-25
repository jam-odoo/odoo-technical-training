# -*- coding: utf-8 -*-
{
    "name": " OpenAcademy",
    "summary": "OpenAcademy Course managment",
    "description": """
OpenAcacdemy Course managment
================================================
- Open Academy Courses
- Open Academy Session
""",
    "category": "OpenAcademy",
    "version": "0.1",
    "author": "Odoo, Inc",
    "website": "https://www.odoo.com",
    "depends": ["base", "mail"],
    "data": [
        "wizard/wizard_invite_partner_views.xml",
        "views/openaademy_views.xml",
        "views/openacademy_workflow.xml",
        "report/report_sessions.xml",
        "views/openaademy_reports.xml",

    ],
    "demo": [], 
}