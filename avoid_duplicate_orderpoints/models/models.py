# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.constrains('product_id', 'product_min_qty', 'product_max_qty', 'qty_multiple',
                    'warehouse_id','location_id','group_id','company_id','route_id')
    def _check_orderpoint_rules(self):        
        for rec in self:
            orderpoint_obj = rec.env['stock.warehouse.orderpoint'].search([
                '&', '&', '&','&','&','&','&','&',
                ('product_id', '=', rec.product_id.id),
                ('product_min_qty', '=', rec.product_min_qty),
                ('product_max_qty', '=', rec.product_max_qty),
                ('qty_multiple', '=', rec.qty_multiple),
                ('warehouse_id','=', rec.warehouse_id.id),
                ('location_id','=',rec.location_id.id),
                ('group_id','=', rec.group_id.id),
                ('company_id','=', rec.company_id.id),
                ('route_id','=', rec.route_id.id)
            ], limit=2)

            if len(orderpoint_obj) > 1:
                raise UserError(
                    _("La regla de abastecimiento ya existe, si desea modificarla su id es [%s]" % orderpoint_obj[0].id))

