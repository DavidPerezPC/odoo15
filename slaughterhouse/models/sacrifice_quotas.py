# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar cuotas de sacrificio.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      17/09/2021
    *************************************************************************/
"""

from odoo import models, fields, api


class SacrificeQuotas(models.Model):
    _name = "sacrifice.quotas"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sacrifice quotas"
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                                help="Field function: Show users who are specie.")
    fee_per_head = fields.Float(string="Fee per head", store=True, tracking=True,
                                  help="In this field the user is asked to add the fee per head.")
    sow_quota = fields.Float(string="Sow quota", store=True, tracking=True,
                             help="In this field it is required to assign quota per sow.")
    is_overweight_fee = fields.Boolean(string="is overweight fee", store=True, tracking=True, default=False,
                                       help="In this field, the user is asked if they drive due to overweight.")
    starting_weight_over_weight = fields.Integer(string="Starting weight over weight", store=True, tracking=True,
                                                 default=0,
                                                 help="Field to assign the initial overweight weight.")
    final_weight_over_weight = fields.Integer(string="Final weight over weight", store=True, tracking=True, default=0,
                                              help="Field to assign the initial overweight weight.")
    overweight_fee = fields.Float(string="Overweight fee", store=True, tracking=True,
                                  help="In this field it is requested to add the sacrifice quota.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()
