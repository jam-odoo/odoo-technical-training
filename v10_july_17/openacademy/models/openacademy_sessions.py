# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields


class OpenacademySession(models.Model):
    """Openacademy Sesssion Model"""

    _name = "openacademy.session"
    _STATES = [
        ("new", "New"),
        ("approve", "Approved"),
        ("reject", "Rejected"),
        ("open", "Open"),
        ("cancel", "Cancelled"),
        ("done", "Done")
    ]

    _order = "sequence, id"

    name = fields.Char(string="Session Name", required=True, index=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence", default=100)
    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date")
    day_duration = fields.Float(string="Duration in Days", digits=(5,2))
    code = fields.Char(string="Code", size=64)
    state = fields.Selection(selection=_STATES, string="Status", 
                                required=True, default="new")
    session_notes = fields.Html(string="Session Notes")
    banner_image = fields.Binary(string="Banner")
    max_seats = fields.Integer(string="Maximum Seats")
    min_registration = fields.Integer(string="Minimum required registrations")
    rem_seat_per = fields.Float(string="Remaining Seats(%)")
    admin_email = fields.Char(string="Admin Email")
    session_url = fields.Char(string="Published URL")
    