# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields

class Book(models.Model):
    '''
    Library Books Model
    '''

    _name = 'library.book'
    _description= 'Library Books'
    _order = 'name, purchase_date desc, id'

    name = fields.Char(string='Title', required=True, index=True)
    book_index = fields.Html(string='Index')
    cover = fields.Selection(selection=[
                                ('NC', 'No Cover'),
                                ('HC', 'Hard Cover'),
                                ('SC', 'Soft Cover'),
                                ], string='Cover Type', required=True, default='NC') 
    last_rent_date = fields.Datetime(string='Last Rented Date')
    purchase_date = fields.Date(string='Purchase Date')
    purchase_price = fields.Float(string='Purchase Price', digits=(5, 5), required=True)
    active = fields.Boolean(string='Archived ', default=True)
    book_cover = fields.Binary(string='Book Cover')
    book_cover_name = fields.Char(string='Book Cover Name')
