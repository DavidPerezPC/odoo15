# -*- coding: utf-8 -*-
# Author: Jesús Valdes
# Date: 25/06/2021

from odoo import models, fields, api

class NewModule(models.Model):
    _inherit = 'hr.employee'

    x_NSS = fields.Char(string="Número de seguro social")
    x_INFONAVIT = fields.Char(string="Crédito de INFONAVIT")


