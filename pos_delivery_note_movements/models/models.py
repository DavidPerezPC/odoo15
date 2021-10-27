# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class poss_config(models.Model):
    _inherit = 'pos.config'

    x_restricted_albaran = fields.Boolean(string='Movimientos de albaran', store=True, default=False)


class pos_session(models.Model):
    _inherit = 'pos.session'

    @api.constrains('state')
    def pos_validation(self):
        for rec in self:
            if rec.picking_ids:
                for i in rec.picking_ids:
                    if i.state != 'done':
                        if i.state != 'cancel':                            
                            if self.config_id.x_restricted_albaran:
                                raise UserError('No podra cerrar el PoS si hay movimientos de albaran pendientes de cerrar.')
