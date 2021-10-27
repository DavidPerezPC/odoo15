from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def open_wizard_account_date(self):
        return {
            'name': _('Cambio de fecha'),
            'res_model': 'account.change.date',
            'view_mode': 'form',
            'context': {'default_name':self.name,
                        'default_move_id': self.id},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }