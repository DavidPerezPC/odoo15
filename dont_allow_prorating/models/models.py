# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class dont_prorating(models.Model):
    _inherit = 'account.analytic.tag'

    @api.constrains('active_analytic_distribution', 'analytic_distribution_ids')
    def totalpor(self):
        total = list()
        for rec in self:
            if rec.active_analytic_distribution:
                for i in rec.analytic_distribution_ids:
                    total.append(i.percentage)
                summation = sum(total)
                summation = round(summation, 2)
                if summation > 100 or summation < 100:
                    raise ValidationError("La sumatoria de porcentajes tiene que ser igual a 100")
                elif summation == 100:
                    pass
