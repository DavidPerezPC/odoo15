# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class condition_allow(models.Model):
    _inherit = 'account.move'

    @api.constrains('line_ids')
    def validation(self):
        for rec in self:
            for i in rec.line_ids:
                analytic_account = i.analytic_account_id
                analytic_tag = i.analytic_tag_ids
                if analytic_account and analytic_tag:
                    names = ''
                    for e in analytic_tag:
                        if e.active_analytic_distribution:
                            names = names + str(e.name) + ", "
                    if names != '':
                        cadena = "No se permite añadir la etiqueta analítica prorrateable: " + names + " si se específico cuenta analítica."
                        raise UserError(cadena)
                    else:
                        pass
                else:
                    pass
