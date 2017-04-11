# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields

STATES = [
    ("new", "New"),
    ('approve', 'Approve'),
    ('reject', "Rejected"),
    ("open", "Open for registration"),
    ('confirm', 'Confirmed'),
    ('done', 'Done')
]

class OpenAcademyTags(models.Model):
    """OpenAcademy Tags"""
    _name = "openacademy.tags"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")

class OpenAcademySession(models.Model):
    """OpenAcademy Session Managment"""

    _name = "openacademy.session"

    name = fields.Char(string="Session Name", required=True, help="Session name goes here... e.g. Odoo Technical Training")
    active = fields.Boolean(string="Archived ?", default=True)
    sequence  = fields.Integer(string="Sequence", default=10)
    website_description = fields.Html(string="Website Description")
    notes = fields.Text(string="Notes", help="Internal Notes for session.")
    max_seats = fields.Integer(string="Maximum Seats", required=True, help="Maximum number of seats avilable for session")
    min_saets = fields.Integer(string="Minimum Seats", required=True)
    start_date = fields.Datetime(string="Session Start Date", required=True)
    end_date = fields.Datetime(string="Sesssion End Date", required=True)
    duration = fields.Float(string="Duration in Days", required=True)
    state = fields.Selection(selection=STATES, string="States", default="new")
    left_seat_per = fields.Float(string="Remaining Seats", digits=(8,5))
    image = fields.Binary(string="Image")
    course_id = fields.Many2one(comodel_name="openacademy.course", ondelete="restrict", required=True, copy=False, index=True)
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor")
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="rel_session_parnter_attendee", \
                                    column1="session_id", column2="partner_id", string="Partner Attendee")
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", string="Tags")