# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_introductory = fields.Boolean(string="Is introductory", default=False, store=True,
                                     help="The purpose of this field is to know if the contact is an introducer")