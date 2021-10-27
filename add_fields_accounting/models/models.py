# -*- coding: utf-8 -*-

from odoo import models, fields, api


class add_fields(models.Model):
    _inherit = 'account.move.line'

    x_territory = fields.Many2one("zone.pam", related="partner_id.x_zone", string="Territorio", store=True)
    x_sector = fields.Many2one("res.partner.industry", related="partner_id.industry_id", string="Sector", store=True)
