# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class promotions_board(models.Model):
    _name = 'promotions.board'
    _description = 'Módulo creado para vista de tablero de promociones'

    # # Campos relacionados
    x_active = fields.Boolean(string="Estado Promoción")
    x_customers = fields.Char(string="Clientes")
    x_route = fields.Char(string="Ruta")
    x_name_promotion = fields.Char(string="Nombre de promoción")
    x_products = fields.Char(string="Productos")
    x_reward_type = fields.Char(string="Recompensa")

    def update_promotions(self):
        self.env['promotions.board'].search([]).unlink()
        # tools.drop_view_if_exists(self.env.cr, self._table)
        # self._cr.execute("""CREATE OR REPLACE VIEW %s AS (SELECT row_number() OVER () as id, x_as as x_active ,
        # name as x_name_promotion, route as x_route,partners as x_customers,products as x_products FROM
        # coupon_program WHERE active=true)""" % (self._table,))
        data = self.env['coupon.program'].search([('active', '=', True)])
        for i in data:
            if i.x_as:
                type = i.reward_type
                discount = "Descuento" if type == "discount" else "Descuento en cascada" if type == "multi_discount" else "Producto gratis" if type == "product" else "Envío gratis" if type == "free_shipping" else "Mismo Producto Gratis"
                if i.re_products:
                    products = eval(str(i.re_products))
                    if i.re_partners:
                        customers = eval(str(i.re_partners))
                        if i.re_route:
                            route = eval(str(i.re_route))
                            for cus in range(len(customers)):
                                for rou in range(len(route)):
                                    for pro in range(len(products)):
                                        dictionary = {
                                            'x_name_promotion': i.name,
                                            'x_active': i.x_as,
                                            'x_customers': customers[cus],
                                            'x_route': route[rou],
                                            'x_products': products[pro],
                                            'x_reward_type': discount
                                        }
                                        self.env['promotions.board'].create(dictionary)
