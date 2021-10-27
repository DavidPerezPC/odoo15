# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math


class total_report_duration_days(models.Model):
    _inherit = 'stock.generate.report'

    x_sum_qty_pendding_supply = fields.Float(string='Sumatoria pendiente de surtir', compute='sum_field_report')
    x_sum_qty_on_hand = fields.Float(string='Sumatoria inventario actual', compute='sum_field_report')
    x_sum_daily_consumption_average = fields.Float(string='Sumatoria consumo promedio diario',
                                                   compute='sum_field_report')
    x_sum_qty_product = fields.Float(string='Sumatoria cantidad de producto', compute='sum_field_report')
    x_sum_duration_days = fields.Integer(string='Sumatoria duración días', compute='sum_field_report')

    @api.depends('inventory_lines')
    def sum_field_report(self):
        list1 = list()
        list2 = list()
        list3 = list()
        list4 = list()
        self.x_sum_qty_pendding_supply = 0.0
        self.x_sum_qty_on_hand = 0.0
        self.x_sum_daily_consumption_average = 0.0
        self.x_sum_qty_product = 0.0
        self.x_sum_duration_days = 0.0
        for rec in self:
            for i in rec.inventory_lines:
                list1.append(i.qty_per_supply)
                list2.append(i.qty_on_hand)
                list3.append(i.daily_consumption_average)
                list4.append(i.qty_product)
            self.x_sum_qty_pendding_supply = sum(list1)
            self.x_sum_qty_on_hand = sum(list2)
            self.x_sum_daily_consumption_average = sum(list3)
            self.x_sum_qty_product = sum(list4)
            if list4 and list2:
                if sum(list4) > 0 and sum(list3) > 0:
                    sumatory = sum(list4) / sum(list3)
                    sumatory_abs = abs(sumatory)
                    decimal_part, int_part = math.modf(sumatory_abs)
                    if decimal_part >= 0.5:
                        sumatory_abs = math.ceil(sumatory_abs)
                    else:
                        sumatory_abs = int_part
                    self.x_sum_duration_days = math.ceil(sumatory_abs)
                else:
                    self.x_sum_duration_days = 0.0
            else:
                self.x_sum_duration_days = 0.0
