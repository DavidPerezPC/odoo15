# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TransferRemision(models.Model):
    _inherit = "stock.picking"

    def calculate_remission_details(self):
        self.ensure_one()
        picking = self.sudo()
        cfdi_values = {}

        for line in picking.move_ids_without_package:
            sale_line = line.sale_line_id
            quantity_done_wo_reward = line.quantity_done
            qty_reward = 0
            if not sale_line:
                order_id = self.env['sale.order'].search([('name', '=', line.origin)])
                if order_id:
                    sale_line_obj = self.env['sale.order.line']
                    sale_line = sale_line_obj.search([('order_id', '=', order_id.id),('product_id', '=',line.product_id.id)],limit=1)
                    sale_lines = sale_line_obj.search([('order_id', '=', order_id.id),('product_id', '=',line.product_id.id)])
                    sale_reward_lines = sale_lines.filtered(lambda l: l.is_reward_line == True)
                    if len(sale_lines) != len(sale_reward_lines):
                        qty_reward = ((sale_reward_lines and sum(sale_reward_lines.mapped('product_uom_qty'))) or 0)
                        quantity_done_wo_reward = quantity_done_wo_reward - qty_reward
            if not line.product_id or not line.quantity_done:
                continue
            price_reduce = sale_line.price_unit * (1.0 - sale_line.discount / 100.0)
            cfdi_values[sale_line.id] = {}
            cfdi_values[sale_line.id]['wo_discount'] = sale_line.price_unit * (1 - (sale_line.discount / 100.0))
            taxes = sale_line.tax_id.compute_all(cfdi_values[sale_line.id]['wo_discount'], quantity=quantity_done_wo_reward, product=sale_line.product_id, partner=sale_line.order_id.partner_shipping_id)['taxes']
            cfdi_values[sale_line.id]['total_line_taxes']= sum(tax.get('amount') for tax in taxes)
            cfdi_values[sale_line.id]['discount_promotion'] = (sale_line.is_reward_line and 0.00 or
                                sale_line.price_unit * quantity_done_wo_reward * (sale_line.discount_promotions/100.0))
            cfdi_values[sale_line.id]['total_wo_discount'] = picking.sale_id.currency_id.round((sale_line.price_unit * quantity_done_wo_reward) + (qty_reward * 0.01))
            cfdi_values[sale_line.id]['discount_amount'] = picking.sale_id.currency_id.round(cfdi_values[sale_line.id]['total_wo_discount'] - 
                                                                                            (cfdi_values[sale_line.id]['wo_discount'] * quantity_done_wo_reward) - (qty_reward * 0.01))
            cfdi_values[sale_line.id]['line_original'] = sale_line
            cfdi_values[sale_line.id]['line_qty'] = line.quantity_done

        return cfdi_values
            