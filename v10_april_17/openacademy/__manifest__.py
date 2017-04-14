{    
    "name": "OpenAcademy Managment",
    "description": """
OpenAcademy Managment
===============================
* Sessions Managment
* Course Managment
* etc...
""",
    "summary": "Sessions,Courses",
    "license": "LGPL-3",
    "version": "1.0",
    "category": "Extra Addons",
    "sequence": 0,
    "website": "https://www.odoo.com",
    "author": "Odoo, Inc",
    "depends": ["sale", "mail"],
    "data": [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "workflow/openacademy_workflow.xml",
        "report/report_openacademy_session.xml",
        "report/openacademy_reports.xml",
        "views/openacademy_views.xml",
        "views/partner_view.xml",
        "views/templates.xml",
        "wizard/wizard_invitations_view.xml",
    ],
    "demo": [
        "demo/openacademy_session_demo.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}