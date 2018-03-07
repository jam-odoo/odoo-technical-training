# -*- coding: utf-8 -*-

from odoo import models, fields



class EquipmentsTags(models.Model):

    _name = "equipment.tags"

    name =  fields.Char(string="Tag Name", required=True, 
            index=True)
    color = fields.Integer(string="Color Index")


class Equipments(models.Model):

    _name = "equipment.equipment"
    _description = "Equipments"
    _order = "sequence, id"

    name =  fields.Char(string="Equipment Name", required=True,
                        copy=False)
    sequence = fields.Integer(string="Sequence", default=10)
    purchase_date = fields.Date(string="Purchase Date", required=True)
    active = fields.Boolean(string="Archived", default=True)
    equipment_life = fields.Integer(string="Life in Months",
                    help="Equipments Life in  months")
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




class EquipmentsLogs(models.Model):

    _name = "equipment.logs"

    name =  fields.Char(string="Log title", required=True, 
            index=True)
    log_date = fields.Datetime(string="Log Date")
    notes = fields.Text(string="Notes")
    equipment_id = fields.Many2one(comodel_name="equipment.equipment", 
                        string="Equipment")