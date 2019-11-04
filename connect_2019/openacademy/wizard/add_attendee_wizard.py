# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AddAttendeeWizard(models.TransientModel):
    _name = 'add.attendee.wizard'
    _description = 'Add Attendees Wizard'

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session', string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}