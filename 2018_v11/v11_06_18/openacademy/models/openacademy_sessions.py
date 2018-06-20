# -*- encoding: utf-8 -*-

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class OpenAcademyTags(models.Model):

    _name = 'openacademy.tags'

    name = fields.Char(string='Tag', required=True, index=True)
    color = fields.Integer(string="Color Index")

class OpenAcademySession(models.Model):

    _name = 'openacademy.session'

    def _get_default_user(self):
        return self.env.user.id


    name = fields.Char(string='Title', required=True, index=True,
                        help='Title goes here... e.g. Odoo Technical Training June 2018',
                        size=200)
    course_id = fields.Many2one(comodel_name="openacademy.course", required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible', default=_get_default_user)
    user_email = fields.Char(related="user_id.email", string="Email")
    code = fields.Char(string="Code", szie=64)
    start_date = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now())
    duration = fields.Float(string="Duration (Days)", digits=(5,2), default=1)
    end_date = fields.Datetime(string='End Date')
    notes = fields.Html(string="Description")
    active = fields.Boolean(string="Active", default=True)
    total_seat = fields.Integer(string="Total Seats", default=10)
    min_seat = fields.Integer(string="Minimum Required Registrations")
    can_overbook = fields.Boolean(string="Can be Overbooked")
    remmain_seat_per = fields.Float(string="Remaing Seats(%)", digits=(5,2), default=0.0)
    booked_seats = fields.Integer(string="Booked Seats")
    all_day = fields.Selection(selection=[('yes', 'Yes'),('no', 'No')], string="Allday Event")
    state = fields.Selection(selection=[('new', 'New'),
                                      ('approve', 'Approved'),
                                      ('open', 'Open'),
                                      ('cancel', 'Cancel'),
                                      ('done', 'Done')], string="Status", default="new")
    image = fields.Binary(string="Image")
    tag_ids = fields.Many2many(comodel_name="openacademy.tags", relation="rel_openacademy_session_tags",
                                column1="sessoin_id", column2="tag_id",string="Tags")


    _sql_constraints = [
        ('unique_sessoin_code', 'UNIQUE (code)','The code must be unique !'),
    ]

    @api.constrains('start_date', 'end_date')
    @api.multi
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                _logger.warning("Sesssion '{}' ({}) was attmepted to save with wrong dates by user {}.".format(record.name, record, self.env.user.id))
                raise UserError(_("Start date can not be in future of end date."))

    @api.onchange("course_id")
    def onchange_course_id(self):
        #self.ensure_one()
        if self.course_id:
            self.image = self.course_id.banner

    @api.onchange("start_date", "duration")
    def onchange_dates(self):
        #self.ensure_one()
        if self.start_date:
            self.end_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S") + relativedelta(days=self.duration)

    @api.model
    def create(self, vals):
        if vals.get('code'):
            vals.update({'code': vals['code'].upper()})
        res = super(OpenAcademySession, self).create(vals)

        return res

    @api.multi
    def write(self, vals):
        if vals.get('code'):
            vals.update({'code': vals['code'].upper()})
        return super(OpenAcademySession, self).write(vals)

    @api.multi
    def unlink(self):
        #raise ValidationError(_("Session can not be deledted, please archive the record"))
        self.active = False
        return True