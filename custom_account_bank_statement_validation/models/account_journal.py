
from odoo import api, fields, models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def create_bank_statement_from_import_banks_csv(self):
        """return action to create a bank statements. This button should be called only on journals with type =='bank'"""
        action = self.env["ir.actions.actions"]._for_xml_id("custom_account_bank_statement_validation.custom_statement_bank_import")
        action.update({
            'views': [[False, 'form']],
            'context': "{'default_journal_id': " + str(self.id) + "}",
        })
        return action

