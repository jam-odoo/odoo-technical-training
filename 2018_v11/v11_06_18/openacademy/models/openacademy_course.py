# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class OpenAcademyCouse(models.Model):

    _name = 'openacademy.course'

    name = fields.Char(string='Title', required=True, index=True,
                        help='Couse title goes here (e.g. Odoo Technical Training)')
    active = fields.Boolean(string="Active", default=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Responsible')
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sessions")
    session_count = fields.Integer(string="# Sessions", compute="_get_session_count")
    notes = fields.Html(string="Notes")
    banner = fields.Binary(string='Banner')
    banner_fname = fields.Char(string="Banner File Name")

    @api.multi
    @api.depends('session_ids')
    def _get_session_count(self):
    	for course in self:
    		course.session_count =  len(course.session_ids)

    def open_sessions(self):
    	action_id = self.env.ref("openacademy.action_view_openacademy_sessions")
    	action_data = action_id.read()[0]
    	action_data.update({'domain': [('course_id', '=', self.id)]})
    	return action_data