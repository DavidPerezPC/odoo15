# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class validation_blank(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def validation_error(self):
        for rec in self:
            if rec.order_line:
                order_line = rec.order_line
                for i in order_line:
                    if str(i.name).strip() == '':
                        raise UserError("No se permite guardar descripción de linea de producto en blanco.")

