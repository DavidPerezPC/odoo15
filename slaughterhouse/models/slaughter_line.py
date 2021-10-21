# -*- coding: utf-8 -*-

'''
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar la línea de sacrificio/corte a utilizar.
    * VERSION
      1.1
    * Author:
      Erick Enrique Abrego Gonzalez
    * Date:
      17/09/2021
    *************************************************************************/
'''

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError



class SlaughterLine(models.Model):
    _name = "slaughter.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Slaughter line"

    name = fields.Char(string="Description", store=True, tracking=True, help="Description of the line")
    code = fields.Integer(string="Line", store=True, tracking=True, help="Code of the line")
    full_name = fields.Char(string="Line name", compute="_compute_full_name", store=True, help="Full name of the line")
    sequence_line = fields.Integer(string="Sequence line")
    channel_weight = fields.Float(string="Channel weight", store=True, tracking=True, help="Weight when is in the channel")
    standing_weight = fields.Float(string="Standing weight", store=True, tracking=True, help="Weight when is standing")
    active = fields.Boolean(string="Active", default=True, tracking=True)

    @api.constrains('channel_weight','standing_weight')
    def _check_correct_weight(self):
        for record in self:
            if record.channel_weight < 0 or record.standing_weight < 0:
                raise ValidationError("It's not possible set negative value to the weight")

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            lines = self.env['slaughter.line'].search([('code','=',rec.code)])
            if len(lines) > 1:
                raise UserError(_("The line [{}] is already registered: ".format(rec.code)))

    @api.depends('name','code')
    def _compute_full_name(self):
        for rec in self:
            full_name = ''
            full_name += '[' + str(rec.code) + '] ' + str(rec.name)
            rec.full_name = full_name

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.code) + '] ' + str(rec.name)))
        return res

