from odoo import api, fields, models

class NewModule(models.Model):
    _inherit = 'account.analytic.line'

    x_account_analytic_group = fields.Char(string='Grupo de cuanta analítica',store=True,
                                           related='account_id.group_id.name')
