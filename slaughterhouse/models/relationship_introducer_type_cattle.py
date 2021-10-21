# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Catalogo de relación introductor/tipo de ganado.
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


class RelationshipIntroducerTypeCattle(models.Model):
    _name = 'relationship.introducer.type.cattle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Relationship Introducer Type Cattle'
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    cattle_type = fields.Many2one(comodel_name='slaughter.cattle.type', string='Cattle type', store=True, tracking=True,
                                  help="Field function: It shows the different types of cattle that exist.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                                help="Field function: Show users who are specie.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    @api.constrains("cattle_type", "partner_id")
    def different_places(self):
        for rec in self:
            search = self.env["relationship.introducer.type.cattle"].search(
                [('partner_id', '=', rec.partner_id.name),
                 ('cattle_type', '=', rec.cattle_type.name)])
            for val in search:
                if rec.id != val.id:
                    if rec.cattle_type.name == val.cattle_type.name:
                        raise UserError(_("The same introducer: " + str(
                            val.partner_id.name) + " cannot be established with the same type of cattle: " + str(
                            val.cattle_type.name)))
