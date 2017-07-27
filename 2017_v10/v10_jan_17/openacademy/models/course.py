# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields
from odoo import api
from odoo import exceptions
from odoo import _

class OpenAcademyTags(models.Model):
    """OpenAcademy Tags"""
    _name = "openacademy.tags"

    name = fields.Char(string="Tag", size=128, required=True)
    color = fields.Integer(string="Color")

class OpenAcademyCourse(models.Model):
    """OpenAcademy Course"""

    _name = "openacademy.course"

    name = fields.Char(string="Course Title", size=128, required=True, help="Course Name goes here i.e. Odoo Technical Training")
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sesssions")



class OpenAcademySession(models.Model):
    """OpenAcademy Sessions"""

    _name = "openacademy.session"

    _inherit = ["mail.thread"]

    name = fields.Char(string="Session Subject", size=128, required=True, help="Session Subject goes here i.e. Odoo Technical Training")
    seat_price= fields.Float(string="Seat Price", digits=(6,3), default=100.00, required=True, track_visibility="always")
    active = fields.Boolean(string="Archived ?", default=True)
    start_date = fields.Datetime(string="Session Start Date", required=True, readonly=True, states={'new':[('readonly', False)]}, track_visibility="onchange")
    end_date = fields.Datetime(string="Session End Date", required=False, track_visibility="onchange", readonly=True, states={'new':[('readonly', False)]})
    duration = fields.Integer(string="Duration (In days)", default=0,  track_visibility="onchange")
    description = fields.Html(string="Description")
    banner = fields.Binary(string="Banner")
    state = fields.Selection(selection=[("new", "New"), 
                                        ('approve', 'Approved'),
                                        ('reject', 'Rejected'),
                                        ('open', 'Open'),
                                        ('confirm', 'Confirmed'), 
                                        ('done', "Done"),
                                        ('cancel', "Cancelled")], 
                                    string="Status", default="new")
    secert_key = fields.Char(string="Secert Key")
    total_seats =  fields.Integer(string="Total Seats")
    total_reg_seats =  fields.Integer(string="Total Regsitered Seats")
    min_seats = fields.Integer(string="Minimum Required Saets")
    remain_seats = fields.Float(compute="_get_remain_seats", string="Remianing Seats")
    code  = fields.Char(string="Code", size=36)
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", required=True, readonly=True, states={'new':[('readonly', False)]})
    course_id = fields.Many2one(comodel_name="openacademy.course", string="Course", readonly=True, states={'new':[('readonly', False)]})
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", relation="rel_session_tags", column1="session_id", column2="tag_id", string="Tags")
    attendee_ids = fields.One2many(comodel_name="openacademy.attendee", inverse_name="session_id", string="Attendee")
    sequence = fields.Integer(string="Sequence", default=10)
    owner_id = fields.Many2one(comodel_name="res.users", string="Reposnsible", required=True)

    _sql_constraints = [
        ("consta_uniq_session_code", "UNIQUE(code)", "Code must be unique !")
    ]

    @api.multi
    @api.depends("total_seats", "total_reg_seats")
    def _get_remain_seats(self):
        for record in self:
            vals ={"remain_seats":0.0}
            if record.total_seats > 0.0:
                remain_seats = record.total_seats - record.total_reg_seats
                remain_seats_per = (remain_seats / float(record.total_seats))*100.00
                vals.update({'remain_seats': remain_seats_per})
            record.write(vals)

    @api.multi
    def confirm_session(self):
        for record in self:
            record.state = "confirm"
            record.message_post(body="Your Session has been confimed on")
        print "******************", self


    @api.multi
    def do_something(self):
        for record in self:
            print "==========", record

    @api.multi
    def action_approve(self):
        for record in self:
            record.state = "approve"
            record.message_post(body="Congratulations ! Your session has been approived by ....")

    @api.multi
    def action_reject(self):
        for record in self:
            record.state = "reject"

    @api.multi
    def action_open(self):
        for record in self:
            record.state = "open"

    @api.multi
    def action_confirm(self):
        for record in self:
            record.state = "confirm"

    @api.multi
    def action_cancel(self):
        for record in self:
            record.state = "cancel"

    @api.multi
    def action_reset(self):
        for record in self:
            record.delete_workflow()
            record.state = "new"
            record.create_workflow()
    @api.model
    def print_this(self):
        return "#*#"*5

    @api.multi
    @api.constrains("start_date", "end_date")
    def _check_dates(self):     
        for record in self:
            if record.end_date < record.start_date:
                raise exceptions.ValidationError(_("End date can not be in past to start date"))
            if datetime.strptime(record.start_date, "%Y-%m-%d %H:%M:%S") < datetime.now():
                raise exceptions.ValidationError(_("Event Start date should be future date !"))

    @api.model
    def create(self, vals):
        print "=================", vals
        if vals.get("total_seats") == 0:
            vals.update({'total_seats': 20})
        partner = super(OpenAcademySession, self).create(vals)
        print '@####################', partner
        return partner

    @api.multi
    def write(self, vals):
        print "=================", vals
        # if "start_date" in vals and datetime.strptime(vals.get("start_date"), "%Y-%m-%d %H:%M:%S") < datetime.now():
        #     raise exceptions.ValidationError("Event Start date should be future date or greater then {}!".format(datetime.now().strftime("%Y-%m-%d")))        
        res = super(OpenAcademySession, self).write(vals)
        return res 


    @api.onchange("start_date", "duration")
    def onchange_start_date(self):
        for record in self:
            if record.start_date:
                end_date = datetime.strptime(record.start_date, "%Y-%m-%d %H:%M:%S") + timedelta(days=record.duration)
                record.end_date  = end_date


class OpenAcademyAttendee(models.Model):
    "OpenAcademy Attendee Info"
    _name = "openacademy.attendee"

    _rec_name = "full_name"

    partner_id = fields.Many2one(comodel_name="res.partner", string="Attendee Partner")
    full_name = fields.Char(string="Full Name", required=True)
    email =  fields.Char(string="Email")
    count = fields.Integer(string="Invited Count")
    state = fields.Selection(selection=[("invite", "Invited"), ("attend", "Attending"), ("not_attend", "Not Attending"), ("maybe", "May Be Attending")], string="Status", default="invite")
    session_id = fields.Many2one(comodel_name="openacademy.session", string="Session")