# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    street_name = fields.Char('Street Name')
    street_number = fields.Char('House Number')
    street_number2 = fields.Char('Door Number')
    street = fields.Char('Street')
    city = fields.Char('city')
    country_id = fields.Many2one('res.company.country')


