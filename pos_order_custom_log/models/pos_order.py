# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit = ['pos.order', 'mail.thread', 'mail.activity.mixin']