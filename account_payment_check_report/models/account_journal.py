from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import logging
# import odoo.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)


class InheritAccountPayment(models.Model):
    _inherit='account.journal'

    template_bank = fields.Selection([
        ('report_payment_check_document', 'Bancomer'),
        ('report_payment_check_document_s', 'Santander'),
        ('report_payment_check_document_b', 'Banorte'),
        ('report_payment_check_document_c', 'Citibanamex'),
        ('report_payment_check_document_cgpi', 'Banamex GPI')
    ], string='Template', copy=False, index=True, track_visibility='onchange')

