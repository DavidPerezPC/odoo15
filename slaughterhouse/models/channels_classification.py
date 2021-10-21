# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar Canales de clasificación.
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


class ChannelsClassification(models.Model):
    _name = 'channels.classification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Channels classification'
    _rec_name = "partner_id"

    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    classification_type = fields.Selection(
        [('standing weight', 'Standing Weight'), ('carcass weight', 'Carcass Weight'),
         ('carcass / truck weight performance', 'Carcass / Truck Weight Performance')], string="Type Classification",
        tracking=True, help="Field function: It shows the different types of classifications that exist.d function: "
                            "Show users who are introducers.")
    cattle_type = fields.Many2one(comodel_name='slaughter.cattle.type', string='Cattle type', store=True, tracking=True,
                                  help="Field function: It shows the different types of cattle that exist.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                             help="Field function: Show users who are specie.")
    quality = fields.Selection(
        [('approved quality', 'Approved Quality'), ('low quality chiclan', 'Low Quality Chiclan'),
         ('low quality +30', 'Low Quality +30'), ('low quality machacas', 'Low Quality Machacas'),
         ('low quality headless', 'Low Quality Headless')], tracking=True,
        help="Field function: It shows the different types of quality to select.")
    rank = fields.Char(string="Rank", compute="rank_function", store=True)
    starting_range = fields.Integer(string="Starting rank", store=True, tracking=True,
                                    help="The initial range will be defined in this field.")
    final_rank = fields.Integer(string="Final rank", store=True, tracking=True,
                                help="The final range will be defined in this field.")
    sort_code = fields.Char(string="Sort code", store=True, tracking=True,
                            help="The classification code will be defined in this "
                                 "field.")
    description_sort_code = fields.Char(string="Description sort code", store=True, tracking=True,
                                        help="The classification code description will be defined in this field.")
    product_code_channel = fields.Char(string="Product code in channel", store=True, tracking=True,
                                       help="The channel product code will be defined in this field.")
    sending_files = fields.Boolean(string="Sending files grouped in this classification.", store=True, tracking=True,
                                   help="In this field, the sending of files grouped in this classification will be "
                                        "defined.")
    active = fields.Boolean(default=True, tracking=True)
    sequence = fields.Integer()

    @api.constrains("partner_id", "starting_range", "final_rank")
    def overlap_rank(self):
        for rec in self:
            search = self.env["channels.classification"].search(
                [('partner_id', '=', rec.partner_id.name), ('sort_code', '=', rec.sort_code)])
            for val in search:
                if rec.starting_range in range(val.starting_range, val.final_rank):
                    if rec.id != val.id:
                        raise UserError(
                            _("The initial weight, overlaps with the classification code " + str(
                                val.sort_code) + " ,whose range is " + str(
                                val.rank) + " impossible to continue!!."))
                elif rec.starting_range == val.final_rank:
                    raise UserError(
                        _("The initial weight, overlaps with the classification code " + str(
                            val.sort_code) + " ,whose range is " + str(
                            val.rank) + " impossible to continue!!."))

    @api.constrains("starting_range", "final_rank")
    def no_negative_numbers(self):
        for rec in self:
            if rec.starting_range < 0:
                raise UserError(_("The starting range cannot be a negative number!."))
            elif rec.final_rank < 0:
                raise UserError(_("The final range cannot be a negative number!."))
            elif rec.final_rank <= rec.starting_range:
                raise UserError(_("The final range must be greater than the initial value!."))

    @api.depends("starting_range", "final_rank")
    def rank_function(self):
        for rec in self:
            self.rank = str(rec.starting_range) + ' - ' + str(rec.final_rank)

    @api.onchange('sort_code')
    def _check_sort_code(self):
        for rec in self:
            if rec.sort_code:
                sort_code = rec.sort_code
                rec.sort_code = sort_code.upper()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[' + str(rec.sort_code) + '] ' + str(rec.description_sort_code)))
        return res
