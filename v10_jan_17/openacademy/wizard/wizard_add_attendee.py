# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddAttendee(models.TransientModel):

    _name = "wizard.add.attendee"

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partners")

    @api.multi
    def add_partners(self):
        session_id = self.env.context.get("active_id")
        AttendeeModel = self.env["openacademy.attendee"]
        for record in self:
            for partner in record.partner_ids:
                vals ={
                    "session_id": session_id,
                    "partner_id": partner.id,
                    "count": 1,
                    "full_name": partner.name,
                    "email": partner.email,
                }
                AttendeeModel.create(vals)
