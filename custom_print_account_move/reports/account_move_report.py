# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AccountMoveReport(models.AbstractModel):
    _name = 'report.custom_print_account_move.print_account_move'
    _description = 'Reprte de asientos contables'

    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)

        return {
            'docs' : docs
        }