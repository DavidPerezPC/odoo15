# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar los diferentes tipos de ganado.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      17/09/2021
    *************************************************************************/
"""

from odoo import models, fields, api


class SlaughterCattleType(models.Model):
    _name = "slaughter.cattle.type"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cattle type"

    name = fields.Char(string="Description of the type of cattle", store=True,
                       help="The description is defined in this field", tracking=True)
    code = fields.Char(string="Internal reference ", store=True,
                       help="The internal reference is specified in this field.", tracking=True)
    gender = fields.Selection(
        [('b - male', 'B - Male'), ('h - female', 'H - Female'),
         ('a - both', 'A - Both')], string="Gender",
        tracking=True, help="In this field the genus of the species is defined.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                                help="Field function: Show users who are specie.")
    short_code = fields.Char(string="Short code", store=True,
                                  help="The short code is specified in this field", tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.code) + '] ' + str(rec.name)))
        return res
