# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions



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

    def get_start_date(self):
        return fields.Datetime.now()


    name = fields.Char(string="Session Name", required=True, index=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence", default=100)
    start_date = fields.Datetime(string="Start Date", default=get_start_date,required=True)
    end_date = fields.Datetime(string="End Date")
    day_duration = fields.Float(string="Duration in Days", digits=(5,2))
    code = fields.Char(string="Code", size=64)
    state = fields.Selection(selection=_STATES, string="Status", 
                                required=True, default="new")
    session_notes = fields.Html(string="Session Notes")
    banner_image = fields.Binary(string="Banner")
    max_seats = fields.Integer(string="Maximum Seats")
    min_registration = fields.Integer(string="Minimum required registrations")
    rem_seat_per = fields.Float(string="Remaining Seats(%)", compute="_compute_partner_count", store=True)
    admin_email = fields.Char(string="Admin Email")
    session_url = fields.Char(string="Published URL")
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", ondelete="restrict", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="Resnposible", required=True)
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="rel_session_partner_m2m", column1="session_id", column2="parnter_id", string="Partner Attendees")
    course_id = fields.Many2one(comodel_name="openacademy.course", string="Course", required=True)
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", string="Tags")
    country_id = fields.Many2one(comodel_name="res.country", related="instructor_id.country_id", store=True)
    total_partner_count = fields.Integer(compute="_compute_partner_count", string="Total Invited Partners")

    _sql_constraints = [
        ("uniq_session_code", "UNIQUE (code)", "Code must be unique for every session !")
    ]

    @api.multi
    @api.constrains("end_date", "start_date")
    def _check_session_dates(self):
        if self.filtered(lambda record :  record.end_date < record.start_date):
            raise exceptions.ValidationError("End date can not be before start date !")
        # for record in self:
        #     if record.end_date < record.start_date:
        #         raise exceptions.ValidationError("End date can not be before start date !")

    @api.depends("attendee_ids", "max_seats")
    def _compute_partner_count(self):
        for record in self:
            record.total_partner_count = len(record.attendee_ids.ids)
        if record.max_seats > 0:
            record.rem_seat_per = - ((record.total_partner_count - record.max_seats) / float(record.max_seats)) * 100.00

    @api.onchange("end_date", "start_date")
    def onchange_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                record.day_duration = (datetime.strptime(record.end_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(record.start_date, "%Y-%m-%d %H:%M:%S")).days
            else:
                record.day_duration = 0.0


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