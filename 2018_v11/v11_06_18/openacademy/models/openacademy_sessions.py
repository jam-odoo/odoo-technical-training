# -*- encoding: utf-8 -*-

from odoo import models, fields

class OpenAcademySession(models.Model):

    _name = 'openacademy.session'

    name = fields.Char(string='Title', required=True, index=True,
                        help='Title goes here... e.g. Odoo Technical Training June 2018',
                        size=200)
    start_date = fields.Datetime(string='Start Date', required=True)
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