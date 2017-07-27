# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class OpenAcademyFroms(http.Controller):

    @http.route([
        "/sessions",
        "/session/<int:session_id>"
    ], website=True)
    def sessions(self, session_id=False, **kwargs):
        if session_id:
            data = {
                "session": request.env["openacademy.session"].sudo().browse(session_id)
            }
            return request.render("openacademy.oa_sessions_page", data)

        else:
            data = {
                "sessions": request.env["openacademy.session"].sudo().search([])
            }
            return request.render("openacademy.oa_sessions_list", data)

