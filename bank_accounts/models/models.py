# -*- coding: utf-8 -*-

from odoo import models, fields, api


class modify(models.Model):
    _inherit = 'res.partner.bank'

    x_branch_office = fields.Char(string="Sucursal")
    x_accounts_to_show = fields.Boolean(string="Mostrar en factura")
