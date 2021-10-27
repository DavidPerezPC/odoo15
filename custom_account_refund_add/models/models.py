# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        super(AccountMove, self).action_post()
        if 'out_refund' in self.move_type or 'in_refund' in self.move_type:
            if self.reversed_entry_id:
                move_lines = self.line_ids.filtered(lambda line: line.account_internal_type in ('receivable','payable') and not line.reconciled)
                for line in move_lines:
                    self.reversed_entry_id.js_assign_outstanding_line(line.id)