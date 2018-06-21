# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('validate', 'Validate'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ])

    @api.multi
    def action_approve(self):
        for sale in self:
            sale.state = 'validate'