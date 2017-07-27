# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api
from openerp import exceptions


class WizardAddPartner(models.TransientModel):

    _name = "wizard.add.partner"

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partners")
    count = fields.Integer(sting="{Invitee Count", default=1)

    @api.multi
    def add_partner(self):
        print "====================="
        SessionModel = self.env["openacademy.session"]
        AttendeeModel = self.env["openacademy.attendee"]
        session_id = self.env.context.get("active_id")
        for record in self:
            for partner in record.partner_ids:
                vals = {
                    "partner_id": partner.id,
                    "name": partner.name_get()[0][1], #get the full name of partner, partner.name can be used also.
                    "email": partner.email,
                    "count": record.count,
                    "session_id": session_id,
                }
                AttendeeModel.create(vals)