# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from decimal import *
import operator
import math
from num2words import num2words
from datetime import *
import datetime
import json
import re
import uuid
from functools import partial
from lxml import etree
from dateutil.relativedelta import relativedelta

import pytz

class PosOrder(models.Model):
    _inherit = "pos.order"


    pos_date_due = fields.Date(string='Due Date', readonly=True, index=True, copy=False,
                               states={'draft': [('readonly', False)]})
    total_discount_tarifa = fields.Float(string='Discount tarifa')
    discountpromo = fields.Float(string='Discount Promo')
    price_discount = fields.Float(string='price list discount')
    invoice_number = fields.Char(string='Invoice number')
    onchange_promotions = fields.Integer(string='Global promociones')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        partner_id = self.env['res.partner'].sudo().search([('id', '=', ui_order['partner_id'])])

        res['pos_date_due'] = ui_order.get('pos_date_due', False)
        res['amount_in_words'] = ui_order.get('amount_in_words', False)
        res['invoice_number'] = ui_order.get('invoice_number', False)
        amount_in_words = self.l10n_mx_edi_cfdi_amount_to_text_order(partner_id, ui_order)


        # res['pos_date_due']=(self.calculate_pos_date_due(ui_order)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        res['amount_in_words']=amount_in_words
        res['invoice_number'] = self.get_account_move(partner_id, ui_order)

        return res

    @api.model
    def calculate_pos_date_due(self, ui_order):
        partner_id = self.env['res.partner'].sudo().search([('id', '=', ui_order['partner_id'])])

        pos_date_due = ''
        for key in partner_id.property_payment_term_id.line_ids:
            if key.days > 0:
                pos_date_due = datetime.datetime.strptime(ui_order['creation_date'].replace('T', ' ')[:19],
                                                          '%Y-%m-%d %H:%M:%S') + timedelta(days=key.days)
                print(pos_date_due)

        self.pos_date_due=pos_date_due
        return (pos_date_due)

    @api.model
    def _process_order(self, order, draft, existing_order):
        """Create or update an pos.order from a given dictionary.

        :param dict order: dictionary representing the order.
        :param bool draft: Indicate that the pos_order is not validated yet.
        :param existing_order: order to be updated or False.
        :type existing_order: pos.order.
        :returns: id of created/updated pos.order
        :rtype: int
        """
        order = order['data']
        print(order)
        pos_session = self.env['pos.session'].browse(order['pos_session_id'])
        if pos_session.state == 'closing_control' or pos_session.state == 'closed':
            order['pos_session_id'] = self._get_valid_session(order).id

        pos_order = False
        if not existing_order:
            pos_order = self.create(self._order_fields(order))
        else:
            pos_order = existing_order
            pos_order.lines.unlink()
            order['user_id'] = pos_order.user_id.id
            pos_order.write(self._order_fields(order))
        print(pos_order.pos_date_due)
        pos_order = pos_order.with_company(pos_order.company_id)
        self = self.with_company(pos_order.company_id)
        self._process_payment_lines(order, pos_order, pos_session, draft)

        if not draft:
            try:
                pos_order.action_pos_order_paid()
            except psycopg2.DatabaseError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))
            pos_order._create_order_picking()

        if pos_order.to_invoice and pos_order.state == 'paid':
            pos_order.action_pos_order_invoice()

        return pos_order.id

    @api.model
    def get_account_move(self, data, otro):

        order_number = self.search([('pos_reference', '=', otro['name'])])
        return order_number.account_move.name