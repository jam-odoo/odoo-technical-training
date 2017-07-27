# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request



class OpenAcademy(http.Controller):

    @http.route(["/session",
                "/session/session_id/<int:session_id>"],  type="http", auth="public", website=True, methods=['GET'])
    def session(self, session_id=0,**post):
        values = {
            "session_ids": []
        }
        if session_id:
            values.update({'session_ids': request.env["openacademy.session"].sudo().search([('id', "=", session_id)])})
            return request.render("openacademy.session_page", values)
        #request.redirect("/")
        values.update({
            "session_ids": request.env["openacademy.session"].sudo().search([])
        })
        return request.render("openacademy.sessions", values)