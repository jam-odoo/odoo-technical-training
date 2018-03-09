# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, exceptions
from odoo import _

class EquipmentsTags(models.Model):

    _name = "equipment.tags"

    name =  fields.Char(string="Tag Name", required=True, 
            index=True)
    color = fields.Integer(string="Color Index")


class Equipments(models.Model):

    _name = "equipment.equipment"
    _description = "Equipments"
    _order = "sequence, id"
    _inherit = ["mail.thread",'mail.activity.mixin']

    def _get_default_curr(self):
        return self.env.user.company_id.currency_id


    name =  fields.Char(string="Equipment Name", required=True,
                        copy=False, translate=True, track_visibility="always")
    sequence = fields.Integer(string="Sequence", default=10)
    purchase_date = fields.Date(string="Purchase Date", required=True, default=fields.Date.today())
    day_work_start = fields.Datetime(string="Daily Work Start", required=True, default=fields.Datetime.now())
    day_work_end = fields.Datetime(string="Daily Work End", required=True, default=fields.Datetime.now())
    active = fields.Boolean(string="Archived", default=True,  track_visibility="onchange")
    equipment_life = fields.Integer(string="Life in Months",
                    help="Equipments Life in  months")
    code = fields.Char(string="Code")
    state = fields.Selection(selection=[
                                ("New", "New"),
                                ("InUse", "In Use"),
                                ("InService", "IN Service"),
                                ("Recycled", "Recycled"),
                                ("Out", "Out Of Service"),
                            ], string="Status", required=True, default="New")
    value = fields.Float(string="Value", digits=(5,3))
    mytime = fields.Float(string="My Time")
    notes = fields.Html(string="Notes")
    image = fields.Binary(string="Image")
    user_id = fields.Many2one(comodel_name="res.users", string="Maintainer")
    sale_id = fields.Many2one(comodel_name="sale.order", string="Reference Oder")
    tag_ids = fields.Many2many(comodel_name="equipment.tags", 
                                        relation="rel_equipment_tag_m2m",
                                        column1="equipment_id",
                                        column2="tag_id", string="Tags")
    log_ids = fields.One2many(comodel_name="equipment.logs", 
                                inverse_name="equipment_id", string="Logs")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", default=_get_default_curr)
    dep = fields.Monetary(compute="_calc_dep", string="Monthly Depreciation")
    sumvalue = fields.Monetary(compute="_calc_sumvalue", store=True, string="Sim value")
    log_count = fields.Integer(compute="_log_count", string="#Nbr Logs")


    _sql_constraints = [
        ("unique_equip_code", "UNIQUE (code)", "Code must be unique !")
    ]

    @api.multi
    @api.depends("log_ids")
    def _log_count(self):
        for record in self:
            record.log_count = len(record.log_ids.ids)


    @api.multi
    @api.depends("value", "equipment_life")
    def _calc_sumvalue(self):
        for record in self:
            record.sumvalue = record.value * record.equipment_life

    @api.multi
    @api.depends("value", "equipment_life")
    def _calc_dep(self):
        for record in self:
            record.dep = record.value / record.equipment_life if record.equipment_life != 0.0 else 0.0

    def get_me(self):
        return "This is Me"

    @api.multi
    @api.constrains("equipment_life", "value")
    def _validate_equipment_life(self):
        if self.filtered(lambda l: l.equipment_life < 0.0 or l.value < 0.0):
            raise exceptions.ValidationError(_("Equipments life or value can not be negative value."))
        # for record in self:
        #     if  record.equipment_life < 0.0:
        #        raise exceptions.ValidationError("Equipments life can not be negative value ({}).".format(record.equipment_life))
    @api.model
    def create(self, vals):
        vals.update({
            "code": self.env["ir.sequence"].next_by_code("equipment.equipment")
        })
        # if vals["equipment_life"] < 0.0:
        #     raise exceptions.ValidationError("Equipments life can not be negative value ({}).".format(vals.get("equipment_life")))
        res = super(Equipments, self).create(vals)
        return res

    # @api.model
    # def write(self, vals):
    #     if vals.get("equipment_life") < 0.0:
    #         raise exceptions.ValidationError("Equipments life can not be negative value ({}).".format(vals.get("equipment_life")))
    #     res = super(Equipments, self).write(vals)
    #     return res

    @api.multi
    def unlink(self):
        if self.filtered(lambda l: l.state != "New"):
            raise exceptions.ValidationError(_("Record not in New state can not be deleted please archive it."))
        return super(Equipments, self).unlink()

    @api.onchange("equipment_life", "value")
    def onchange_field(self):
        if self.equipment_life > 120:
            raise exceptions.ValidationError("Equipments life can not be more then 120 months")

    @api.multi
    def action_out(self):
        for record in self.filtered(lambda l : l.state != "Out"):
            record.state = 'Out'
        return True

class EquipmentsLogs(models.Model):

    _name = "equipment.logs"

    name =  fields.Char(string="Log title", required=True, 
            index=True)
    log_date = fields.Datetime(string="Log Date")
    notes = fields.Text(string="Notes")
    equipment_id = fields.Many2one(comodel_name="equipment.equipment", 
                        string="Equipment")