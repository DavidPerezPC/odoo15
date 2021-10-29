from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import logging
# import odoo.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)


class InheritAccountPayment(models.Model):
    _inherit='account.payment'

    template_journal=fields.Selection(string='Nombre de plantilla para cheque', related='journal_id.template_bank')
    printed = fields.Boolean(string='Impreso', default=False)
    show_legend = fields.Boolean(string='Mostrar Leyenda',  store=True)

    @api.model
    def _get_template_journal(self):
        """
        Modify the generated barcode to be compatible with the default
        barcode rule in this module. See `data/default_barcode_patterns.xml`.
        """
        self.template_journal = self.journal_id.template_bank



    def _get_invoice_payment_amount(self, inv):
        """
        Computes the amount covered by the current payment in the given invoice.

        :param inv: an invoice object
        :returns: the amount covered by the payment in the invoice
        """
        print('journal',self.journal_id.template_bank)

        self.ensure_one()
        return sum([
            data['amount']
            for data in inv._get_reconciled_info_JSON_values()
            if data['account_payment_id'] == self.id
        ])


    # Obtengo los asteriscos de relleno para el monto de los cheques
    # Considera los separadores de 3 digitos
    def _get_custom_amount_space(self, length, is_currency_simbol = True):
        amount_int_length = len(str(int(self.amount)))
        length = length - 3 # .00
        asterisks = "*" * length
        commas = 0
        if (not is_currency_simbol): commas += 1 # $
        for comma in range(0, amount_int_length, 3): # ,   ,
            if (comma != 0):
                commas += 1
        asterisks = asterisks[commas:]
        return asterisks[ 0 : (len(asterisks) - amount_int_length) ]


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
        currency_type = 'M.N.' if currency_name == 'MXN' else 'M.E.'

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

    @api.model
    def setPrint(self):
        self.printed = True
        print('printed', self.printed)