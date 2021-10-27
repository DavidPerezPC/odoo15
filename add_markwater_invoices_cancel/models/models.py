# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddMarkwaterInvoicesCancel(models.TransientModel):
    _inherit = 'res.config.settings'

    x_activate_markwater_cancel = fields.Boolean(string="Marca de agua(Facturas canceladas)")

    @api.model
    def get_values(self):
        res = super(AddMarkwaterInvoicesCancel, self).get_values()
        res.update(x_activate_markwater_cancel=self.env['ir.config_parameter'].sudo().get_param(
            'AddMarkwaterInvoicesCancel.x_activate_markwater_cancel'))
        return res

    def set_values(self):
        super(AddMarkwaterInvoicesCancel, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        x_activate_markwater_cancel = self.x_activate_markwater_cancel or False

        param.set_param('AddMarkwaterInvoicesCancel.x_activate_markwater_cancel',
                        x_activate_markwater_cancel)


