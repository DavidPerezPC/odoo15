# -*- coding: utf-8 -*-

from odoo import models, fields, api


class update_duplicate_sale_prices(models.Model):
    _inherit = "sale.order"

    # Función para tomar el precio actualizado del producto al duplicar una venta.
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        method = super(update_duplicate_sale_prices, self).copy(default)
        method.update_prices()
        for rec in method.order_line:
            rec.purchase_price = rec.product_id.standard_price
        return method
