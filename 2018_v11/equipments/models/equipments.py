# -*- coding: utf-8 -*-

from odoo import models, fields


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
    image = fields.Binary(string="Image")