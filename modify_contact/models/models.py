# -*- coding: utf-8 -*-

from odoo import models, fields, api


class modify_contact(models.Model):
    _inherit = 'stock.picking'

    Contact = fields.Many2one('res.partner',string="Contacto", related="partner_id", store=True)
