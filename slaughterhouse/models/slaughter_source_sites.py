# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Módulo creado para catalogo de sitios de origen.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      08/10/2021
    *************************************************************************/
"""

from odoo import models, fields, api, _


class SourceSites(models.Model):
    _name = "source.sites"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Specie"
    _rec_name = "origin_site_name"

    origin_site_name = fields.Char(string="Origin site name", store=True, tracking=True,
                                   help="The name of the source site will be specified in this field")
    reference = fields.Char(string="Reference", store=True, tracking=True,
                            help="In this field the reference of the site of origin will be specified.", size=10)
    partner_id = fields.Many2one(comodel_name='res.partner', string='livestock supplier', store=True, tracking=True,
                                 help="The livestock supplier will be chosen in this field.")
    responsible_site = fields.Char(string="Responsible for the site", store=True, tracking=True,
                                   help="The person responsible for the site will be specified in this field.")
    country_id = fields.Many2one(comodel_name='res.country', string='Country', store=True, tracking=True,
                                 help="In this field the catalog of countries will be displayed.")
    provincia_id = fields.Many2one(comodel_name='res.country.state', string='Provincia', store=True, tracking=True,
                                   help="In this field the catalog of provincia will be displayed.")
    city_id = fields.Many2one(comodel_name='res.city', string='City', store=True, tracking=True,
                              help="In this field the catalog of city will be displayed.")
    locality_id = fields.Char(string='Locality', store=True, tracking=True,
                                  help="In this field the locality will be defined.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, str(rec.origin_site_name)))
        return res
