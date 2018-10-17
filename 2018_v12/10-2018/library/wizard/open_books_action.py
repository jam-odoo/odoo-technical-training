# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class WizardOpenBooks(models.TransientModel):

    _name = "wizard.open.books"

    name = fields.Char(string="Label", default="Click Open to see the books", readonly=True)

    @api.multi
    def open_books(self):
        print ("*"*100)
        rent_ids = self.env['library.rent'].browse(self.env.context.get('active_ids'))
        book_ids = rent_ids.mapped('book_id')
        action_data = self.env.ref('library.action_view_library_book_wizard').read()[0]
        action_data.update({
            'domain': [('id', 'in', book_ids.ids)],
        })
        if len(book_ids) == 1:
            action_data.update({
                'view_mode': 'form',
                'views': [(self.env.ref('library.view_library_book_form').id, 'form')],
                'res_id': book_ids.id
            })
        print (action_data)
        return action_data