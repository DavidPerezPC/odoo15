# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar catalogo de especies.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      17/09/2021
    *************************************************************************/
"""

from odoo import models, fields, api, _


class SpecieCatolog(models.Model):
    _name = "specie.catalog"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Specie"

    name = fields.Char(string="Species name", store=True, help="The species of cattle is defined in this field.")
    reference = fields.Char(string="Reference", store=True, help="The species reference is defined in this field.")
    active = fields.Boolean(default=True, tracking=True)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.reference) + '] ' + str(rec.name)))
        return res
