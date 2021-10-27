# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def calcular_promociones(self, partner_id, pricelist_id, orderlines):
        sale_id = self.sudo().create({
            'partner_id': partner_id,
            'pricelist_id': pricelist_id,
        })
        for line in orderlines:
            product_id = self.env['product.product'].browse(line['id'])
            sol_id = self.env['sale.order.line'].sudo().create({
                'name': product_id.name,
                'product_id': product_id.id,
                'product_uom_qty': line['quantity'],
                'price_unit': 0,
                'order_id': sale_id.id,
                'new_price': line['new_price'],
            })
            sol_id.sudo().product_id_change()
            sol_id.sudo()._onchange_discount()
            sol_id.write({
                'product_uom': line['uom_id'],
            })
            sol_id.sudo().product_uom_change()
            if line['discount']:
                sol_id.sudo().write({
                    'price_unit': sol_id.price_subtotal / sol_id.product_uom_qty,
                    'discount': line['discount'],
                })
                sol_id.sudo()._compute_amount()
        sale_id.sudo().recompute_coupon_lines()
        res = []
        for num, line in enumerate(sale_id.order_line):
            res.append({
                'product_id': line.product_id.id,
                'cantidad': line.product_uom_qty,
                'uom_id': line.product_uom.id,
                'total': line.price_subtotal,
                'is_reward_line': line.is_reward_line,
                'discount_promotions': line.discount_promotions,
                'descuento_pdf': line.discount,
                'price_unit_pdf': line.price_unit,
                'new_price': line.new_price,
            })
        sale_id.sudo().unlink()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    new_price = fields.Float()