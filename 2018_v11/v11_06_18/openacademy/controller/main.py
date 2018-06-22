# -*- encoding: utf-8 -*-

from odoo import http, _
from odoo.http  import request


class SessionController(http.Controller):

    @http.route([
            '/session',
            '/session/<int:session>',
        ], type='http', auth='public', website=True)
    def sessions(self, session=False, **post):
        if session:
            sesions = request.env['openacademy.session'].browse(session)
        else:
            sesions = request.env['openacademy.session'].search([])
        values = {
            'sessions': sesions
        }
        return request.render('openacademy.sessions', values)