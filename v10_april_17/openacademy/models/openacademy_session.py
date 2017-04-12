# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta


from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _


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

    def _get_user_company(self):
        return self.env.user.company_id.id

    def _set_end_date(self):
        start_date = datetime.now()
        end_date = start_date + relativedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        return end_date

    name = fields.Char(string="Session Name", required=True, help="Session name goes here... e.g. Odoo Technical Training")
    active = fields.Boolean(string="Archived ?", default=True)
    sequence  = fields.Integer(string="Sequence", default=10)
    website_description = fields.Html(string="Website Description")
    notes = fields.Text(string="Notes", help="Internal Notes for session.")
    max_seats = fields.Integer(string="Maximum Seats", required=True, help="Maximum number of seats avilable for session")
    min_saets = fields.Integer(string="Minimum Seats", required=True)
    invited_partner = fields.Integer(compute="_compute_invited_partner", store=True, string="Invited Partners")
    start_date = fields.Datetime(string="Session Start Date", required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(string="Sesssion End Date", required=True, default=_set_end_date)
    duration = fields.Float(string="Duration in Days", required=True, default=1)
    state = fields.Selection(selection=STATES, string="States", default="new")
    left_seat_per = fields.Float(compute="_compute_invited_partner", string="Remaining Seats", digits=(8,5))
    image = fields.Binary(string="Image")
    course_id = fields.Many2one(comodel_name="openacademy.course", ondelete="restrict", required=True, copy=False, index=True)
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor")
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="rel_session_parnter_attendee", \
                                    column1="session_id", column2="partner_id", string="Partner Attendee")
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", string="Tags")
    code = fields.Char(string="Code", size=32)
    company_id = fields.Many2one(comodel_name="res.company", required=True, string="Compnay", default=_get_user_company)
    website = fields.Char(related="instructor_id.website", string="Website")
    country_id = fields.Many2one(compute="res.country", related="instructor_id.country_id", string="Country")

    _sql_constraints = [
        ("uqni_code_per_session", "UNIQUE(code, company_id)", "Code must be unique per company !"),
    ]


    @api.depends("attendee_ids")
    def _compute_invited_partner(self):
        for record in self:
            partners = len(record.attendee_ids.ids)
            record.invited_partner = partners
            record.left_seat_per = ((record.max_seats - partners ) / 100.00)*100.00


    @api.multi
    @api.constrains("start_date", "end_date")
    def _constrains_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                # import pdb
                # pdb.set_trace()
                raise exceptions.ValidationError(_("Sesssion start date\
                 (%s) can not be after end date (%s)"%(record.start_date, record.end_date)))

    @api.onchange("start_date", "end_date")
    def _onchnage_dates(self):
        vals = {}
        if self.start_date > self.end_date:
            # raise exceptions.ValidationError(_("Sesssion start date\
            #      (%s) can not be after end date (%s)"%(self.start_date, self.end_date)))
            vals.update({"warning": {
                        "title": "Date Validation !",
                        "message": "Sesssion start date can not be after end date.",
                }
            })
        elif self.start_date and self.end_date:
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
            diff  = end_date - start_date
            self.duration = diff.days
        return vals

    @api.onchange("course_id")
    def _onchange_course(self):
        self.code = self.course_id.code if self.course_id else "<NOT FOUND>"
        vals = {'domain': {'instructor_id': [('id', 'in', [ i for i in range(1,10)])]}}
        return vals


    @api.multi
    def copy(self, default=None):
        # if self.ensure_one():
        #     self.myoperation()
        # else    
        #     for record in self:
        #         record.myoperation()
        raise exceptions.ValidationError("Document can not be duplicated")