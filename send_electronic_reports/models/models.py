# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,timedelta


class SendElectronicReports(models.Model):
    _name = 'send.electronic.reports'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Enviar reportes'

    name = fields.Char(string='Nombre')
    company_id = fields.Many2one('res.company', string='Compañía', default= lambda self:self.env.company.id)
    move_type = fields.Selection(string='Tipo de movimiento',
                                 selection=[
                                     ('out_invoice', 'Factura de clientes'),
                                     ('payment' , 'Pagos')
                                 ])
    template_id = fields.Many2one('mail.template', string='Plantilla de correo electrónico')

    def action_report_sent(self):
        for rec in self:
            initial_date = datetime.today() - timedelta(days=2)
            end_date = datetime.today() + timedelta(days=2)
            if rec.move_type == 'out_invoice':
                move = rec.env['account.move'].search([('company_id','=',self.company_id.id),('invoice_date','>=',initial_date),('invoice_date','<=',end_date),('move_type','=','out_invoice'),('state','=','posted'),('edi_state','in',('to_send','to_cancel'))])
            else:
                move = rec.env['account.payment'].search([('company_id','=',self.company_id.id),('date','>=',initial_date),('date','<=',end_date),('state','=','posted'),('edi_state','in',('to_send','to_cancel'))])

            if move:
                rec.message_post_with_template(rec.template_id.id)


class ReportSendElectronic(models.Model):
    _name = 'report.send_electronic_reports.print_unstamped_document_report'
    _description = 'Generación de reporte'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Agrupamos los registros por medio del folio
        docs = self.env['send.electronic.reports'].browse(docids)
        company_id = docs['company_id']
        move_type = docs.move_type
        initial_date = datetime.today() - timedelta(days=2)
        end_date = datetime.today() + timedelta(days=2)

        if move_type == 'out_invoice':
            records = self.env['account.move'].search([('company_id','=',company_id.id),('invoice_date','>=',initial_date),('invoice_date','<=',end_date),('move_type','=','out_invoice'),('state','=','posted'),('edi_state','in',('to_send','to_cancel'))])
        else:
            records = self.env['account.payment'].search([('company_id','=',company_id.id),('date','>=',initial_date),('date','<=',end_date),('state','=','posted'),('edi_state','in',('to_send','to_cancel'))])
        return {
            'docs': docs,
            'records': records
        }