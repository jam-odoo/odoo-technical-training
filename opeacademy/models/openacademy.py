# -*- coding: utf-8 -*-
import pprint
from datetime import datetime
from dateutil import relativedelta

from openerp import models
from openerp import fields
from openerp import api
from openerp.exceptions import ValidationError
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

pp = pprint.PrettyPrinter(indent=4)


class Partner(models.Model):

    _name = "res.partner"
    _inherit = "res.partner"

    instructor = fields.Boolean(string="Instructor")


class OpenAcademySessionTags(models.Model):
    """OpenAcademySessionTags"""
    _name = "openacademy.session.tags"

    name = fields.Char(string="Tag")


class OpenAcademyCourse(models.Model):

    _name = "openacademy.course"

    name = fields.Char(string="Course Name", size=100, help="Name of the Course", required=True)
    active = fields.Boolean(string="Active")
    notes = fields.Html(string="Description")
    code = fields.Char(string="Code", size=10)
    responsible_id = fields.Many2one(comodel_name="res.users", string="Responsible")
    session_ids = fields.One2many(comodel_name="openacademy.sessions", inverse_name="course_id", string="Sessions")

    @api.multi
    def name_get(self):
        if "name_join" in self.env.context.keys() and self.env.context['name_join']:
            names = []
            for record in self:
                name = "({}) {}".format(record.code or "/", record.name)
                names.append((record.id, name))
            return names
        return super(OpenAcademyCourse, self).name_get()


class OpenAcademySession(models.Model):
    """OpenAcademy Session Managment"""
    _name = "openacademy.sessions"

    _OS_STATES = [
        ("new", "New Session"),
        ("approve", "Approved"),
        ("reject", "Rejected"),
        ("open", "Open"),
        ("confirm", "Confirmed"),
        ("done", "Finished"),
        ("cancel", "Cancelled"),
    ]

    name = fields.Char(string="Session Name", required=True, readonly=True, states={'new': [('readonly', False)]})
    active = fields.Boolean(string="Active", default=True)
    start_date = fields.Datetime(string="Start Date", default=fields.Datetime.now, required=True, readonly=True, states={'new': [('readonly', False)]})
    end_date = fields.Datetime(string="End Date", required=True, readonly=True, states={'new': [('readonly', False)]})
    duration = fields.Float(string="Duration", digits=(5,2), required=True, readonly=True, states={'new': [('readonly', False)]})
    notes = fields.Html(string="Notes", readonly=True, states={'new': [('readonly', False)]})
    max_seat = fields.Integer(string="Maximum Avaliable Seats", default=10, readonly=True, states={'new': [('readonly', False)]})
    min_seat = fields.Integer(string="Minimum Required Registration", default=0, readonly=True, states={'new': [('readonly', False)]})
    banner = fields.Binary(string="Event Banner")
    state = fields.Selection(selection=_OS_STATES, string="States", default="new", required=True)
    instructor_id = fields.Many2one(comodel_name="res.partner", required=True, string="Instructor", readonly=True, states={'new': [('readonly', False)]})
    course_id = fields.Many2one(comodel_name="openacademy.course", required=True, string="Course", readonly=True, states={'new': [('readonly', False)]})
    tag_ids = fields.Many2many(comodel_name="openacademy.session.tags", relation="rel_session_tags", column1="session_id", column2="tag_id", string="Keywords")
    attendee_ids = fields.One2many(comodel_name="openacademy.attendee", inverse_name="session_id", string="Attendee", readonly=True, states={'open': [('readonly', False)]}) 
    total_seats = fields.Float(compute="_compute_totalseats", string="Total Invitations")
    confirm_seats = fields.Float(compute="_compute_totalseats", string="Confirmed Invitations")
    rem_seat_per = fields.Float(compute="_compute_totalseats", string="Reaming Seats")

    @api.depends("attendee_ids")
    def _compute_totalseats(self):
        for rec in self:
            rec.total_seats = sum([ att.count for att in rec.attendee_ids ])
            rec.confirm_seats = sum([ att.count for att in rec.attendee_ids if att.state == "show" ])
            rec.rem_seat_per = ((rec.max_seat - rec.confirm_seats)/rec.max_seat) * 100.0
    @api.one
    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End Date should be greater then start date !")        

    @api.onchange('start_date', 'duration')
    def _onchange_start_date(self):
        start_date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATETIME_FORMAT)
        self.end_date = start_date + relativedelta.relativedelta(days=self.duration)

    @api.one
    def approve_session(self):
        self.state = "approve"

    @api.one
    def reject_session(self):
        self.state = "reject"

    @api.one
    def confirm_session(self):
        if self.confirm_seats < self.min_seat:
            raise ValidationError("Can not confirm Session !\nConfirmed Seats count '{}' less then minimum required seats({})".format(self.confirm_seats, self.min_seat))
        self.state = "confirm"

    @api.one
    def done_session(self):
        self.state = "done"

    @api.one
    def session_reset(self):
        self.delete_workflow()
        self.state = 'new'
        self.create_workflow()

    # @api.model
    # @api.returns('self', lambda value: value.id)
    # def create(self, vals):
    #     pp.pprint(vals)
    #     if vals.get("start_date") and vals.get("end_date") and vals.get("end_date") <  vals.get("start_date"):
    #         raise ValidationError("End Date should be greater then start date !")
    #     res = super(OpenAcademySession, self).create(vals)
    #     return res
    # @api.one
    # def write(self, vals):
    #     res = super(OpenAcademySession, self).write(vals)
    #     if self.start_date and self.end_date and self.end_date < self.start_date:
    #         raise ValidationError("End Date should be greater then start date !")


class OpenAcademyAttendee(models.Model):
    """OpenAcademyAttendee"""
    _name = "openacademy.attendee"
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    count = fields.Integer(string="Attendee Count", default=1, required=True)
    email = fields.Char(string="Email")
    state = fields.Selection(selection=[('invite', "Invited"), ("show", "Going"), ("noshow", "Not Going"), ("maybe", "Maybe")], string="State", default="invite")
    session_id = fields.Many2one(comodel_name="openacademy.sessions", string="Session")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.email = self.partner_id.email