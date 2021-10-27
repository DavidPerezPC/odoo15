# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MRPUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    def action_unbuild(self):
        res = super(MRPUnbuild, self).action_unbuild()
        if self.mo_id:
            self.mo_id.state = 'unbuild'
        return res