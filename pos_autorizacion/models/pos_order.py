# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from decimal import *
from decimal import Decimal
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


class PosOrder(models.Model):
    _inherit = "pos.order"

    amount_in_words=fields.Char(string='Pos Order Amount in words')



    @api.model
    def l10n_mx_edi_cfdi_amount_to_text_order(self, data, otro):
        """Method to transform a float amount to text words
        E.g. 100 - ONE HUNDRED
        :returns: Amount transformed to words mexican format for invoices
        :rtype: str
        """

        pricelist_id=self.env['product.pricelist'].sudo().search([('id','=', otro['pricelist_id'])])

        currency_name =pricelist_id.currency_id.name.upper()

        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency_name == 'MXN' else 'M.E.'
        amount=otro['amount_total']
        # Split integer and decimal part
        amount_i, amount_d = divmod(amount, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))

        words = pricelist_id.currency_id.with_context(lang='es_ES').amount_to_text(amount_i).upper()

        return('%(words)s con %(amount_d)02d/100 %(currency_type)s' % {
            'words': words,
            'amount_d': amount_d,
            'currency_type': currency_type,
        })

    @api.model
    def _l10n_mx_edi_cfdi_amount_to_text(self):
        """Method to transform a float amount to text words
        E.g. 100 - ONE HUNDRED
        :returns: Amount transformed to words mexican format for invoices
        :rtype: str
        """
        self.ensure_one()

        currency_name = self.currency_id.name.upper()

        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency_name == 'MXN' else 'M.E.'

        # Split integer and decimal part
        amount_i, amount_d = divmod(self.amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))

        words = self.currency_id.with_context(lang=self.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
        return '%(words)s %(amount_d)02d/100 %(currency_type)s' % {
            'words': words,
            'amount_d': amount_d,
            'currency_type': currency_type,
        }

