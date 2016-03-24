##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models
from openerp import fields, api, exceptions

from openerp.tools.translate import _

class wiz_add_attendee(models.TransientModel):

    _name = "wiz.add.attendee"

    attendee_ids = fields.Many2many("res.partner", string="Attendees")

    def default_get(self, cr, uid, fields_list, context=None):
        res = super(wiz_add_attendee, self).default_get(cr, uid, fields_list, context=context)
        session_pool = self.pool.get('openacademy.session')
        recordset = session_pool.browse(cr, uid, context.get('active_id'), context)
        res.update({'attendee_ids': [rec.id for rec in recordset.att_ids]})
        return res

    @api.one
    def add_attendee(self):
        if self.attendee_ids:
            session_pool = self.env['openacademy.session']
            recordset = session_pool.browse(self.env.context['active_id'])
            recordset.att_ids = self.attendee_ids
        else:
            raise exceptions.MissingError(_("No/Zero Attendees Selected !"))


