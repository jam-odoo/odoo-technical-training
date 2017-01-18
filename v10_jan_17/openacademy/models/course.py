# -*- coding: utf-8 -*-

from odoo import models, fields


class OpenAcademyCourse(models.Model):
    """OpenAcademy Course"""

    _name = "openacademy.course"

    name = fields.Char(string="Course Title", size=128, required=True, help="Course Name goes here i.e. Odoo Technical Training")


class OpenAcademySession(models.Model):
    """OpenAcademy Sessions"""

    _name = "openacademy.session"

    name = fields.Char(string="Session Subject", size=128, required=True, help="Session Subject goes here i.e. Odoo Technical Training")
    seat_price= fields.Float(string="Seat Price", digits=(6,3), default=100.00, required=True)
    active = fields.Boolean(string="Archived ?", default=True)
    start_date = fields.Datetime(string="Session Start Date", required=True)
    end_date = fields.Datetime(string="Session End Date", required=True)
    duration = fields.Integer(string="Duration (In days)", default=1)
    description = fields.Html(string="Description")
    banner = fields.Binary(string="Banner")
    state = fields.Selection(selection=[("new", "New"), 
                                        ('confirm', 'Confirmed'), 
                                        ('open', 'Open Session'), 
                                        ('done', "Done"),
                                        ('cancel', "cancelled")], 
                                    string="Status", default="new")
    secert_key = fields.Char(string="Secert Key")
    total_seats =  fields.Integer(string="Total Seats")
    min_seats = fields.Integer(string="Minimum Required Saets")
    remain_seats = fields.Float(string="Remianing Seats")
