# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



class OpenAcademyMain(http.Controller):

    @http.route(["/sessions",
                "/sessions/<int:session_id>"], type="http", auth="user",website=True)
    def get_sessions(self, session_id=None,*args, **kwargs):
        print "=====================", session_id
        print '~~~~~~~~~~~~~~~~~~~~~~',args
        if session_id:
            try:
                session_id = int(session_id)
                session = request.env["openacademy.session"].sudo().browse(session_id)
                return request.render("openacademy.openacademy_session_page", {'session': session})
            except:
                return request.redirect("/404")

        else:
            sessions = request.env["openacademy.session"].sudo().search([])
            values = {
                "sessions": sessions,
            }
            return request.render("openacademy.openacademy_sessions", values)