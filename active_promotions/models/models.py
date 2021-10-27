# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class promotions(models.Model):
    _inherit = 'coupon.program'
    _description = 'Módulo para promociones activas por ruta/cliente/producto'

    x_as = fields.Boolean(string="Promoción Activa", compute="date_compute", store=False)
    partners = fields.Char(string="Clientes", compute="list_partners", store=False)
    products = fields.Char(string="Productos", compute="list_products", store=False)
    route = fields.Char(string="Ruta", compute="list_partners", store=False)

    re_name_promotions = fields.Char(string="Nombre de promoción", related="name", store=True)
    re_company_id = fields.Many2one(string="Compañia", related="company_id", store=True)
    re_active_store = fields.Boolean(string="Promoción Activa", store=True)
    re_partners = fields.Char(string="Clientes", store=True)
    re_products = fields.Char(string="Productos", related="products", store=True)
    re_route = fields.Char(string="re_Ruta", store=True)

    @api.depends("rule_date_from", "rule_date_to")
    def date_compute(self):
        for rec in self:
            today = datetime.now()
            if rec.rule_date_from and rec.rule_date_to:
                if rec.rule_date_from <= today <= rec.rule_date_to:
                    rec.x_as = True
                    rec.re_active_store = True
                else:
                    rec.x_as = False
                    rec.re_active_store = False
            else:
                rec.x_as = False
                rec.re_active_store = False

    @api.depends('rule_partners_domain')
    @api.onchange('rule_partners_domain')
    def list_partners(self):
        for ref in self:

            ref.partners = ''
            ref.route = ''
            names = list()
            route_partners = list()
            var = ref.rule_partners_domain
            out = []
            if var:
                out = eval(var)
                out = list(out)
                if len(out) <= 3:
                    out = str(out)
                    out = eval(out)
                    customer_search = ref.env['res.partner'].search(out)
                    for data in customer_search:
                        names.append(data.name)
                        name_route = data.user_id.property_warehouse_id.name
                        if name_route:
                            if name_route not in route_partners:
                                route_partners.append(name_route)

                elif len(out) >= 3:
                    var = ref.rule_partners_domain
                    if var:
                        var = var.replace('[', '(')
                        var = var.replace(']', ')')
                        var = var.replace('"', '\'')

                        out = eval(var)
                        out = list(out)

                        customer_search = ref.env['res.partner'].search(out)

                        for data in customer_search:
                            names.append(data.name)
                            name_route = data.user_id.property_warehouse_id.name
                            if name_route not in route_partners:
                                route_partners.append(name_route)
            ref.partners = names
            ref.re_partners = names
            ref.route = route_partners
            ref.re_route = route_partners

    @api.depends('rule_products_domain')
    def list_products(self):
        for ref in self:
            ref.products = ''
            var = ref.rule_products_domain
            out = eval(var)
            out = list(out)

            if len(out) <= 3:
                out = str(out)
                out = eval(out)
                product_search = ref.env['product.product'].search(out)
                names = list()
                for c in product_search:
                    names.append(c.name)
                ref.products = names

            elif len(out) >= 3:
                var = ref.rule_products_domain
                var = var.replace('[', '(')
                var = var.replace(']', ')')
                var = var.replace('"', '\'')
                out = eval(var)
                out = list(out)

                product_search = ref.env['product.product'].search(out)
                names = list()
                for c in product_search:
                    names.append(c.name)
                ref.products = names