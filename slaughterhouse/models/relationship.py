# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar la relación de almacén/subproducto/inroductor.
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


class Relationship(models.Model):
    _name = 'slaughter.relationship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Types Forfeiture'
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    type_register = fields.Selection([('carry entrails', 'Carry entrails'), ('leave entrails', 'Leave entrails')],
                                     string="Type of register", tracking=True, help="Field function: It shows the "
                                                                                    "different types of records to "
                                                                                    "select.")
    by_product_type = fields.Many2one(comodel_name='slaughter.sub.product.type', string='By product type', store=True,
                                      tracking=True,
                                      help="Field function: Show users who are by product type.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                                help="Field function: Show users who are specie.")
    location_id = fields.Many2one(comodel_name='stock.location', string='Location', store=True, tracking=True,
                                help="Field function: Show users who are location.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()
