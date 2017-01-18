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
    "depends": ["base"],
    "category": "Custom Addons",
    "data": [
        "views/openacademy_views.xml",
    ],
    "demo": [
        "demo/openacademy_session_demo.xml",
    ],
    "application": True,
    "sequence": 0,
    "installable": True,
    "auto_intall": False
}