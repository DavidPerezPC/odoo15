# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date, get_lang
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def sent_auto_invoice_email(self):
        for rec in self:
            try:
                if rec.move_type in ('out_invoice','out_refund'):
                    if rec.partner_id.x_is_auto_invoice_send and rec.state == 'posted' and rec.edi_state == 'sent':
                        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
                        rec.message_post_with_template(template.id)
                        rec.is_move_sent = True
            except Exception as error:
                _logger.info(error)

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_is_auto_invoice_send = fields.Boolean(string="Envio automático de factura", default=False, store=True, tracking=True)



