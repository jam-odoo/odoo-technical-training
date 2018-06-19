# -*- encoding: utf-8 -*-

from odoo import models, fields

class OpenAcademyCouse(models.Model):

    _name = 'openacademy.course'

    name = fields.Char(string='Title', required=True, index=True,
                        help='Couse title goes here (e.g. Odoo Technical Training)')
    active = fields.Boolean(string="Active", default=True)
    session_count = fields.Integer("# Sessoin")
    notes = fields.Html(string="Notes")
    banner = fields.Binary(string='Banner')
    banner_fname = fields.Char(string="Banner File Name")