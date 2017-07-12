# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'OpenAcademy',
    'version' : '0.1',
    'summary': 'Course, sessnions',
    'sequence': 1,
    'description': """
OpenAcademy Managment
===================================
- Sesssion 
- Courses
- Atteafdance
""",
    'category': 'Custom Addons',
    'author': 'Odoo, Inc',
    'website': 'https://www.odoo.com',
    'images' : [
    ],
    'depends' : ['base'],
    'data': [
        "views/openacademy_sessions_views.xml",
    ],
    'demo': [
        "demo/openacademy_session_demo.xml",
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
 }