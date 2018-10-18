# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Library Managment',
    'version': '0.1', 
    'website': 'https://www.odoo.com',
    'summary': 'Library, Books, Custoemr Managment',
    'sequence': 2,
    'category': 'Library',
    'author': 'Odoo Inc',
    'description': '''Library, Books, Custoemr Managment''',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'views/library_menu_view.xml',
        'views/library_rental_views.xml',
        'views/library_book_views.xml',
        'wizard/open_books_action_views.xml',
        'views/res_partner_view.xml',
        'data/mail_data.xml',
        'reports/book_report_template.xml',
        'reports/library_book_report.xml',
    ],
    'demo': [
        'demo/library_demo.xml',
        'demo/library_rental_demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'installable': True,
}