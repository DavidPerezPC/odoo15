# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomLinkSaleToInvoice(models.TransientModel):
    _name = 'link.sale.to.invoice'
    _description = 'Enlazar ventas con facturas'

    invoice = fields.Many2one('account.move',string='Factura')
    sale_order = fields.Many2one('sale.order',string='Venta')

    def link(self):
        if self.invoice.move_type == 'out_invoice':
            if self.invoice.amount_total_signed == self.sale_order.amount_total:
                lines = []
                for line in self.sale_order.order_line:
                    for invoice_line in self.invoice.invoice_line_ids:
                        if line.product_id.id == invoice_line.product_id.id and line.product_uom_qty == invoice_line.quantity:
                            line.invoice_lines = [(4,invoice_line.id)]
                            lines.append(line)
                            for move_line in line.invoice_lines:
                                if move_line.quantity != invoice_line.quantity and move_line.move_id.move_type == 'out_invoice':
                                    line.invoice_lines = [(3, move_line.id)]
                            self.invoice.invoice_origin = self.sale_order.name

                    if self.invoice.reversal_move_id:
                        for reversal in self.invoice.reversal_move_id:
                            for reverse_line in reversal.invoice_line_ids:
                                if line.product_id.id == reverse_line.product_id.id and line.price_unit == reverse_line.price_unit:
                                    line.invoice_lines = [(4, reverse_line.id)]

                for sale_line in self.sale_order.order_line:
                    if sale_line not in lines:
                        for move_line in sale_line.invoice_lines:
                            if move_line.move_id.move_type == 'out_invoice':
                                sale_line.invoice_lines = [(3, move_line.id)]