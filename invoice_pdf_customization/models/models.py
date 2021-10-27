# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def get_footer_values(self):
        invoice = self.sudo()
        response = {}
        promissory_note_one = """POR ESTE PAGARE ME(NOS) OBLIGO(AMOS) A PAGAR INCONDICIONALMENTE, A LA ORDEN DE"""
        promissory_note_two = """EL DÍA """+str(self.invoice_date_due)+""", EN ESTA CIUDAD, O EN CUALQUIER OTRA QUE SEA(MOS) 
        REQUERIDO(OS) A ELECCION DEL TENEDOR DE ESTE PAGARE EL DIA DEL VENCIMIENTO INDICADO, LA CANTIDAD DE, 
        """+str(self.amount_residual)+""" ("""+ invoice._l10n_mx_edi_cfdi_amount_to_text() +""""), VALOR RECIBIDO 
        EN MERCANCIA A """
        reiterate =  """(NUESTRA) ENTERA SATISFACCION, SI NO FUERE PUNTUALMENTE CUBIERTO A SU VENCIMIENTO, PAGARE 
        INTERESES MORATORIOS HASTA SU LIQUIDACION TOTAL A RAZON DEL % MENSUAL, CULIACÁN SINALOA, A """+str(self.invoice_date_due)

        response['promissory_note_one'] = promissory_note_one
        response['promissory_note_two'] = promissory_note_two
        response['company'] = """INDUSTRIAS GUACAMAYA SA DE CV, """
        response['reiterate'] = reiterate

        return response

    def is_invoice_client(self):
        invoice = self

        if 'in_invoice' in invoice.move_type:
            return False
        if 'out_invoice' in invoice.move_type:
            return True

    def calculate_lines_details(self):
        self.ensure_one()
        invoice = self.sudo()
        details_move_lines = {}

        code_iva = "14020001"
        subtotal_products = 0
        subtotal_iva = 0
        subtotal_credit = 0

        total_debit = 0
        total_credit = 0

        details_move_lines["details_product"] = []
        details_move_lines["details_tax"] = []
        details_move_lines["details_credit"] = []
        details_move_lines["details_credit"] = []
        for line in invoice.line_ids:
            #extraccion de detalles del producto
            if line.product_id:
               subtotal_products = subtotal_products + line.debit
               details_move_lines["details_product"].append(line)
            #Extracción para los detalles de iva
            elif not line.product_id and line.tax_line_id:
                subtotal_iva = subtotal_iva + line.debit
                details_move_lines["details_tax"].append(line)
            #Exctracción de otros conceptos
            elif not line.product_id and not line.tax_line_id:
                subtotal_credit = subtotal_credit + line.credit
                details_move_lines["details_credit"].append(line)

        total_debit = subtotal_products + subtotal_iva
        total_credit = subtotal_credit
        details_move_lines.update({"subtotal_products": subtotal_products})
        details_move_lines.update({"subtotal_tax" : subtotal_iva})
        details_move_lines.update({"total_debit" : total_debit})
        details_move_lines.update({"total_credit": total_credit})

        return details_move_lines

    def calculate_no_entrada(self):
        #se obtiene el ultimo insertado según las fechas
        # response = self.env["stock.picking"].search([('origin','=',self.invoice_origin),('partner_id','=',self.partner_id.id),('date_done', '<=',self.invoice_date)], order= 'date_done desc', limit=1)
        if self.invoice_line_ids:
            purchase_orders = []
            stock_picking = []
            for line in self.invoice_line_ids:
                if line.purchase_order_id:
                    if line.purchase_order_id not in purchase_orders:
                        purchase_orders.append(line.purchase_order_id)
                        response = self.env["stock.picking"].search(
                            [('origin', '=', line.purchase_order_id.name), ('partner_id', '=', self.partner_id.id),
                             ('state', '=', 'done')], order='date_done desc', limit=1)
                        if response:
                            stock_picking.append(response.name)
            if stock_picking:
                stock_picking_values = ", ".join(stock_picking)
                return stock_picking_values
            return {}


    def action_post(self):
        super(AccountInvoice, self).action_post()
        try:            
            if 'out_invoice' in self.move_type:                
                self.action_process_edi_web_services()
        except Exception as error:            
            _logger.info(error)

class CustomAccountMoveLine(models.Model):
    _inherit = "account.move.line"

    discount_promotions = fields.Float(string='Descuento Promociones (%)', digits='Discount', default=0.0, readonly=True)
