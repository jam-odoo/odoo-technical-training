# -*- coding: utf-8 -*-

from odoo import models, fields

class OpenAcademyCourse(models.Model):
    """OpenAcademy Course Managment"""

    _name = "openacademy.course"

    name = fields.Char(string="Course Name", required=True, help="Course name goes here... e.g. Odoo Trainings")
    course_contain = fields.Html(string="Course Contain")
    active = fields.Boolean(string="Active", default=True)
    code = fields.Char(string="Code", size=32)
    user_id = fields.Many2one(comodel_name="res.users", string="Responsible",ondelete="set null", required=True, copy=False, index=True)
    session_ids = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id", string="Sesssions")