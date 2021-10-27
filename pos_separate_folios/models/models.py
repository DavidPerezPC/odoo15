# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pos_separate_folios(models.Model):
    _inherit = 'pos.order'

    x_pos_invoice = fields.Char(string="Factura", compute="separate_name_facture_pos")
    x_pos_invoice_store = fields.Char(string="Factura", related="x_pos_invoice", store=True)

    @api.depends('state')
    def separate_name_facture_pos(self):
        for rec in self:
            invoiced_pos = rec.state
            if invoiced_pos == 'invoiced':
                folio = ''
                invoice_name_pos = self.env["account.move"].search([('invoice_origin', '=', rec.name)])
                x = len(invoice_name_pos)
                for i in invoice_name_pos:
                    na_fa_pos = i.name
                    if x > 1:
                        folio += na_fa_pos + ','
                    else:
                        folio += na_fa_pos
                rec.x_pos_invoice = folio
            elif invoiced_pos != 'invoiced':
                rec.x_pos_invoice = ''


class pos_separate(models.Model):
    _inherit = 'sale.order'

    x_invoice = fields.Char(string="Factura", compute="separate_name_facture")
    x_invoice_store = fields.Char(string="Factura", related="x_invoice", store=True)

    @api.depends('invoice_status')
    def separate_name_facture(self):
        for rec in self:
            invoiced = rec.invoice_status
            if invoiced == 'invoiced':
                folio = ''
                invoice_name = self.env["account.move"].search([('invoice_origin', '=', rec.name)])
                size = len(invoice_name)
                for i in invoice_name:
                    na_fa = i.name
                    if size > 1:
                        folio += na_fa + ','
                    else:
                        folio += na_fa
                rec.x_invoice = folio
            elif invoiced != 'invoiced':
                rec.x_invoice = ''
