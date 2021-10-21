# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockDurationDays(models.Model):
    _name = 'stock.duration.days'
    _description = 'Módulo para generacion de reporte de duracion en dias'

    default_code = fields.Char(string="Referencia")
    product_id = fields.Char(string="Producto")
    product_uom = fields.Char(string="Unidad de medida")
    category = fields.Char(string="Categoria")
    qty_pendding_supply = fields.Float(string="Pendiente de surtir")
    qty_per_supply = fields.Float(string="Cantidad pendiente de surtir")
    qty_on_hand = fields.Float(string="Inventario actual")
    daily_consumption_average = fields.Float(string="Consumo promedio diario")
    qty_product = fields.Float(string="Cantidad de producto")
    duration_days = fields.Integer(string="Duración en días")
    location_id = fields.Many2one('stock.location',string="Ubicación")
    company_id = fields.Many2one('res.company', string="Compañia", default=lambda self: self.env.company, store=True)
    inventory_id = fields.Many2one('stock.generate.report', string="Inventario en dias")
    pendding_supply_ids = fields.Many2many("stock.move.line", string="Pendientes de surtir")
    reserved_ids = fields.Many2many('stock.move', string="Reservados")

