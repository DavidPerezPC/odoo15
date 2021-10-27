# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.constrains('order_ids', 'state')
    def _constrains_order_ids(self):
        if self.order_ids:
            refund_payments = []
            for rec in self.order_ids:
                if rec.state != 'invoiced':
                    if self.config_id.x_restricted_closure:
                        if rec.amount_paid < 0:
                            refund_payments.append(rec.name)
                        if not refund_payments:
                            raise UserError(_('Facture todos sus pedidos por favor'))


class PosCongig(models.Model):
    _inherit = 'pos.config'

    x_restricted_closure = fields.Boolean(string='Cierre de caja restringido', store=True, default=False)
