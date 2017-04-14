# -*- coding: utf-8 -*-
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _



class OpenAcademyCourse(models.Model):
    """OpenAcademy Course Managment"""

    _name = "openacademy.course"

    name = fields.Char(string="Course Name", required=True, help="Course name goes here... e.g. Odoo Trainings")
    course_contain = fields.Html(string="Course Contain")
    active = fields.Boolean(string="Active", default=True)
    code = fields.Char(string="Code", size=32)
    user_id = fields.Many2one(comodel_name="res.users", string="Responsible",ondelete="set null", required=True, copy=False, index=True)
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sesssions")

    @api.model
    def create(self, vals):
        if not vals["code"]:
            vals.update({"code": vals["name"].upper()})
        res = super(OpenAcademyCourse, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        for record in self:        
            if "code" in vals.keys() and not vals["code"]:
                vals.update({"code": vals["name"].upper() if "name" in vals.keys() else record.name.upper()})
        res = super(OpenAcademyCourse, self).write(vals)
        return res

    @api.multi
    def unlink(self):
        self.write({"active": False})
        # raise exceptions.ValidationError("Please archive the record. This record can not be deleted")
        return False

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, "%s ( %s )"%(record.name, record.code)))
        return res

class Parnter(models.Model):

    _inherit = "res.partner"

    instructor = fields.Boolean(string="Insructor")
    website = fields.Char(string="Homepage")
    country_id =  fields.Many2one(index=True)
    course_ids = fields.Many2many(comodel_name="openacademy.course", string="Course")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection=[
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('verify', "Verify"),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ])

    @api.multi
    def action_confirm(self):
        # for order in self:
        #     if order.state != "verify":
        #         raise exceptions.ValidationError("Snap ! Something went wrong.")
        res = super(SaleOrder, self).action_confirm()
        return res