# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
    Catalogo de sitios de origen/introductor
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


class SlaughterSourceSitesIntroducer(models.Model):
    _name = 'slaughter.source.sites.introducer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Channels classification'
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    origin_site_id = fields.Many2one(comodel_name='source.sites', string='Origin site', store=True, tracking=True,
                                     help="Field function: Show users who are origin site.")
    receive_source_reference = fields.Boolean(string='requires receiving referral of origin to enter the trail',
                                              store=True, tracking=True,
                                              help="In this field the user specified if it is required to receive a referral to enter the trail.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    @api.constrains("origin_site_id")
    def different_places_of_origin(self):
        for rec in self:
            search = self.env["slaughter.source.sites.introducer"].search(
                [('partner_id', '=', rec.partner_id.name),
                 ('origin_site_id', '=', rec.origin_site_id.origin_site_name)])
            for val in search:
                if rec.id != val.id:
                    if rec.origin_site_id.origin_site_name == val.origin_site_id.origin_site_name:
                        raise UserError(
                            _("The same introducer: " + str(val.partner_id.name) + " /origin: " + str(
                                val.origin_site_id.origin_site_name) + " relationship cannot be established more than once."))
