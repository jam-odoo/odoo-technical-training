# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _



class Rental(models.Model):
    '''
    Library Books Model
    '''

    _name = 'library.rent'
    _description= 'Library Books Rentals'
    _order = 'sequence, start_date desc, id'
    _rec_name = 'book_id'

    def _get_end_date(self):
        return fields.Datetime.now() + relativedelta(days=5)

    sequence = fields.Integer(string="Sequence", default=10)
    active = fields.Boolean(string='Is Active ?', default=True)
    book_id = fields.Many2one(comodel_name='library.book', string='Book', required=True, index=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    start_date = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(string='End Date', required=True, default=_get_end_date)
    state = fields.Selection(selection=[
                                ('draft', 'Drafted'),
                                ('confirm', 'Confirmed'),
                                ('rent', 'Rented'),
                                ('exrent', 'Extened Rental'),
                                ('return', 'Returned'),
                                ('cancel', 'Cancelled')
                            ], string='State', required=True, default='draft')