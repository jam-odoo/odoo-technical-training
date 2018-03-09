# -*- coding: utf-8 -*-
{
    'name': "Equipments Managements",
    'summary': "Equipments Management",
    'description': """
Equipments Management
========================================
    """,
    'author': "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Equipments',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['sale_management', 'base'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/equipments_views.xml',
        'views/sale_view.xml',
        'data/sequence_data.xml',
        'reports/report_equipments.xml',
        'reports/equipments_reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/equipments_demo.xml',
    ],
}