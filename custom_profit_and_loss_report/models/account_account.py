from odoo import api, fields, models

class AccountAccount(models.Model):
    _inherit = 'account.account'

    x_is_discount_account = fields.Boolean(string='Es una cuenta de descuento',default=False)
