# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    l10n_mx_edi_payment_method_id = fields.Many2one('l10n_mx_edi.payment.method',
                                                    string="Payment Way", store=True,
                                                    help="Indicates the way the invoice was/will be paid, where the options could be: "
                                                         "Cash, Nominal Check, Credit Card, etc. Leave empty if unkown and the XML will show 'Unidentified'.",
                                                    default=lambda self: self.env.ref('l10n_mx_edi.payment_method_otros', raise_if_not_found=False))