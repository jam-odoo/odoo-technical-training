# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class WebsiteEqipments(http.Controller):


    @http.route([
            '/equipments',
            '/equipment/<int:equipment_id>'
    ], auth="public", website=True)
    def equipments(self, equipment_id=False,**post):
        if equipment_id:
            vals = {
                "equipment": request.env["equipment.equipment"].browse(equipment_id)
            }
            return request.render("equipments.equipment_page_view", vals)
        vals = {
            "equipments" : request.env["equipment.equipment"].search([])
        }
        return request.render("equipments.equipments_view", vals)