# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime


class repport_new(models.Model):
    _name = 'order.service.report'

    x_route_pos = fields.Char(string="Ruta", store=True)
    x_receipt_number_pos = fields.Char(string="Número de recibo", store=True)
    x_creation_date_pos = fields.Datetime(string="Fecha de creación", store=True)
    x_customer_pos = fields.Char(string="Cliente", store=True)
    x_cashier_pos = fields.Char(string="Cajero", store=True)
    x_authorizing_pos = fields.Char(string="Autorizador", store=True)
    x_authorization_date_pos = fields.Datetime(string="Fecha de autorización", store=True)
    x_product_pos = fields.Char(string="Producto", store=True)
    x_state_pos = fields.Char(string="Estado", store=True)
    x_remaining_days_pos = fields.Char(string="Tiempo autorización", store=True, help="Formato: DD HH/MM")
    x_commercial_user_pos = fields.Char(string="Comercial", store=True)

    def report_service(self):
        self.env['order.service.report'].search([]).unlink()
        data = self.env['pos.autorizacion'].search([])
        for i in data:
            for products in i.detalle_ids:
                dictonary = {
                    'x_route_pos': i.ruta,
                    'x_receipt_number_pos': i.name,
                    'x_creation_date_pos': i.create_date,
                    'x_customer_pos': i.partner_id.name,
                    'x_cashier_pos': i.user_id.name,
                    'x_authorizing_pos': i.autorizador_id.name,
                    'x_authorization_date_pos': i.fch_autorizacion,
                    'x_product_pos': products.product_id.name,
                    'x_state_pos': i.state,
                    'x_remaining_days_pos': i.remaining_days,
                    'x_commercial_user_pos': i.x_commercial_user_pos.name
                }
                self.env['order.service.report'].create(dictonary)
