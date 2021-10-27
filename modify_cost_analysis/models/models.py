# -*- coding: utf-8 -*-

from odoo import models, fields, api


class modify(models.AbstractModel):
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    @api.model
    def _get_report_values(self, docids, data=None):
        productions = self.env['mrp.production'] \
            .browse(docids) \
            .filtered(lambda p: p.state != 'cancel')
        res = None
        if all(production.state == 'done' for production in productions):
            res = self.get_lines(productions)
        return {'lines': res,
                'productions': productions,
                }
