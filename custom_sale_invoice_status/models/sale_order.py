# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_status = fields.Selection(selection_add=[('partial_invoiced', 'Parcialmente Facturado')])

    @api.depends('picking_ids')
    def _get_invoice_status(self):
        super(SaleOrder, self)._get_invoice_status()
        for rec in self:
            #Variables para identificar el estado de queda movimiento
            done_move = []
            all_backorders = []
            done_backorders = []
            wait_backorders = []
            cancel_backorders = []
            #Obtenemos los movimientos de albaran relacionados a la orden de venta
            # stock_move = self.env['stock.picking'].search([('origin','=', rec.name)])
            stock_move = self.picking_ids
            #Recorremos cada movimiento de albaran para obtener su estado y si este tiene backorder
            for move in stock_move:
                if move.backorder_id:
                    all_backorders.append(move)
                    if move.state == 'done':
                        done_backorders.append(move)
                    elif move.state == 'cancel':
                        cancel_backorders.append(move)
                    else:
                        wait_backorders.append(move)
                if move.state == 'done':
                    done_move.append(move)

            #Filtramos si el pedido tiene lineas que por facturar
            line_to_invoice = rec.order_line.filtered(lambda line: line.invoice_status == 'to invoice')

            #Recorremos las lines del pedido para indicar el estado en el que se encuentra el pedido
            for line in rec.order_line:
                #Si se entrego y facturo menos de lo solicitado y no se genero backorder
                if done_move and not all_backorders:
                    if line.qty_invoiced > 0 and line.qty_invoiced == line.qty_delivered and not line_to_invoice:
                        rec.invoice_status = 'invoiced'
                        line.invoice_status = 'invoiced'
                #Si se llega a cancelar el backorder
                elif done_move and cancel_backorders and not wait_backorders:
                    if line.qty_invoiced > 0 and line.qty_invoiced == line.qty_delivered and not line_to_invoice:
                        rec.invoice_status = 'invoiced'
                        line.invoice_status = 'invoiced'
                #Si se genero backorder de la entrega
                elif done_move and all_backorders:
                    #Si se tienen entregas pendientes con backorder
                    if wait_backorders:
                        if line.qty_invoiced > 0 and line.qty_invoiced == line.qty_delivered and line.qty_to_invoice == 0 and not line_to_invoice:
                            rec.invoice_status = 'partial_invoiced'
                            line.invoice_status = 'partial_invoiced'
                    #Si todas las entregas fueron hechas
                    elif not wait_backorders:
                        if line.qty_invoiced > 0 and line.qty_invoiced == line.qty_delivered and line.qty_to_invoice == 0 and not line_to_invoice:
                            rec.invoice_status = 'invoiced'
                            line.invoice_status = 'invoiced'

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    invoice_status = fields.Selection(selection_add=[('partial_invoiced', 'Parcialmente Facturado')])

class SaleReport(models.Model):    
    _inherit = "sale.report"

    invoice_status = fields.Selection(selection_add=[('partial_invoiced', 'Parcialmente Facturado')])











