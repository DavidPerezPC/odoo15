# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockSerial(models.Model):
    _inherit = 'stock.production.lot'

    x_stock_quant = fields.One2many('stock.quant', 'lot_id', string="Existencias de inventario")


class batch_existence(models.Model):
    _inherit = 'stock.move.line'

    x_quantity_lot = fields.Float(string="Cantidad disponible", compute="calculed_quantity")

    @api.depends('lot_id')
    def calculed_quantity(self):
        for rec in self:
            if rec.location_id.usage == 'internal':
                existence = rec.env['stock.quant'].search(
                    [('product_id', '=', rec.product_id.id), ('location_id', '=', rec.location_id.id),
                     ('lot_id', '=', rec.lot_id.id)], limit=1)
                self.x_quantity_lot = existence.quantity
            else:
                existence = rec.env['stock.quant'].search(
                    [('product_id', '=', rec.product_id.id), ('location_id', '=', rec.location_dest_id.id)], limit=1)
                self.x_quantity_lot = existence.quantity