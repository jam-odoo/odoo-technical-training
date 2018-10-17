# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class BookTags(models.Model):
    '''
    Library Books Model
    '''

    _name = 'library.book.tags'

    name = fields.Char(string='Tag Name', required=True, translate=True, index=True)
    color_index = fields.Integer(string='Color Index')


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
    tag_ids = fields.Many2many(comodel_name='library.book.tags')
    author_ids = fields.Many2many(comodel_name='res.partner',
                                    relation='rel_book_auhtor_parnter',
                                    column1='book_id',
                                    column2='partner_id',
                                    string='Auhtors')
    rental_ids = fields.One2many(comodel_name='library.rent', inverse_name='book_id', string='Rentals')
