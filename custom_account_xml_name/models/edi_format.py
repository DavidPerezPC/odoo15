# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging


_logger = logging.getLogger(__name__)


class EdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _create_invoice_cfdi_attachment(self, invoice, data):
        receptor_rfc = ''
        partner_rfc = ''
        if invoice.company_id.vat:
            receptor_rfc = invoice.company_id.vat
        if invoice.partner_id.vat:
            partner_rfc = invoice.partner_id.vat
        cfdi_filename = ('%s_%s_%s_%s.xml' % (receptor_rfc, invoice.name, invoice.invoice_date, partner_rfc)).replace(
            '/', '-')
        description = _('Mexican invoice CFDI generated for the %s document.') % invoice.name
        return self._create_cfdi_attachment(cfdi_filename, description, invoice, data)

    def _post_invoice_edi(self, invoices, test_mode=False):
        edi_result = super(EdiFormat, self)._post_invoice_edi(invoices, test_mode=test_mode)
        if self.code != 'cfdi_3_3':
            return edi_result

        for invoice in invoices:
            try:
                receptor_rfc = ''
                partner_rfc = ''
                name = str(invoice.sequence_prefix).replace('/','')
                name = str(name).replace('-','')                
                name += str(invoice.sequence_number)                    
                if invoice.company_id.vat:
                    receptor_rfc = invoice.company_id.vat
                if invoice.partner_id.vat:
                    partner_rfc = invoice.partner_id.vat
                cfdi_filename = ('%s_%s_%s.xml' % (receptor_rfc, name, partner_rfc)).replace('/', '')
                cfdi_filename = str(cfdi_filename).replace('-','_')
                attachments = edi_result[invoice]['attachment']
                for attachment in attachments:
                    attachment.name = cfdi_filename
            except Exception as error:
                _logger.info(error)
        return edi_result
