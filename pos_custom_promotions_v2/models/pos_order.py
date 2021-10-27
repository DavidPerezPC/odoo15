# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _prepare_invoice_line(self, order_line):
        fields_return = super(PosOrder, self)._prepare_invoice_line(order_line)
        fields_return['discount_promotions'] = order_line.discount_promotions
        if order_line.price_unit_pdf:
            fields_return['price_unit'] = order_line.price_unit_pdf
        if order_line.descuento_pdf:
            fields_return['discount'] = order_line.descuento_pdf
        return fields_return


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    is_reward_line = fields.Boolean('Is a program reward line')
    discount_promotions = fields.Float()
    price_unit_pdf = fields.Float()
    descuento_pdf = fields.Float()
    price_unit = fields.Float(digits='Product Price')
    discount = fields.Float(digits='Discount')

    @api.model
    def _order_line_fields(self, line, session_id=None):
        fields_return = super(PosOrderLine, self)._order_line_fields(line, session_id=None)
        if line and line[2]:
            fields_return[2].update({'is_reward_line': line[2].get('is_reward_line', False)})
            fields_return[2].update({'discount_promotions': line[2].get('discount_promotions', 0)})
            fields_return[2].update({'price_unit': line[2].get('price_unit_pdf', fields_return[2]['price_unit'])})
            fields_return[2].update({'discount': line[2].get('descuento_pdf', fields_return[2]['discount'])})
        return fields_return