# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
       Módulo creado para catalogo de Conceptos de pasaje.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      08/10/2021
    *************************************************************************/
"""

from odoo import models, fields, api, _


class SlaughterPassageConcepts(models.Model):
    _name = "slaughter.passage.concepts"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Passage Concepts"
    _rec_name = "name_passage_concept"

    name_passage_concept = fields.Char(string="Name of the passage concept", store=True, tracking=True,
                                       help="In this field the name of the passage concept will be defined.")
    short_code = fields.Char(string="Short code", store=True, tracking=True,
                             help="IThe code is defined in this field.")
    concept_type = fields.Selection(
        [('purchase', 'Purchase'), ('won', 'Won'),
         ('shipment', 'Shipment'), ('sale', 'Sale'),
         ('transfer', 'Transfer')], string="Concept type", tracking=True,
        help="In this field the different types of concepts that exist will be shown.")
    movement_type = fields.Selection([('entry', 'Entry'), ('departure', 'Departure'), ('passage', 'Passage')],
                                     compute='automatic_value', store =True,
                                     string="Movement type", tracking=True,
                                     help="In this field the different types of movements will be shown..")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    @api.depends('concept_type')
    def automatic_value(self):
        for rec in self:
            rec.movement_type = rec.movement_type
            if rec.concept_type == 'purchase':
                rec.movement_type = 'entry'
            elif rec.concept_type == 'shipment':
                rec.movement_type = 'departure'
            elif rec.concept_type == 'sale':
                rec.movement_type = 'departure'
            elif rec.concept_type == 'won':
                rec.movement_type = rec.movement_type
            elif rec.concept_type == 'transfer':
                rec.movement_type = rec.movement_type
