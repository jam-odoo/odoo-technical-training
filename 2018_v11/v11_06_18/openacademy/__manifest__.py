# -*- encoding: utf-8 -*-

{
    'name': 'OpenAcademy Planning',
    'summary': 'Course, Session Managment',
    'decription': '''
OpenAcademy Planning
=================================
- Session Mnagamnet
etc..
    ''',
    'depends': ['mail', 'sale_management', 'website'],
    'category': 'OpenAcademy',
    'website': 'https://www.odoo.com',
    'author': ' Odoo Inc',
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/openacdemy_menu.xml',
        'views/openacdemy_sessions_views.xml',
        'views/openacdemy_attendee_views.xml',
        'views/openacdemy_course_views.xml',
        'views/sale_view.xml',
        'report/openacademy_session_report.xml',
        'report/openacademy_report.xml',
        'views/templates.xml',

    ],
    'demo': [
        'demo/openacdemy_demo.xml',
    ],
}