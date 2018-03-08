# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, exceptions
from odoo import _

class Sale(models.Model):

    _inherit ="sale.order"

    po_number =  fields.Char(string="PO Number")
    state = fields.Selection(selection_add=[("validate", "Validation")])
    payment_term_id = fields.Many2one(string="Business Terms")
