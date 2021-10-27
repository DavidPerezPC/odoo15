# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddTerritory(models.Model):
    _inherit = 'account.move.line'

    x_delivery_territory_id = fields.Many2one(comodel_name="zone.pam", string="Territorio por dirección de entrega", compute="_compute_territory", store=True)

    @api.depends('move_id', 'move_id.partner_id.x_zone', 'move_id.partner_shipping_id.x_zone')
    def _compute_territory(self):
        for rec in self:
            rec.x_delivery_territory_id = False
            if rec.move_id.partner_shipping_id:
                rec.x_delivery_territory_id = rec.move_id.partner_shipping_id.x_zone.id
            else:
                rec.x_delivery_territory_id = rec.move_id.partner_id.x_zone.id



