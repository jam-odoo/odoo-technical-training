# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class openacademy_session(models.Model):
	"""Open Academy Session"""

	_name = "openacademy.session"

	name = fields.Char(string="Session Title", size=200, \
						translate=True, required=True, copy=False)
	max_seat = fields.Integer(string="Maximum Seats", required=True,\
								 default=10, index=True)
	duration_days = fields.Float(string="Duration(days)", digits=(6,3),\
								 required=True, default=1)
	start_date = fields.Datetime(string="Start Date")
	end_date = fields.Datetime(string="End Date")
	is_public = fields.Boolean(string="Is Public Event ?")
	notes = fields.Text(string="Notes")
	contain = fields.Html(string="Session Course")
	banner = fields.Binary(string="Banner")
