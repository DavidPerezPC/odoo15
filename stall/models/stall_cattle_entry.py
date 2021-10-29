# -*- coding: utf-8 -*-


"""
    /*************************************************************************
    * Description
      Entrada de ganado.
    * VERSION
      1.1
    * Author:
      Jesús Ernesto Valdés Carrillo
    * Date:
      22/10/2021
    *************************************************************************/
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import random


class StallCattleEntry(models.Model):
    _name = 'stall.cattle.entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Cattle entry'
    _rec_name = 'sequence_ticket'

    state = fields.Selection(
        [('open', 'Open'), ('close', 'Close')], default='open',
        store=True, copy=False, tracking=True, required=True,
        readonly=True)
    sequence_ticket = fields.Char(string="Sequence", required=True, readonly=True, copy=False, index=True,
                                  default="Nuevo")
    name = fields.Char(string="Remission number", store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Introducer', store=True, tracking=True,
                                 help="Field function: Show users who are introducers.")
    livestock_supplier = fields.Many2one(comodel_name='res.partner', string='livestock supplier', store=True,
                                         tracking=True,
                                         help="The livestock supplier will be chosen in this field.")
    origin_site = fields.Many2one(comodel_name='source.sites', string='Origin site', store=True, tracking=True,
                                  help="The livestock supplier will be chosen in this field.")
    ticket_date = fields.Date(string="Ticket date", store=True, tracking=True,
                              help="Field function: Show users who are slaughter date.")
    company_purchase_order = fields.Many2one(comodel_name='res.company', string='Company purchase order', store=True,
                                             tracking=True,
                                             help="The livestock supplier will be chosen in this field.")
    purchase_order = fields.Char(string="Purchase order", store=True)
    lot_number = fields.Char(string="Lot number", store=True)

    # Remission
    shipping_date = fields.Date(string="Shipping date", store=True, tracking=True,
                                help="Field function: Show users who are slaughter date.")
    shipping_method = fields.Many2one(comodel_name='delivery.carrier', string='Shipping method', store=True,
                                      tracking=True,
                                      help="The livestock supplier will be chosen in this field.")
    drivers_name = fields.Many2one(comodel_name='res.partner', string='Drivers name', store=True, tracking=True,
                                   help="Field function: Show users who are introducers.")
    vehicle = fields.Many2one(comodel_name='fleet.vehicle', string='Vehicle', store=True, tracking=True,
                              help="Field function: Show users who are introducers.")
    plate_number = fields.Char(string="Plate number", compute="assign_plates", store=True, tracking=True,
                               help="Plate number")
    health_guide = fields.Char(string="Health guide", store=True, tracking=True, help="Health guide")
    transit_guide = fields.Char(string="Transit guide", store=True, tracking=True, help="Transit guide")
    another_document = fields.Char(string="Another document", store=True, tracking=True, help="Another document")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                                help="Field function: Show users who are specie.")
    cattle_type = fields.Many2one(comodel_name='slaughter.cattle.type', string='Cattle type', store=True, tracking=True,
                                  help="Field function: It shows the different types of cattle that exist.")
    heads_shipped = fields.Integer(string="Heads shipped", store=True, help="Heads shipped")
    kgs_sent = fields.Float(string="Kgs sent", store=True, help="Kgs sent")

    # Ticket detail
    gross_weight = fields.Float(string="Gross weight", store=True, help="Gross weight")
    tara_weight = fields.Float(string="Tara weight", store=True, help="Tara weight")
    neto_weight = fields.Float(string="Neto weight", store=True, help="Neto weight")
    transfer_loss = fields.Float(string="Transfer loss", store=True, help="Transfer loss")
    transfer_loss_percentage = fields.Float(string="% transfer loss", store=True, help="% transfer loss")
    start_time = fields.Float(string="Start time", store=True, help="Start time")
    final_time = fields.Float(string="Final time", store=True, help="Final time")

    heads_received = fields.Integer(string="Heads received", store=True, help="Heads received")
    hurt_heads = fields.Integer(string="Hurt heads", store=True, help="Hurt heads")
    sunny_heads = fields.Integer(string="Sunny heads", store=True, help="Sunny heads")
    dead_heads = fields.Integer(string="Dead heads", store=True, help="Dead heads")
    kgs_dead = fields.Float(string="Kgs dead", store=True, help="Kgs dead")
    comments = fields.Text(string="Commments", store=True, tracking=True, help="Comments")

    # Pen distribution
    to_distribute = fields.Integer(string="Cbz distribute", store=True, help="To distribute")
    heads_parts_distribute = fields.Integer(string="Heads ptes distribute", store=True, help="Heads parts distribute")
    corralero = fields.Many2one(comodel_name='hr.employee', string="Corralero", store=True, tracking=True,
                                help="Corralero")

    active = fields.Boolean(default=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence_ticket', _('New')) == _('New'):
            vals['sequence_ticket'] = self.env['ir.sequence'].next_by_code('ticket.sequence') or _('New')
            result = super(StallCattleEntry, self).create(vals)
            result['sequence_ticket'] = vals['sequence_ticket']
        return result

    @api.depends('state')
    def action_validate(self):
        self.state = 'validate'

    @api.depends('state')
    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('vehicle')
    def assign_plates(self):
        for rec in self:
            if rec.vehicle:
                for i in rec.vehicle:
                    rec.plate_number = i.license_plate

    def action_weigh(self):
        self.gross_weight = random.randrange(1, 1000, 1)

    def action_tara_weigh(self):
        self.tara_weight = random.randrange(1, 1000, 1)
