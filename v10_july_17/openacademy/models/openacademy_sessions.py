# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields


class OpenAcademyTags(models.Model):

    _name = "openacademy.tags"

    name = fields.Char(string="Session Name", required=True, index=True)
    color = fields.Integer(string="Color")

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
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", ondelete="restrict", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Resnposible", required=True)
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="rel_session_partner_m2m", column1="session_id", column2="parnter_id", string="Partner Attendees")
    course_id = fields.Many2one(comodel_name="openacademy.course", string="Course", required=True)
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", string="Tags")

class OpenacademyCourse(models.Model):
    """Openacademy Sesssion Model"""

    _name  = "openacademy.course"

    name = fields.Char(string="Course Name")
    code = fields.Char(string="Code", size=32)
    user_id = fields.Many2one(comodel_name="res.users", string="Resnposible", required=True)
    course_contain = fields.Html(string="Course Contains") 
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sessions")


class Partner(models.Model):

    _inherit = "res.partner"

    session_ids = fields.Many2many(comodel_name="openacademy.session", relation="rel_session_partner_m2m", column1="parnter_id", column2="session_id", string="Sesssions")