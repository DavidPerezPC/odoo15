# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class delete_button(models.Model):
    _inherit = 'account.move'

    def button_delete(self):
        for rec in self:
            rec.invoice_line_ids = [((5, 0, 0))]
