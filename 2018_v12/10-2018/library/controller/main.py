# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request


class LibararyController(http.Controller):

    @http.route('/books', type='http', auth='public', website=True)
    def get_books(self, **kwargs):
        books = request.env['library.book'].search([])
        values = {
            'books': books,
        }

        return request.render("library.books", values)