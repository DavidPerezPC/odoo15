# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pytz import timezone
from datetime import datetime


class NewModule(models.Model):
    _inherit = 'stock.picking'

    x_fecha_recepcion = fields.Datetime(string="Fecha de recepción", compute='_get_date_of_reception')

    @api.depends('origin')
    def _get_date_of_reception(self):
        for rec in self:
            rec.x_fecha_recepcion = ''
            order_origin_obj = rec.env['purchase.order'].search([('name', '=', rec.origin)], limit=1)
            if order_origin_obj:
                rec.x_fecha_recepcion = order_origin_obj.effective_date
