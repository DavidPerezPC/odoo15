# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,timedelta

class StatementsReports(models.Model):
    _inherit = 'send.electronic.reports'

    move_type = fields.Selection(selection_add=[('statement_bank', 'Extractos bancarios')])

    def action_report_sent(self):
        super(StatementsReports, self).action_report_sent()
        for rec in self:
            move = False
            initial_date = datetime.today() - timedelta(days=2)
            end_date = datetime.today() + timedelta(days=2)
            if rec.move_type == 'statement_bank':
                move = rec.env['account.move'].search([('company_id', '=', self.company_id.id), ('move_type', '=', 'entry'),('date','>=',initial_date),('date','<=',end_date),('journal_id.type','=','bank'),('state','=','posted'),('edi_state','in',('to_send','to_cancel'))])
            if move:
                rec.message_post_with_template(rec.template_id.id)

class ReportSendElectronic(models.Model):
    _inherit = 'report.send_electronic_reports.print_unstamped_document_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = super(ReportSendElectronic, self)._get_report_values(docids, data=None)
        docs = self.env['send.electronic.reports'].browse(docids)
        company_id = docs['company_id']
        move_type = docs.move_type
        initial_date = datetime.today() - timedelta(days=2)
        end_date = datetime.today() + timedelta(days=2)

        if move_type == 'statement_bank':
            records = self.env['account.move'].search([('company_id', '=', company_id.id), ('move_type', '=', 'entry'), ('date', '>=', initial_date),('date', '<=', end_date), ('journal_id.type', '=', 'bank'), ('state', '=', 'posted'),('edi_state', 'in', ('to_send', 'to_cancel'))])
            report['records'] = records

        return report