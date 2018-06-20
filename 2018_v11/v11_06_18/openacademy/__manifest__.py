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
    'depends': ['base'],
    'category': 'OpenAcademy',
    'website': 'https://www.odoo.com',
    'author': ' Odoo Inc',
    'license': 'LGPL-3',
    'data': [
        'views/openacdemy_menu.xml',
        'views/openacdemy_sessions_views.xml',
        'views/openacdemy_attendee_views.xml',
        'views/openacdemy_course_views.xml',
    ],
    'demo': [
        'demo/openacdemy_demo.xml',
    ],
}