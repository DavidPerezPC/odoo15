# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar tipos  de decomisos.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      17/09/2021
    *************************************************************************/
"""


from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TypesForfeiture(models.Model):
    _name = 'types.forfeiture'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Types Forfeiture'
    _rec_name = "description"

    description = fields.Char(string="Description", store=True, tracking=True,
                              help="Field function: The description of the type of seizure is required in this field.")
    type = fields.Selection(
        [('standing animal', 'Standing Animal'), ('channel', 'Channel'),
         ('by-product', 'By-Product')], string="Type", tracking=True,
        help="Field function: It shows the different types of confiscation to select.")
    reference = fields.Char(string="Reference", store=True, size=10, tracking=True,
                            help="Field function: It shows the different types of confiscation to select.")
    location_id = fields.Many2one(comodel_name='stock.location', string='Location', store=True, tracking=True,
                                  help="Field function: Show users who are location.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    @api.constrains('reference')
    def same_reference(self):
        search = self.env['types.forfeiture'].search([])
        for record in search:
            for rec in self:
                if rec.reference == record.reference:
                    if rec.id != record.id:
                        raise UserError(_("A reference equal to this already exists: " + str(record.reference)))

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.reference) + '] ' + str(rec.description)))
        return res
