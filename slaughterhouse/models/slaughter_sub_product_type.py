# -*- coding: utf-8 -*-

'''
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar los tipos de subproductos existentes.
    * VERSION
      1.1
    * Author:
      Erick Enrique Abrego Gonzalez
    * Date:
      17/09/2021
    *************************************************************************/
'''

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError



class SlaughterSubProductType(models.Model):
    _name = 'slaughter.sub.product.type'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Type of the sub product'

    name = fields.Char(string="Description", store=True, help="Description of the sub product")
    code = fields.Char(string="Code", store=True, help="The sub product code is defined in this field")
    sequence_line = fields.Char(string="Sequence line")

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            lines = self.env['slaughter.sub.product.type'].search([('code', '=', rec.code)])
            if len(lines) > 1:
                raise UserError(_("The sub product code [{}] is already registered: ".format(rec.code)))

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.code) + '] ' + str(rec.name)))
        return res
