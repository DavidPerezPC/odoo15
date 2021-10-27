from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    has_addenda = fields.Boolean(string="Contiene addenda?", default=False, compute="_get_has_addenda")

    @api.depends("partner_id")
    def _get_has_addenda(self):
        for rec in self:
            rec.has_addenda = False
            try:
                if rec.partner_id.is_company and rec.partner_id.l10n_mx_edi_addenda:
                    rec.has_addenda = True
                elif not rec.partner_id.is_company and rec.partner_id.parent_id.l10n_mx_edi_addenda:
                    rec.has_addenda = True
            except Exception as error:
                _logger.info(error)

