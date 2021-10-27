# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pytz
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_lines.state', 'move_lines.date', 'move_type')
    def _compute_scheduled_date(self):
        super(StockPicking, self)._compute_scheduled_date()
        try:
            for picking in self:
                moves_dates = picking.move_lines.filtered(lambda move: move.state not in ('done', 'cancel')).mapped('date')
                user_tz = self.env.user.tz
                tz = pytz.timezone(user_tz)
                if picking.move_type == 'direct':
                    scheduled_date = min(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
                    if scheduled_date < fields.Datetime.now(tz):
                        picking.scheduled_date = fields.Datetime.now(tz)
                    else:
                        picking.scheduled_date = scheduled_date
                else:
                    scheduled_date = max(moves_dates, default=picking.scheduled_date or fields.Datetime.now())
                    if scheduled_date < fields.Datetime.now(tz):
                        picking.scheduled_date = fields.Datetime.now(tz)
                    else:
                        picking.scheduled_date = scheduled_date
        except Exception as error:
            _logger.info(error)


    @api.depends('move_lines.date_deadline', 'move_type')
    def _compute_date_deadline(self):
        super(StockPicking, self)._compute_date_deadline()
        try:
            for picking in self:
                user_tz = self.env.user.tz
                tz = pytz.timezone(user_tz)
                if picking.move_type == 'direct':
                    date_line = min(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)
                    if date_line < fields.Datetime.now(tz):
                        picking.date_deadline = fields.Datetime.now(tz)
                    else:
                        picking.date_deadline = date_line
                else:
                    date_line = max(picking.move_lines.filtered('date_deadline').mapped('date_deadline'), default=False)
                    if date_line < fields.Datetime.now(tz):
                        picking.date_deadline = fields.Datetime.now(tz)
                    else:
                        picking.date_deadline = date_line
        except Exception as error:
            _logger.info(error)