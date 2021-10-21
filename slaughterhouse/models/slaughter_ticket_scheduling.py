# -*- coding: utf-8 -*-

"""
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar programaciones de entradas a sacrificio.
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
from datetime import datetime
import pytz


class SlaughterTicketScheduling(models.Model):
    _name = 'slaughter.ticket.scheduling'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Slaughter ticket scheduling'
    _rec_name = "slaughter_line"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft',
        store=True, copy=False, tracking=True, required=True, readonly=True)
    slaughter_line = fields.Many2one(comodel_name='slaughter.line', string='Slaughter line', store=True, tracking=True,
                                     help="Field function: Show users who are slaughter line.")
    specie_id = fields.Many2one(comodel_name='specie.catalog', string='Species name', store=True, tracking=True,
                             help="Field function: Show users who are specie.")
    slaughter_date = fields.Date(string="Slaughter date", store=True, tracking=True,
                                 help="Field function: Show users who are slaughter date.")
    active = fields.Boolean(default=True, tracking=True)

    @api.model
    def default_get(self, fields):
        res = super(SlaughterTicketScheduling, self).default_get(fields)
        time_zone = pytz.timezone('America/Chihuahua')
        res.update({
            'slaughter_date': datetime.now(tz=time_zone)
        })
        return res

    def action_discard(self):
        self.state = 'draft'
        return True

    def action_cancel(self):
        self.state = 'cancel'
        return True
