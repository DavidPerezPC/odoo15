from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _set_correct_name_to_xml(self):
        for rec in self:
            receptor_rfc = ''
            partner_rfc = ''
            if rec.company_id.vat:
                receptor_rfc = rec.company_id.vat
            if rec.partner_id.vat:
                partner_rfc = rec.partner_id.vat
            cfdi_filename = ('%s_%s_%s_%s.xml' % (receptor_rfc, rec.name, rec.invoice_date, partner_rfc)).replace('/', '-')
            if rec.move_type == 'out_invoice' or rec.move_type == 'out_refund':
                if rec.edi_document_ids:
                    for document in rec.edi_document_ids:
                        if document.name:
                            if 'xml' in document.name:
                                document.attachment_id.name = cfdi_filename