##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-Today Odoo Inc (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "OpenAcademy",
    'version': '0.1',
    'author': 'Odoo Inc',
    'website': 'https://www.odoo.com',
    'category': 'Course Management',
    'depends': ['mail'],
    'summary': 'Session, Course, Attendee',
    'description': """
Course and Session Management

---

 - Course Management
 - Session Management
 - Attendee Management
""",
    'data': [
        'security/openacademy_security.xml',
        'security/ir.model.access.csv',
        'wizard/wiz_add_attendee_view.xml',
        'openacademy_view.xml',
        'openacademy_workflow.xml',
        'views/report_openacademy.xml',
        'openacademy_report.xml',
    ],
    'demo':[
        'openacademy_demo.xml',
    ],
}






