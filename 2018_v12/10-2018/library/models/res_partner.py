# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, _ , exceptions



class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_author = fields.Boolean(string='Is Author ?')
    author_code = fields.Char(string='Author Ref', size=32)
    website = fields.Char(string="URL", index=True)