# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import re
_logger = logging.getLogger(__name__)

class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    @api.model
    def _l10n_mx_edi_get_serie_and_folio(self, move):
        res = super(AccountEdiFormat, self)._l10n_mx_edi_get_serie_and_folio(move)
        try:
            serie_number = str(res['serie_number']).replace('/', '')
            serie_number = serie_number.replace('-', '')
            serie_number = serie_number.replace('_', '')
            serie_number = ''.join(filter(lambda x: not x.isdigit(), serie_number))
            res['serie_number'] = serie_number
            if move.move_type == "out_refund":
                name_numbers = list(re.finditer('\d+', move.name))
                folio_number = name_numbers[-1].group().lstrip('0')
                sequence_prefix = ''.join(filter(lambda x: str(x).isdigit(), move.sequence_prefix))
                folio_number = str(sequence_prefix) + str(folio_number)
                res['folio_number'] = folio_number
        except Exception as error:
            _logger.info(error)
        return res