# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class pos_refund(models.Model):
    _inherit = 'pos.order'

    x_is_refund = fields.Boolean(string="Es reembolso", compute="fun_is_refund", store=True)
    x_refund = fields.Many2one(comodel_name="pos.order", string="Ref.venta reembolso", compute="assignment_refund",
                               store=True)

    @api.depends('name')
    def assignment_refund(self):
        try:
            for rec in self:
                rec.x_refund = False
                search = self.env['pos.order'].search(
                    [('pos_reference', '=', rec.pos_reference), ('x_is_refund', '=', True)], limit=1)
                if not rec.x_is_refund:
                    if search:
                        rec.x_refund = search.id
                else:
                    search_reverse = self.env['pos.order'].search(
                        [('pos_reference', '=', rec.pos_reference), ('x_is_refund', '=', False)], limit=1)
                    rec.x_pos_invoice_store = search_reverse.x_pos_invoice_store
                    rec.x_refund = False
        except Exception as e:
            _logger.info(e)

    @api.depends('name')
    def fun_is_refund(self):
        search = self.env['pos.order'].search([('name', 'like', '%REEMBOLSO%')])
        self.x_is_refund = False
        try:
            for record in search:
                if record:
                    record.x_is_refund = True
        except Exception as e:
            _logger.info(e)


class option_pos_refun(models.Model):
    _inherit = 'pos.session'

    x_count_refund_session = fields.Integer(string="Reembolsos", compute="fun_count_refund", store=True)

    @api.depends('order_ids.amount_return')
    def fun_count_refund(self):
        try:
            for rec in self:
                search = self.env['pos.order'].search([('x_is_refund', '=', True), ('session_id', '=', rec.id)])
                count = len(search)
                rec.x_count_refund_session = count
        except Exception as e:
            _logger.info(e)

    def action_count_refund(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('point_of_sale.action_pos_pos_form')
        action['context'] = {}
        action['domain'] = [('x_is_refund', '=', True), ('session_id', '=', self.id)]
        return action
