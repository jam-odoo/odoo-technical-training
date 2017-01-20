# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api

class partner(models.Model):

    _inherit = "res.partner"

    instructor = fields.Boolean(string="Instructor")
    website = fields.Char(string="Homepage")

class SaleOrder(models.Model):
    _inherit= "sale.order"
    
    invoice_status = fields.Selection(selection_add=[('sale_one', "Sale Done")]) 
    payment_term_id = fields.Many2one(required=True)