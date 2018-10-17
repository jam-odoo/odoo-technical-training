# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, _ , exceptions



class Rental(models.Model):
    '''
    Library Books Model
    '''

    _name = 'library.rent'
    _description= 'Library Books Rentals'
    _order = 'sequence, start_date desc, id'
    _rec_name = 'book_id'

    def _get_end_date(self):
        return fields.Datetime.now() + relativedelta(days=14)

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
    rental_days = fields.Integer(string="Number of Days", compute="compute_rental_days", store=True)


    @api.onchange('start_date')
    def onchange_start_date(self):
        self.ensure_one()
        if self.start_date:
            self.end_date = self.start_date  + relativedelta(days=14)

    @api.multi
    @api.depends('start_date', 'end_date')
    def compute_rental_days(self):
        for rent in self:
            if rent.start_date and rent.end_date:
                rent.rental_days = (rent.end_date - rent.start_date).days

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         print (vals)
    #         if vals.get('start_date') and vals.get('end_date'):
    #             start_date = datetime.strptime(vals.get('start_date'), "%Y-%m-%d %H:%M:%S")
    #             end_date = datetime.strptime(vals.get('end_date'), "%Y-%m-%d %H:%M:%S")
    #             if vals.get('start_date') >= vals.get('end_date'):
    #                 raise exceptions.ValidationError(_("Start date can not be after end date."))
    #     result = super(Rental, self).create(vals_list)
    #     print (result)
    #     return result

    @api.constrains('start_date', 'end_date')
    def _validate_dates(self):
        self.ensure_one()
        # import pdb
        # pdb.set_trace()
        if self.start_date and self.end_date\
            and self.start_date >= self.end_date:
            raise exceptions.ValidationError(_("Start date can not be after end date."))