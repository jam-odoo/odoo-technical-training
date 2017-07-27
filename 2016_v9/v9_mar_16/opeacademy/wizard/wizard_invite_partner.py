# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class WizardInvitepartner(models.TransientModel):
    """Invite Partner Attendee"""
    _name = "wizard.invite.partner"

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partners")

    @api.one
    def invite_partners(self):
        session_id = self.env.context.get("active_id", False)
        SessionModel = self.env['openacademy.sessions']
        AttendeeModel = self.env["openacademy.attendee"]
        if session_id:
            session = SessionModel.sudo().browse(session_id)
            # # print "================", session_id,session
            # invites = []
            for partner in self.partner_ids:
                vals = {
                    'partner_id': partner.id,
                    'email': partner.email,
                    'count': 1,
                    'state': 'invite',
                    'session_id': session_id
                }
                AttendeeModel.sudo().create(vals)
            body = "<p>Partners Invited : </p><ul>" + "".join(["<li>"+p.name+"</li>" for p in self.partner_ids]) + "</ul>"
            session.message_post(body=body)
            #     invites.append(AttendeeModel.create(vals))
            # session.attendee_ids = [ i.id for i in invites]
        #for partner in self.partner_ids: