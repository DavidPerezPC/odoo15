# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    check_all_client_payment_method = fields.Boolean(default=False, string="Respetar formas de pago de cliente")