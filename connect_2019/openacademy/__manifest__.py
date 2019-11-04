# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",

    'summary': """
        Course management""",

    'description': """
        Open Academy allow you to manager you course, session, teacher and attendee. 
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'website', 'website_sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/openacademe_menu_views.xml',
        'views/openacademe_course_views.xml',
        'views/openacademy_session_views.xml',
        'views/partner_views.xml',

        'wizard/add_attendee_wizard_view.xml',

        'data/partner_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/course.xml',
    ],
}