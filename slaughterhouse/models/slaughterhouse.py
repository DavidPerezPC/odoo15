# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class slaughterhouse(models.Model):
    _name = 'slaughterhouse.slaughterhouse'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Slaughterhouse'

    name = fields.Char(string="Name", store=True)
    active = fields.Boolean(default=True, tracking=True)
