# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SendElectronicReports(models.Model):
    _inherit = 'send.electronic.reports'

    move_type = fields.Selection(selection_add=[('sale_to_invoice', 'Venta a facturar')])

    def action_report_sent(self):
        super(SendElectronicReports, self).action_report_sent()
        for rec in self:
            move = False
            difference = False
            if rec.move_type == 'sale_to_invoice':
                move = rec.env['sale.order'].search([('company_id','=',self.company_id.id),('invoice_status','=','to invoice')])

                for record in move:
                    total_delivered = sum(record.order_line.mapped('qty_delivered'))
                    total_invoiced =  sum(record.order_line.mapped('qty_invoiced'))
                    if total_invoiced > total_delivered:
                        difference = True

            if move and difference:
                rec.message_post_with_template(rec.template_id.id)

class ReportSendElectronic(models.Model):
    _inherit = 'report.send_electronic_reports.print_unstamped_document_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = super(ReportSendElectronic, self)._get_report_values(docids, data=None)
        docs = self.env['send.electronic.reports'].browse(docids)
        company_id = docs['company_id']
        move_type = docs.move_type

        sale_orders = []
        if move_type == 'sale_to_invoice':
            records = self.env['sale.order'].search([('company_id','=',company_id.id),('invoice_status','=','to invoice')])
            for record in records:
                total_delivered = sum(record.order_line.mapped('qty_delivered'))
                total_invoiced = sum(record.order_line.mapped('qty_invoiced'))
                if total_invoiced > total_delivered:
                    sale_orders.append(record)
            report['records'] = sale_orders

        return report