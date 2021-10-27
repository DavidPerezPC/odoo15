# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools


class comparison(models.Model):
    _inherit = 'stock.move'

    x_amount_to_consume = fields.Float(string="Cantidad a consumir", related="should_consume_qty", store=True)
    x_consumed_by_production = fields.Float(string="Cantidad consumida por producción", related="quantity_done", store=True)
