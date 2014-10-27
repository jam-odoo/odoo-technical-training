##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from datetime import datetime, timedelta

from openerp import models, fields, api, exceptions


class openacademy_course(models.Model):

    _name = "openacademy.course"

    _description = "OpenAcademy Session Model"

    name = fields.Char(string="Course Name", required=True, help="Name of the Course e.g. ODoo Techncial Training")
    active = fields.Boolean(string='Active', default=True)
    attendee_count = fields.Integer(string="Attendee Count")
    user_id = fields.Many2one('res.users', string="Responsible", required=True)
    notes = fields.Html(string="Description")
    code = fields.Char(size=10, string="Code")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    @api.model
    def create(self, vals):
        
        res = super(openacademy_course, self).create(vals)
        return res

#    def create(self, cr, uid, vals, context=None):
#        import pprint
#        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(vals)
#        res = super(openacademy_course, self).create(cr, uid, vals, context=context)
#        print "#######################", res
#        return res

class openacademy_session(models.Model):

    _name = 'openacademy.session'
    _inherit = ['mail.thread']
    _description = "OpenAcademy Session Model"

    @api.model
    def get_end_date(self):
        end_date =datetime.now() + timedelta(days=5)
        return end_date.strftime("%Y-%m-%d %H:%M:%S")
    @api.model
    def get_rem_per(self):
        count = 100.0
        for reocrd in self:
            if reocrd.attendee_count > 0:
                count =100 - (float(reocrd.attendee_count) / float(reocrd.max_att))*100
            reocrd.rem_seat_per = count


    name = fields.Char(string="Name", required=True, help="Name of the Session e.g. ODoo Techncial Training November")
    code = fields.Char(size=10, string="Code")
    active = fields.Boolean(string='Active', default=True)
    attendee_count = fields.Integer(string="Attendee Count", compute="_compute_count" )
    max_att = fields.Integer(string="Max Attenddes", default=10)
    min_att = fields.Integer(string="Min Attenddes", default=3)
    rem_seat_per = fields.Float(string="Remianing Seat Percetage", digits=(5,2), compute="get_rem_per")
    start_date = fields.Datetime(string="Start Date", required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(string="End Date", required=True)
    duration = fields.Float(digits=(5,2), string="Duration (Hours)")
    state = fields.Selection(selection=[('new', 'New'), ('approv', 'Session Approved'),('open', 'Open Session'), ('confirm', 'Confirmed Session'),('done', 'Session Done'), ('cancel', 'Cancelled Session')], string="Status", required=True, default='new', track_visibility="onchange")
    notes = fields.Html(string="Description")
    banner = fields.Binary(string="Banner")
    instructor_id = fields.Many2one('res.partner', string="Instructor", required=True)
    course_id = fields.Many2one('openacademy.course', string="Course", required=True)
    att_ids = fields.Many2many('res.partner', 'rel_session_partner', 'session_id', 'partner_id', string="Attenddes")

    _defaults = {
        'duration': "5.0",
        'end_date': get_end_date,
#        "state": "new",
#        'active': True,
    }

    _sql_constraints = [
        ("const_unique_code", 'unique (code)', 'Code must be Unique !')
    ]

    @api.one
    def action_confirm(self):
        self.state = 'confirm'

    @api.one
    def action_approve(self):
        self.state = 'approv'

    @api.one
    def action_reject(self):
        self.state = 'cancel'

    @api.one
    def action_open(self):
        self.state = 'open'

    @api.one
    def action_done(self):
        self.state = 'done'
 


    @api.one
    @api.depends('att_ids')
    def _compute_count(self):
        self.attendee_count = len(self.att_ids)

#    _constraints = [
#        ('', '')
#    ]

    @api.onchange('start_date')
    def onchange_startdate(self):
        end_date = fields.Datetime.from_string(self.start_date) + timedelta(days=self.duration)
        self.duration = 5.0
        self.end_date = end_date.strftime('%Y-%m-%d %H:%M:%S')

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.end_date <= self.start_date:
            raise exceptions.ValidationError("Invalid Dates !")  

    @api.model
    def create(self, vals):
        flag = False
#        if vals.get('code') and self.search([('code', '=', vals.ge'code'))]):
#            raise exceptions.ValidationError("Code must be Unique!")  
#        else:
#            raise exceptions.ValidationError("Code can not be empty!")
        result = super(openacademy_session, self).create(vals)
        return result


    @api.multi
    def write(self, vals):
#        if 'code' in vals.keys() and vals.get('code') and self.search([('code', '=', vals.get('code'))]):
#            raise exceptions.ValidationError("Code must be Unique!")  
        return super(openacademy_session, self).write(vals)

class res_partner(models.Model):

    _inherit = "res.partner"

    instructor = fields.Boolean(string="Is Instructor ?")


