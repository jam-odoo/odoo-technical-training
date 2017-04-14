# -*- coding: utf-8 -*-
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _



class WizardInvitations(models.TransientModel):
    """Invitation Wizard"""
    _name = "wizard.invitations"

    session_id = fields.Many2one(comodel_name="openacademy.session", string="Sesssion", required=True)
    invitation_lines_ids = fields.One2many(comodel_name="wizard.invitation.line", inverse_name="wizard_id", string="Invitations")

    @api.multi
    def create_invitation(self):
        InvitationModel = self.env["openacademy.invitation"]
        for wizard in self:
            for line in wizard.invitation_lines_ids:
                vals = {
                    "name": line.name,
                    "email": line.email,
                    "phone": line.phone,
                    "partner_id": line.partner_id.id if line.partner_id else False,
                    "count": line.count,
                    "session_id": wizard.session_id.id,
                }
                InvitationModel.create(vals)


class WizardInvitationLines(models.TransientModel):

    _name  = "wizard.invitation.line"
    _inherit = "openacademy.invitation"

    wizard_id = fields.Many2one(comodel_name="wizard.invitations", string="Wizard")