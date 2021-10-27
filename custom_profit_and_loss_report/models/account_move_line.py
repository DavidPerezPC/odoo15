from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_account_analytic_group = fields.Char(string='Grupo de cuanta analítica', store=True,
                                           related='analytic_account_id.group_id.name')
    x_account_type = fields.Many2one(string='Tipo de cuenta', related='account_id.user_type_id', store=True)
    x_account_internal_group = fields.Selection(string='Grupo interno de cuenta', related='account_id.internal_group',
                                                store=True)
    x_is_discount_account = fields.Boolean(string='Es una cuenta de descuento', related='account_id.x_is_discount_account',
                                         store=True)
    x_account_name = fields.Char(string="Nombre de la cuenta", store=True, related='account_id.name')
    x_has_multiple_analytic_lines = fields.Char(string='Tiene multiples lineas analíticas',
                                                   compute='get_analytic_lines', store=True)

    @api.depends('analytic_line_ids')
    def get_analytic_lines(self):
        for rec in self:
            if len(rec.analytic_line_ids) == 1:
                rec.x_has_multiple_analytic_lines = '1 linea'
            elif len(rec.analytic_line_ids) > 1:
                rec.x_has_multiple_analytic_lines = 'multiples lineas'
            else:
                rec.x_has_multiple_analytic_lines = 'sin lineas'


