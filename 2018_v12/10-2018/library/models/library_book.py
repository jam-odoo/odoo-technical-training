# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields

class Book(models.Model):
    '''
    Library Books Model
    '''

    _name = 'library.book'
    _description= 'Library Books'
    _order = 'sequence, name, purchase_date desc, id'

    sequence = fields.Integer(string="Sequence", default=10)
    isbn = fields.Char(string='ISBN', size=64)
    name = fields.Char(string='Title', required=True, translate=True, index=True)
    book_index = fields.Html(string='Index')
    cover = fields.Selection(selection=[
                                ('NC', 'No Cover'),
                                ('HC', 'Hard Cover'),
                                ('SC', 'Soft Cover'),
                            ], string='Type', required=True, default='NC') 
    last_rent_date = fields.Datetime(string='Last Rented Date')
    purchase_date = fields.Date(string='Purchase Date')
    purchase_price = fields.Float(string='Purchase Price', digits=(5, 5), required=True)
    active = fields.Boolean(string='Archived ?', default=True)
    book_cover = fields.Binary(string='Book Cover')
    book_cover_name = fields.Char(string='Book Cover Name')
