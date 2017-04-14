# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta


from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _
from odoo import tools

STATES = [
    ("new", "New"),
    ('approve', 'Approve'),
    ('reject', "Rejected"),
    ("open", "Open for registration"),
    ('confirm', 'Confirmed'),
    ('cancel', 'Cancelled'),
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

    _inherit = ["mail.thread"]

    def _get_user_company(self):
        return self.env.user.company_id.id

    def _get_user(self):
        return self.env.user.id


    def _set_end_date(self):
        start_date = datetime.now()
        end_date = start_date + relativedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        return end_date

    name = fields.Char(string="Session Name", required=True, help="Session name goes here... e.g. Odoo Technical Training", track_visibility="onchange", readonly=True, states={'new': [('readonly', False)]})
    active = fields.Boolean(string="Archived ?", default=True)
    sequence  = fields.Integer(string="Sequence", default=10)
    website_description = fields.Html(string="Website Description")
    notes = fields.Text(string="Notes", help="Internal Notes for session.")
    max_seats = fields.Integer(string="Maximum Seats", required=True, help="Maximum number of seats avilable for session")
    min_saets = fields.Integer(string="Minimum Seats", required=True)
    invited_partner = fields.Integer(compute="_compute_invited_partner", store=True, string="Invited Partners")
    start_date = fields.Datetime(string="Session Start Date", required=True, default=fields.Datetime.now(), track_visibility="onchange", readonly=True, states={'new': [('readonly', False)]})
    end_date = fields.Datetime(string="Sesssion End Date", required=True, default=_set_end_date, track_visibility="onchange", readonly=True, states={'new': [('readonly', False)]})
    duration = fields.Float(string="Duration in Days", required=True, default=1)
    state = fields.Selection(selection=STATES, string="States", default="new", track_visibility="onchange")
    left_seat_per = fields.Float(compute="_compute_invited_partner", string="Remaining Seats", digits=(8,5))
    image = fields.Binary(string="Image")
    image_small = fields.Binary(compute="_get_small_image",string="Image Small")
    course_id = fields.Many2one(comodel_name="openacademy.course", ondelete="restrict", required=True, copy=False, index=True, track_visibility="always", readonly=True, states={'new': [('readonly', False)]})

    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", track_visibility="onchange", readonly=True, states={'new': [('readonly', False)]})
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="rel_session_parnter_attendee", \
                                    column1="session_id", column2="partner_id", string="Partner Attendee")
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", string="Tags")
    code = fields.Char(string="Code", size=32)
    company_id = fields.Many2one(comodel_name="res.company", required=True, string="Compnay", default=_get_user_company)
    website = fields.Char(related="instructor_id.website", string="Website")
    country_id = fields.Many2one(compute="res.country", related="instructor_id.country_id", string="Country")
    invitation_ids = fields.One2many(comodel_name="openacademy.invitation", inverse_name="session_id", string="Invitations")
    user_id  = fields.Many2one(comodel_name="res.users", string="Responisble", required=True, default=_get_user)

    _sql_constraints = [
        ("uqni_code_per_session", "UNIQUE(code, company_id)", "Code must be unique per company !"),
    ]

    @api.multi
    def action_approved(self):
        self.write({"state": 'approve'})

    @api.multi
    def action_rejected(self):
        self.write({"state": 'reject'})

    @api.multi
    def action_open(self):
        self.write({"state": 'open'})

    @api.multi
    def action_confirm(self):
        self.write({"state": 'confirm'})

    @api.multi
    def action_cancel(self):
        self.write({"state": 'cancel'})

    @api.multi
    def action_done(self):
        self.write({"state": 'done'})

    @api.multi
    def reset_workflow(self):
        for record in self:
            record.delete_workflow()
            record.create_workflow()
            record.state = "new"

    @api.multi
    def get_fullname(self):
        return "%s (%s)"%(self.name, self.code)

    @api.depends("image")
    def _get_small_image(self):
        for record in self:
            record["image_small"] = tools.image_resize_image_small(record.image)

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
        self.instructor_id = False
        instructor_ids = []
        if self.course_id:
            instructor_ids = self.env["res.partner"].search([('course_ids', 'in', self.course_id.id)]).ids
        vals = {'domain': {'instructor_id': [('id', 'in', instructor_ids)]}}
        return vals


    @api.multi
    def copy(self, default=None):
        # if self.ensure_one():
        #     self.myoperation()
        # else    
        #     for record in self:
        #         record.myoperation()
        raise exceptions.ValidationError("Document can not be duplicated")

    @api.multi
    def action_approve(self):
        for session in self:
            session.write({"state": "approve"})

    @api.multi
    def open_partners(self):
        attendee_ids = [("id", "in", [ p.id for record in self for p in self.attendee_ids ])]
        # action = self.env.ref("base.action_partner_form").read()[0]
        # print "\n\n>>>>>", action
        # action.update({"domain": attendee_ids, "context":{}, "view_mode": "tree"})
        partner_ids= self.env["res.partner"].search([("customer", "=", True)]).ids
        partner_tree_id =  self.env.ref("base.view_partner_tree").id
        partner_form_id = self.env.ref("base.view_partner_form").id
        action= {
            "type": "ir.actions.act_window",
            "name": "Invited Partners",
            "res_model": "res.partner",
            "domain": attendee_ids,
            "view_mode": "tree",
            "views": [(partner_tree_id, "tree")],
        }
        return action


class OpenAcademyInvitation(models.Model):
    """OpenAcademy Attendees"""

    _name = "openacademy.invitation"


    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    count = fields.Integer(string="Invitation Count", default=1)
    state = fields.Selection(selection=[('invited', "invited"),
                                        ('accept', 'Accpeted'),
                                        ('declined', 'Declined'),
                                        ('pending', 'Pending')], string="State", default="invited")
    session_id = fields.Many2one(comodel_name="openacademy.session", string="Session")

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        if self.partner_id:
            self.name =  self.partner_id.name_get()[0][1]
            self.phone = self.partner_id.phone or self.partner_id.mobile
            self.email = self.partner_id.email